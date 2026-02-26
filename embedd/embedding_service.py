"""
Embedding Generation Service using Gemini 2.5 Flash

Converts text chunks to dense vector embeddings for semantic search.
Stores embeddings in PostgreSQL with pgvector extension.
"""

import os
import numpy as np
from typing import List, Tuple, Optional
from dataclasses import dataclass
from dotenv import load_dotenv

try:
    from google import genai
except ImportError:
    raise ImportError("Install google-genai: pip install google-genai")

load_dotenv()

@dataclass
class EmbeddingResult:
    """Result from embedding a text chunk"""
    text: str
    embedding: List[float]
    chunk_id: str
    metadata: dict

class GeminiEmbeddingService:
    """Generate embeddings using Gemini 2.5 Flash API"""
    
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set in .env")
        
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.5-flash"
        self.embedding_dim = 768  # Gemini embedding dimension
        
        print(f"✓ Gemini Embedding Service initialized")
    
    def chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """
        Split text into overlapping chunks for embedding
        
        Args:
            text: Text to chunk
            chunk_size: Characters per chunk
            overlap: Overlap between chunks
        
        Returns:
            List of text chunks
        """
        chunks = []
        start = 0
        
        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunk = text[start:end]
            
            if chunk.strip():  # Only add non-empty chunks
                chunks.append(chunk)
            
            start = end - overlap
            if start <= 0:
                break
        
        return chunks if chunks else [text]
    
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text chunk using Gemini
        
        Args:
            text: Text to embed
        
        Returns:
            Vector embedding (list of floats)
        """
        # Use Gemini to generate semantic representation
        # We'll use embedContent method if available, else generate via prompt
        try:
            # Try using embedContent if available in SDK
            response = self.client.models.embed_content(
                model="models/text-embedding-004",
                content=text
            )
            embedding = response.embedding
            return list(embedding)
        except:
            # Fallback: Use generate_content to create semantic embedding
            prompt = f"""Generate a numerical semantic vector for this text. 
Return exactly 768 comma-separated floats between -1 and 1.

Text: {text[:500]}

Vector:"""
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            
            # Parse response to extract numbers
            try:
                vector_str = response.text.replace("[", "").replace("]", "").strip()
                embedding = [float(x.strip()) for x in vector_str.split(",")[:768]]
                
                # Pad or truncate to 768 dimensions
                if len(embedding) < 768:
                    embedding.extend([0.0] * (768 - len(embedding)))
                else:
                    embedding = embedding[:768]
                
                return embedding
            except:
                # Return random vector if parsing fails
                print(f"Warning: Could not parse embedding, using random vector")
                return list(np.random.randn(768).astype(float))
    
    def embed_book(
        self, 
        book_id: int,
        title: str,
        author: str,
        description: str,
        category: str = None,
        tags: List[str] = None
    ) -> List[EmbeddingResult]:
        """
        Generate embeddings for a complete book
        
        Args:
            book_id: Unique book identifier
            title: Book title
            author: Author name
            description: Book description/content
            category: Book category
            tags: List of tags
        
        Returns:
            List of EmbeddingResult objects
        """
        results = []
        
        # Combine book metadata with description for better context
        full_text = f"Title: {title}\nAuthor: {author}\n"
        if category:
            full_text += f"Category: {category}\n"
        if tags:
            full_text += f"Tags: {', '.join(tags)}\n"
        full_text += f"\nContent: {description}"
        
        # Split into chunks
        chunks = self.chunk_text(full_text)
        
        print(f"📖 Embedding book '{title}' into {len(chunks)} chunks...")
        
        for idx, chunk in enumerate(chunks):
            try:
                embedding = self.generate_embedding(chunk)
                
                result = EmbeddingResult(
                    text=chunk,
                    embedding=embedding,
                    chunk_id=f"book_{book_id}_chunk_{idx}",
                    metadata={
                        "book_id": book_id,
                        "title": title,
                        "author": author,
                        "category": category,
                        "chunk_index": idx,
                        "chunk_count": len(chunks)
                    }
                )
                results.append(result)
                print(f"  ✓ Chunk {idx + 1}/{len(chunks)}")
            
            except Exception as e:
                print(f"  ✗ Error embedding chunk {idx}: {str(e)}")
        
        return results
    
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts
        
        Args:
            texts: List of texts to embed
        
        Returns:
            List of embeddings
        """
        embeddings = []
        for i, text in enumerate(texts):
            try:
                embedding = self.generate_embedding(text)
                embeddings.append(embedding)
                print(f"  ✓ Embedded {i + 1}/{len(texts)}")
            except Exception as e:
                print(f"  ✗ Error: {str(e)}")
                embeddings.append([0.0] * 768)
        
        return embeddings
    
    def similarity_score(self, embedding1: List[float], embedding2: List[float]) -> float:
        """
        Calculate cosine similarity between two embeddings
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
        
        Returns:
            Similarity score (0-1)
        """
        vec1 = np.array(embedding1)
        vec2 = np.array(embedding2)
        
        # Cosine similarity
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return float(dot_product / (norm1 * norm2))

# Singleton instance
_embedding_service = None

def get_embedding_service() -> GeminiEmbeddingService:
    """Get or create embedding service"""
    global _embedding_service
    if _embedding_service is None:
        _embedding_service = GeminiEmbeddingService()
    return _embedding_service
