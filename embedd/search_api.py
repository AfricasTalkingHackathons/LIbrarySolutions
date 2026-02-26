"""
FastAPI endpoints for semantic search and recommendations
"""

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
from embedd.embedding_service import get_embedding_service
from embedd.search_service import get_search_service
from embedd.vector_db import get_db_session, BookChunkEmbedding

app = FastAPI(title="Maktaba AI Search", version="1.0.0")

# ============ Models ============

class SearchRequest(BaseModel):
    query: str
    limit: int = 10
    threshold: float = 0.3

class SearchResponse(BaseModel):
    title: str
    relevance_score: float
    snippet: str

class RecommendationRequest(BaseModel):
    user_phone: str
    search_history: Optional[List[str]] = None
    education_level: Optional[str] = None
    interests: Optional[List[str]] = None
    limit: int = 5

class RecommendationResponse(BaseModel):
    title: str
    reason: str
    score: float

class BookEmbeddingRequest(BaseModel):
    book_id: int
    title: str
    author: str
    description: str
    category: Optional[str] = None
    tags: Optional[List[str]] = None

# ============ Endpoints ============

@app.get("/")
async def root():
    """Health check"""
    return {
        "service": "Maktaba AI Search API",
        "version": "1.0.0",
        "endpoints": [
            "/search - Semantic search",
            "/recommend - Get recommendations",
            "/embed-book - Index a book",
            "/stats - Search statistics"
        ]
    }

@app.post("/search", response_model=List[SearchResponse])
async def search(
    request: SearchRequest,
    db: Session = Depends(get_db_session)
):
    """
    Semantic search endpoint
    
    Example:
    ```json
    {
        "query": "books about Kenyan women leaders",
        "limit": 5,
        "threshold": 0.3
    }
    ```
    
    Returns books ranked by relevance to your natural language query.
    """
    search_service = get_search_service()
    results = search_service.search(
        query=request.query,
        limit=request.limit,
        similarity_threshold=request.threshold,
        db=db
    )
    
    return [
        SearchResponse(title=title, relevance_score=score, snippet=snippet)
        for title, score, snippet in results
    ]

@app.post("/recommend", response_model=List[RecommendationResponse])
async def recommend(
    request: RecommendationRequest,
    db: Session = Depends(get_db_session)
):
    """
    Get personalized book recommendations
    
    Example:
    ```json
    {
        "user_phone": "+254712345678",
        "search_history": ["African history", "women writers"],
        "education_level": "secondary",
        "interests": ["literature", "history"],
        "limit": 5
    }
    ```
    
    Returns recommended books based on:
    - Search history
    - Education level
    - Personal interests
    """
    search_service = get_search_service()
    results = search_service.get_recommendations(
        user_phone=request.user_phone,
        search_history=request.search_history,
        education_level=request.education_level,
        interests=request.interests,
        limit=request.limit,
        db=db
    )
    
    return [
        RecommendationResponse(title=title, reason=reason, score=score)
        for title, reason, score in results
    ]

@app.post("/embed-book")
async def embed_book(
    request: BookEmbeddingRequest,
    db: Session = Depends(get_db_session)
):
    """
    Index a book by generating and storing embeddings
    
    Example:
    ```json
    {
        "book_id": 1,
        "title": "The River and the Source",
        "author": "Margaret Ogola",
        "description": "Epic tale of four generations of Kenyan women...",
        "category": "Fiction",
        "tags": ["kenya", "women", "history", "literature"]
    }
    ```
    
    This endpoint:
    1. Chunks the text
    2. Generates embeddings for each chunk
    3. Stores in vector database
    """
    try:
        embedding_service = get_embedding_service()
        
        # Generate embeddings
        results = embedding_service.embed_book(
            book_id=request.book_id,
            title=request.title,
            author=request.author,
            description=request.description,
            category=request.category,
            tags=request.tags or []
        )
        
        # Store in database
        for result in results:
            embedding = BookChunkEmbedding(
                chunk_id=result.chunk_id,
                book_id=result.metadata["book_id"],
                title=result.metadata["title"],
                author=result.metadata["author"],
                category=result.metadata.get("category"),
                chunk_text=result.text,
                embedding=result.embedding,
                chunk_index=result.metadata.get("chunk_index"),
                chunk_count=result.metadata.get("chunk_count"),
                meta_data=result.metadata
            )
            db.add(embedding)
        
        db.commit()
        
        return {
            "success": True,
            "book_id": request.book_id,
            "title": request.title,
            "chunks_embedded": len(results),
            "message": f"Successfully indexed '{request.title}' with {len(results)} chunks"
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
async def stats(db: Session = Depends(get_db_session)):
    """
    Get search statistics and system status
    """
    try:
        books_count = db.query(BookChunkEmbedding.book_id).distinct().count()
        chunks_count = db.query(BookChunkEmbedding).count()
        
        return {
            "books_indexed": books_count,
            "chunks_stored": chunks_count,
            "average_chunks_per_book": chunks_count / max(books_count, 1),
            "embedding_dimension": 768,
            "model": "Gemini 2.5 Flash"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    """Health check"""
    return {
        "status": "healthy",
        "service": "Maktaba AI Search"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
