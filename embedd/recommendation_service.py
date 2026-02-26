"""
Book Recommendation Service

Provides personalized book recommendations based on:
- User search history
- Reading patterns
- Similar users (collaborative filtering)
- Content similarity (content-based filtering)
- User preferences and education level
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from collections import Counter
from embedd.vector_db import BookChunkEmbedding, SearchLog, RecommendationLog, get_db_session
from embedd.embedding_service import get_embedding_service


class RecommendationService:
    """Generate personalized book recommendations"""
    
    def __init__(self):
        self.embedding_service = get_embedding_service()
    
    def get_recommendations(
        self,
        user_phone: str = None,
        search_history: List[str] = None,
        education_level: str = None,
        interests: List[str] = None,
        limit: int = 5,
        db: Session = None
    ) -> List[Dict]:
        """
        Get personalized recommendations
        
        Args:
            user_phone: User phone number for history
            search_history: List of recent queries
            education_level: User's education level (primary, secondary, university)
            interests: User's interests (subjects/topics)
            limit: Maximum recommendations to return
            db: Database session
        
        Returns:
            List of recommendation dicts with title, score, reason
        """
        if db is None:
            db = get_db_session()
        
        recommendations = []
        
        try:
            # 1. Content-based recommendations from search history
            if search_history or user_phone:
                content_recs = self._content_based_recommendations(
                    user_phone, search_history, limit * 2, db
                )
                recommendations.extend(content_recs)
            
            # 2. Collaborative filtering (similar users)
            if user_phone:
                collab_recs = self._collaborative_recommendations(
                    user_phone, limit, db
                )
                recommendations.extend(collab_recs)
            
            # 3. Interest-based recommendations
            if interests:
                interest_recs = self._interest_based_recommendations(
                    interests, limit, db
                )
                recommendations.extend(interest_recs)
            
            # 4. Trending books (popular recent searches)
            trending_recs = self._trending_recommendations(limit, db)
            recommendations.extend(trending_recs)
            
            # Deduplicate and rank
            final_recs = self._rank_and_deduplicate(recommendations, limit)
            
            # Log recommendations
            if user_phone and final_recs:
                self._log_recommendation(user_phone, final_recs, db)
            
            return final_recs
            
        finally:
            if db is None:
                db.close()
    
    def _content_based_recommendations(
        self,
        user_phone: str,
        search_history: List[str],
        limit: int,
        db: Session
    ) -> List[Dict]:
        """Recommend books similar to user's search history"""
        recommendations = []
        
        # Get recent searches from database if user_phone provided
        if user_phone:
            recent_searches = db.query(SearchLog).filter(
                SearchLog.user_phone == user_phone
            ).order_by(desc(SearchLog.created_at)).limit(10).all()
            
            search_queries = [log.query for log in recent_searches]
        else:
            search_queries = search_history or []
        
        if not search_queries:
            return recommendations
        
        # Combine queries into a profile
        user_profile = " ".join(search_queries)
        profile_embedding = self.embedding_service.generate_embedding(user_profile)
        
        # Find similar books
        all_chunks = db.query(BookChunkEmbedding).all()
        
        book_scores = {}
        for chunk in all_chunks:
            score = self.embedding_service.similarity_score(
                profile_embedding,
                chunk.embedding
            )
            
            book_key = (chunk.book_id, chunk.title, chunk.author)
            if book_key not in book_scores:
                book_scores[book_key] = {
                    "score": score,
                    "category": chunk.category,
                    "snippet": chunk.chunk_text[:150]
                }
            else:
                book_scores[book_key]["score"] = max(
                    book_scores[book_key]["score"], score
                )
        
        # Convert to recommendations
        for (book_id, title, author), data in sorted(
            book_scores.items(),
            key=lambda x: x[1]["score"],
            reverse=True
        )[:limit]:
            recommendations.append({
                "book_id": book_id,
                "title": title,
                "author": author,
                "score": data["score"],
                "reason": "Based on your reading interests",
                "category": data["category"],
                "snippet": data["snippet"]
            })
        
        return recommendations
    
    def _collaborative_recommendations(
        self,
        user_phone: str,
        limit: int,
        db: Session
    ) -> List[Dict]:
        """Recommend books that similar users found interesting"""
        recommendations = []
        
        # Get user's search queries
        user_searches = db.query(SearchLog.query).filter(
            SearchLog.user_phone == user_phone
        ).all()
        user_queries = {search.query for search in user_searches}
        
        if not user_queries:
            return recommendations
        
        # Find users with overlapping searches
        similar_users = db.query(SearchLog.user_phone).filter(
            SearchLog.query.in_(user_queries),
            SearchLog.user_phone != user_phone
        ).distinct().limit(50).all()
        
        similar_user_phones = [u.user_phone for u in similar_users]
        
        # Get what they searched for that user hasn't
        their_searches = db.query(SearchLog.query).filter(
            SearchLog.user_phone.in_(similar_user_phones)
        ).all()
        
        their_queries = [s.query for s in their_searches if s.query not in user_queries]
        
        # Count popular queries
        query_counts = Counter(their_queries)
        popular_queries = query_counts.most_common(limit)
        
        # Find books matching popular queries
        for query, count in popular_queries:
            query_embedding = self.embedding_service.generate_embedding(query)
            
            chunks = db.query(BookChunkEmbedding).limit(20).all()
            
            for chunk in chunks:
                score = self.embedding_service.similarity_score(
                    query_embedding,
                    chunk.embedding
                )
                
                if score > 0.4:  # Threshold for relevance
                    recommendations.append({
                        "book_id": chunk.book_id,
                        "title": chunk.title,
                        "author": chunk.author,
                        "score": score * (count / 10),  # Weight by popularity
                        "reason": f"Popular with similar readers ({count} searches)",
                        "category": chunk.category,
                        "snippet": chunk.chunk_text[:150]
                    })
                    break  # One book per query
        
        return recommendations
    
    def _interest_based_recommendations(
        self,
        interests: List[str],
        limit: int,
        db: Session
    ) -> List[Dict]:
        """Recommend books matching user's stated interests"""
        recommendations = []
        
        # Combine interests into a query
        interest_query = " ".join(interests)
        query_embedding = self.embedding_service.generate_embedding(interest_query)
        
        # Find matching books
        all_chunks = db.query(BookChunkEmbedding).all()
        
        book_matches = {}
        for chunk in all_chunks:
            score = self.embedding_service.similarity_score(
                query_embedding,
                chunk.embedding
            )
            
            book_key = (chunk.book_id, chunk.title, chunk.author)
            if book_key not in book_matches:
                book_matches[book_key] = {
                    "score": score,
                    "category": chunk.category,
                    "snippet": chunk.chunk_text[:150]
                }
            else:
                book_matches[book_key]["score"] = max(
                    book_matches[book_key]["score"], score
                )
        
        # Convert to recommendations
        for (book_id, title, author), data in sorted(
            book_matches.items(),
            key=lambda x: x[1]["score"],
            reverse=True
        )[:limit]:
            recommendations.append({
                "book_id": book_id,
                "title": title,
                "author": author,
                "score": data["score"],
                "reason": f"Matches your interests: {', '.join(interests[:2])}",
                "category": data["category"],
                "snippet": data["snippet"]
            })
        
        return recommendations
    
    def _trending_recommendations(
        self,
        limit: int,
        db: Session
    ) -> List[Dict]:
        """Recommend currently trending/popular books"""
        recommendations = []
        
        # Get popular searches from last 7 days
        week_ago = datetime.utcnow() - timedelta(days=7)
        recent_searches = db.query(SearchLog.query).filter(
            SearchLog.created_at >= week_ago
        ).all()
        
        query_counts = Counter([s.query for s in recent_searches])
        popular_queries = query_counts.most_common(limit)
        
        for query, count in popular_queries:
            query_embedding = self.embedding_service.generate_embedding(query)
            
            # Find top book for this query
            chunks = db.query(BookChunkEmbedding).limit(10).all()
            
            best_chunk = None
            best_score = 0
            
            for chunk in chunks:
                score = self.embedding_service.similarity_score(
                    query_embedding,
                    chunk.embedding
                )
                if score > best_score:
                    best_score = score
                    best_chunk = chunk
            
            if best_chunk and best_score > 0.3:
                recommendations.append({
                    "book_id": best_chunk.book_id,
                    "title": best_chunk.title,
                    "author": best_chunk.author,
                    "score": best_score * 0.8,  # Slightly lower weight
                    "reason": f"Trending ({count} recent searches)",
                    "category": best_chunk.category,
                    "snippet": best_chunk.chunk_text[:150]
                })
        
        return recommendations
    
    def _rank_and_deduplicate(
        self,
        recommendations: List[Dict],
        limit: int
    ) -> List[Dict]:
        """Remove duplicates and return top recommendations"""
        # Group by book_id
        book_map = {}
        
        for rec in recommendations:
            book_id = rec["book_id"]
            
            if book_id not in book_map:
                book_map[book_id] = rec
            else:
                # Keep the one with better reason or higher score
                if rec["score"] > book_map[book_id]["score"]:
                    book_map[book_id] = rec
        
        # Sort by score
        unique_recs = sorted(
            book_map.values(),
            key=lambda x: x["score"],
            reverse=True
        )
        
        return unique_recs[:limit]
    
    def _log_recommendation(
        self,
        user_phone: str,
        recommendations: List[Dict],
        db: Session
    ):
        """Log recommendations for analytics"""
        book_ids = [rec["book_id"] for rec in recommendations]
        reasons = ", ".join(set(rec["reason"] for rec in recommendations[:3]))
        
        log = RecommendationLog(
            user_phone=user_phone,
            recommended_books=book_ids,
            reason=reasons[:200],
            engagement="shown"
        )
        
        db.add(log)
        db.commit()


def get_recommendation_service():
    """Get recommendation service instance"""
    return RecommendationService()


if __name__ == "__main__":
    # Test recommendations
    print("🎯 Book Recommendation Service")
    service = RecommendationService()
    
    # Test with sample data
    recs = service.get_recommendations(
        interests=["physics", "engineering"],
        limit=5
    )
    
    print(f"\n✓ Generated {len(recs)} recommendations")
    for rec in recs:
        print(f"  - {rec['title']} by {rec['author']}")
        print(f"    Score: {rec['score']:.2f} | {rec['reason']}")
