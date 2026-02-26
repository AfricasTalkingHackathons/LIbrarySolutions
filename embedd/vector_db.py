"""
Vector Database Schema and Operations

Using PostgreSQL with pgvector extension for storing and querying embeddings.
"""

import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime, JSON, Index
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import uuid

Base = declarative_base()

class BookChunkEmbedding(Base):
    """Store book text chunks and their embeddings"""
    __tablename__ = "book_chunk_embeddings"
    
    id = Column(Integer, primary_key=True, index=True)
    chunk_id = Column(String(255), unique=True, nullable=False, index=True)
    book_id = Column(Integer, nullable=False, index=True)
    title = Column(String(500), nullable=False)
    author = Column(String(300), nullable=False)
    category = Column(String(100), index=True)
    
    # Text and embedding
    chunk_text = Column(Text, nullable=False)
    embedding = Column(ARRAY(Float), nullable=False)  # Vector as array
    embedding_dim = Column(Integer, default=768)
    
    # Metadata
    chunk_index = Column(Integer)  # Which chunk in the book
    chunk_count = Column(Integer)  # Total chunks for this book
    meta_data = Column(JSON)  # Additional metadata (renamed from 'metadata' to avoid SQLAlchemy conflict)
    
    # Tracking
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<BookChunkEmbedding(chunk_id={self.chunk_id}, book_id={self.book_id})>"

class SearchLog(Base):
    """Log search queries for analytics and improvement"""
    __tablename__ = "search_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    query = Column(String(1000), nullable=False)
    query_embedding = Column(ARRAY(Float))
    results_count = Column(Integer, default=0)
    user_phone = Column(String(20), index=True)
    clicked_result = Column(Integer)  # Book ID of clicked result
    relevance_score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f"<SearchLog(query={self.query}, results={self.results_count})>"

class RecommendationLog(Base):
    """Track recommendation system performance"""
    __tablename__ = "recommendation_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_phone = Column(String(20), index=True)
    recommended_books = Column(ARRAY(Integer))  # List of book IDs
    reason = Column(String(200))  # Why these books were recommended
    engagement = Column(String(50))  # clicked, ignored, reserved
    created_at = Column(DateTime, default=datetime.utcnow)

# Database initialization
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@localhost:5432/maktaba_db"
)

# Add connection pooling and timeout settings
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verify connections before using
    pool_recycle=3600,   # Recycle connections after 1 hour
    connect_args={
        "connect_timeout": 10,
        "options": "-c statement_timeout=30000"  # 30 second query timeout
    }
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize database with pgvector extension"""
    # Enable pgvector extension
    with engine.connect() as connection:
        try:
            connection.execute("CREATE EXTENSION IF NOT EXISTS vector")
            connection.commit()
            print("✓ pgvector extension enabled")
        except Exception as e:
            print(f"Note: {str(e)}")
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created")

def get_db_session():
    """Get database session"""
    return SessionLocal()
