"""
Semantic Search Service

Query embeddings and find relevant books using vector similarity.
"""

import os
import numpy as np
from pathlib import Path
from typing import List, Tuple, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from embedd.embedding_service import get_embedding_service, EmbeddingResult
from embedd.vector_db import BookChunkEmbedding, SearchLog, get_db_session

class SemanticSearchService:
    """Search books using semantic similarity"""
    
    def __init__(self):
        self.embedding_service = get_embedding_service()
        self._catalogue_cache: Optional[List[dict]] = None
        self._catalogue_mtime: Optional[float] = None
    
    def search(
        self,
        query: str,
        limit: int = 10,
        similarity_threshold: float = 0.3,
        db: Session = None
    ) -> List[Tuple[str, float, str]]:
        """
        Semantic search for books
        
        Args:
            query: Search query in natural language
            limit: Maximum results to return
            similarity_threshold: Minimum similarity score (0-1)
            db: Database session
        
        Returns:
            List of (title, similarity_score, snippet) tuples
        """
        if db is None:
            db = get_db_session()
        
        try:
            # Fast path: try text match first to avoid slow embeddings
            text_results = self._text_search(query, limit, db)
            if text_results:
                self._log_search(query, None, len(text_results), db)
                print(f"✓ Found {len(text_results)} relevant books (text match)")
                return text_results

            # Optional: skip embeddings entirely
            if os.getenv("SEARCH_SKIP_EMBEDDINGS", "0") == "1":
                print("⚠ Embedding search skipped by SEARCH_SKIP_EMBEDDINGS=1")
                return []

            # Generate embedding for query
            print(f"🔍 Searching for: '{query}'")
            query_embedding = self.embedding_service.generate_embedding(query)
            
            # Find similar chunks in database
            chunk_scan_limit = int(os.getenv("SEARCH_CHUNK_SCAN_LIMIT", "1000"))
            all_chunks = db.query(BookChunkEmbedding).limit(chunk_scan_limit).all()
            
            if not all_chunks:
                print("No books indexed yet. Run embedding generation first.")
                return []
            
            # Calculate similarity for all chunks (vectorized)
            query_vec = np.array(query_embedding, dtype=float)
            chunk_matrix = np.array([c.embedding for c in all_chunks], dtype=float)
            if chunk_matrix.size == 0:
                return []

            dot_products = np.dot(chunk_matrix, query_vec)
            norms = np.linalg.norm(chunk_matrix, axis=1) * np.linalg.norm(query_vec)
            with np.errstate(divide="ignore", invalid="ignore"):
                scores = np.where(norms == 0, 0.0, dot_products / norms)

            similarities = [
                {"chunk": all_chunks[i], "score": float(scores[i])}
                for i in range(len(all_chunks))
                if scores[i] >= similarity_threshold
            ]
            
            # Sort by similarity
            similarities.sort(key=lambda x: x["score"], reverse=True)
            
            # Group by book and get best chunks
            book_results = {}
            for item in similarities[:limit * 3]:  # Get more chunks to group
                book_id = item["chunk"].book_id
                
                if book_id not in book_results:
                    book_results[book_id] = {
                        "title": item["chunk"].title,
                        "author": item["chunk"].author,
                        "category": item["chunk"].category,
                        "score": item["score"],
                        "snippet": item["chunk"].chunk_text[:200]
                    }
                else:
                    # Keep highest score
                    if item["score"] > book_results[book_id]["score"]:
                        book_results[book_id]["score"] = item["score"]
            
            # Format results
            results = [
                (result["title"], result["score"], result["snippet"])
                for result in sorted(
                    book_results.values(),
                    key=lambda x: x["score"],
                    reverse=True
                )[:limit]
            ]
            
            # Log search
            self._log_search(query, query_embedding, len(results), db)
            
            print(f"✓ Found {len(results)} relevant books")
            return results
        
        except Exception as e:
            print(f"✗ Search error: {str(e)}")
            return []
        
        finally:
            db.close()

    def _text_search(
        self,
        query: str,
        limit: int,
        db: Session
    ) -> List[Tuple[str, float, str]]:
        """Fast text search for exact/partial matches."""
        q = query.strip()
        if not q:
            return []

        # 1) Reference catalogue (fast text data)
        catalogue = self._load_reference_catalogue()
        if catalogue:
            q_lower = q.lower()
            exact_matches = [
                row for row in catalogue
                if row["book"].lower() == q_lower
            ]

            if exact_matches:
                row = exact_matches[0]
                return [(
                    row["book"],
                    1.0,
                    f"Shelf: {row['shelf']} | Library: {row['library']} | Location: {row['location']}"
                )]

            partial_matches = [
                row for row in catalogue
                if q_lower in row["book"].lower()
                or q_lower in row["library"].lower()
                or q_lower in row["location"].lower()
                or q_lower in row["shelf"].lower()
            ]

            if partial_matches:
                results = [
                    (
                        row["book"],
                        0.85,
                        f"Shelf: {row['shelf']} | Library: {row['library']} | Location: {row['location']}"
                    )
                    for row in partial_matches[:limit]
                ]
                return results

        # 2) Fallback to embeddings DB text search (optional - can fail gracefully)
        if os.getenv("SKIP_DB_TEXT_SEARCH", "0") == "1":
            return []

        try:
            exact = db.query(BookChunkEmbedding).filter(
                BookChunkEmbedding.title.ilike(q)
            ).limit(1).all()

            if exact:
                chunk = exact[0]
                return [(chunk.title, 1.0, chunk.chunk_text[:200])]

            partial = db.query(BookChunkEmbedding).filter(
                BookChunkEmbedding.title.ilike(f"%{q}%")
            ).limit(limit).all()

            return [(c.title, 0.8, c.chunk_text[:200]) for c in partial]
        except Exception as e:
            print(f"⚠ DB text search failed (using catalogue only): {str(e)[:100]}")
            return []

    def _load_reference_catalogue(self) -> List[dict]:
        """Load pipe-delimited reference catalogue for fast text search."""
        catalogue_path = Path(__file__).resolve().parent.parent / "Ingestion" / "catalogue.txt"
        if not catalogue_path.exists():
            return []

        mtime = catalogue_path.stat().st_mtime
        if self._catalogue_cache is not None and self._catalogue_mtime == mtime:
            return self._catalogue_cache

        rows: List[dict] = []
        with open(catalogue_path, encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]

        if not lines:
            return []

        header = lines[0].lower()
        expected = "book|shelf|library|location"
        start_idx = 1 if header == expected else 0

        for line in lines[start_idx:]:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) != 4:
                continue
            book, shelf, library, location = parts
            rows.append({
                "book": book,
                "shelf": shelf,
                "library": library,
                "location": location,
            })

        self._catalogue_cache = rows
        self._catalogue_mtime = mtime
        return rows
    
    def get_recommendations(
        self,
        user_phone: str,
        search_history: List[str] = None,
        education_level: str = None,
        interests: List[str] = None,
        limit: int = 5,
        db: Session = None
    ) -> List[Tuple[str, str, float]]:
        """
        Get personalized book recommendations
        
        Args:
            user_phone: User phone number
            search_history: List of previous searches
            education_level: User's education level (primary, secondary, tertiary)
            interests: User's interests
            limit: Number of recommendations
            db: Database session
        
        Returns:
            List of (title, reason, score) tuples
        """
        if db is None:
            db = get_db_session()
        
        try:
            recommendations = {}
            
            # Strategy 1: Based on search history
            if search_history:
                print(f"📚 Generating recommendations from search history...")
                for query in search_history[-5:]:  # Last 5 searches
                    results = self.search(query, limit=3, db=db)
                    for title, score, _ in results:
                        if title not in recommendations:
                            recommendations[title] = {
                                "score": score,
                                "reason": f"Based on your interest in '{query[:30]}...'"
                            }
            
            # Strategy 2: Based on interests
            if interests:
                print(f"🎯 Generating recommendations from interests...")
                for interest in interests:
                    results = self.search(interest, limit=3, db=db)
                    for title, score, _ in results:
                        if title not in recommendations:
                            recommendations[title] = {
                                "score": score * 0.8,
                                "reason": f"Matches your interest in {interest}"
                            }
            
            # Strategy 3: Popular books in category
            if education_level:
                print(f"📖 Adding {education_level} level recommendations...")
                popular = db.query(
                    BookChunkEmbedding.title,
                    func.avg(BookChunkEmbedding.embedding).label("avg_embedding")
                ).filter(
                    BookChunkEmbedding.category == education_level
                ).group_by(BookChunkEmbedding.title).limit(5).all()
                
                for title, _ in popular:
                    if title not in recommendations:
                        recommendations[title] = {
                            "score": 0.7,
                            "reason": f"Popular among {education_level} level readers"
                        }
            
            # Sort by score and return
            sorted_recommendations = sorted(
                recommendations.items(),
                key=lambda x: x[1]["score"],
                reverse=True
            )[:limit]
            
            results = [
                (title, rec["reason"], rec["score"])
                for title, rec in sorted_recommendations
            ]
            
            print(f"✓ Generated {len(results)} recommendations")
            return results
        
        except Exception as e:
            print(f"✗ Recommendation error: {str(e)}")
            return []
        
        finally:
            db.close()
    
    def _log_search(
        self,
        query: str,
        embedding: Optional[List[float]],
        results_count: int,
        db: Session
    ):
        """Log search for analytics"""
        try:
            log = SearchLog(
                query=query,
                query_embedding=embedding,
                results_count=results_count
            )
            db.add(log)
            db.commit()
        except:
            pass  # Don't fail if logging fails

# Singleton
_search_service = None

def get_search_service() -> SemanticSearchService:
    """Get search service instance"""
    global _search_service
    if _search_service is None:
        _search_service = SemanticSearchService()
    return _search_service
