"""
Demo script: Generate embeddings for sample books and test semantic search
"""

import os
from dotenv import load_dotenv
from embedd.embedding_service import get_embedding_service
from embedd.vector_db import init_db, get_db_session, BookChunkEmbedding
from embedd.search_service import get_search_service

load_dotenv()

# Sample books database
SAMPLE_BOOKS = [
    {
        "book_id": 1,
        "title": "The River and the Source",
        "author": "Margaret Ogola",
        "category": "Fiction",
        "tags": ["Kenya", "Women", "History", "Literature"],
        "description": """
        The River and the Source is an epic tale spanning four generations of Kenyan women.
        It traces the journey of Akosua, from her childhood in pre-colonial Kenya through
        the colonial period and into modern times. The novel explores themes of femininity,
        education, tradition, and social change in African society. Through the lives of
        mothers and daughters, Ogola weaves a powerful narrative about the strength and
        resilience of African women facing colonial oppression and cultural transformation.
        """
    },
    {
        "book_id": 2,
        "title": "Half of a Yellow Sun",
        "author": "Chimamanda Ngozi Adichie",
        "category": "Fiction",
        "tags": ["Nigeria", "War", "Literature", "History"],
        "description": """
        Half of a Yellow Sun is set during the Nigerian-Biafran War and follows the lives
        of three main characters whose destinies become intertwined. The novel explores love,
        identity, and the devastating impact of war on ordinary people. Adichie's powerful
        prose captures the complexity of a nation divided and the human cost of conflict.
        This masterpiece of African literature won numerous awards and has become essential
        reading for understanding modern Nigerian history and culture.
        """
    },
    {
        "book_id": 3,
        "title": "Things Fall Apart",
        "author": "Chinua Achebe",
        "category": "Fiction",
        "tags": ["Nigeria", "Colonial", "African Literature", "Classics"],
        "description": """
        Things Fall Apart is a seminal African novel that tells the story of Okonkwo,
        a respected leader in a pre-colonial Nigerian village. The narrative follows his
        life before, during, and after the arrival of European colonizers. Achebe's novel
        provides a powerful counter-narrative to Western depictions of African society,
        showing the complexity and sophistication of Igbo culture. The title reflects the
        collapse of traditional society as colonialism disrupts established ways of life.
        """
    },
    {
        "book_id": 4,
        "title": "So Long a Letter",
        "author": "Mariama Bâ",
        "category": "Fiction",
        "tags": ["Senegal", "Women", "Marriage", "African Literature"],
        "description": """
        So Long a Letter is written as a letter from Ramatoulaye to her friend Aissatou
        and explores the experience of two Senegalese women navigating marriage, motherhood,
        and widowhood. The novel examines the tension between tradition and modernity,
        examining polygamy and women's roles in African society. Through intimate prose,
        Bâ reveals the inner thoughts and struggles of women confronting patriarchal norms.
        This slim but powerful book has become iconic in African women's literature.
        """
    },
    {
        "book_id": 5,
        "title": "Nervous Conditions",
        "author": "Tsitsi Dangarembga",
        "category": "Fiction",
        "tags": ["Zimbabwe", "Colonial", "Women", "Education"],
        "description": """
        Nervous Conditions follows Tambudzai and her cousin Nyasha as they navigate
        education, colonialism, and gender roles in Zimbabwe. The novel explores how
        colonialism and patriarchy intersect to marginalize African women. Through the
        coming-of-age story of its young protagonist, Dangarembga examines the psychological
        and social impact of colonial education and Western values on African identity.
        """
    },
    {
        "book_id": 6,
        "title": "The Famished Road",
        "author": "Ben Okri",
        "category": "Fantasy/Literature",
        "tags": ["Nigeria", "Magic Realism", "Spirituality"],
        "description": """
        The Famished Road is a magical realist novel set in Nigeria that weaves together
        the spiritual and material worlds. Following Azaro, a spirit-child, the narrative
        explores African mythology, philosophy, and contemporary life. Okri's lyrical prose
        celebrates the richness of African cultural traditions while critiquing post-colonial
        society. The novel won the Booker Prize and stands as a testament to the power of
        African imagination and storytelling.
        """
    },
    {
        "book_id": 7,
        "title": "Purple Hibiscus",
        "author": "Chimamanda Ngozi Adichie",
        "category": "Fiction",
        "tags": ["Nigeria", "Family", "Religion", "Coming of Age"],
        "description": """
        Purple Hibiscus tells the story of Kambili, a fifteen-year-old girl from Nigeria
        whose family's deep Catholic faith masks darker realities. The novel explores themes
        of religious extremism, domestic violence, and the search for identity. Through
        Kambili's journey, Adichie examines how traditions can be distorted to justify harm,
        and how literature and art provide paths to freedom and self-discovery.
        """
    }
]

def embed_sample_books():
    """Generate embeddings for sample books"""
    print("=" * 60)
    print("📚 Embedding Sample Books with Gemini 2.5 Flash")
    print("=" * 60)
    
    # Initialize database
    print("\n1️⃣ Initializing database...")
    init_db()
    
    # Get services
    embedding_service = get_embedding_service()
    db = get_db_session()
    
    # Embed each book
    print("\n2️⃣ Generating embeddings...\n")
    
    for book in SAMPLE_BOOKS:
        try:
            # Generate embeddings
            results = embedding_service.embed_book(
                book_id=book["book_id"],
                title=book["title"],
                author=book["author"],
                description=book["description"],
                category=book["category"],
                tags=book["tags"]
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
            print(f"✅ Indexed: {book['title']} ({len(results)} chunks)\n")
        
        except Exception as e:
            print(f"❌ Error embedding {book['title']}: {str(e)}\n")
            db.rollback()
    
    db.close()
    print("=" * 60)
    print("✅ All books embedded successfully!")
    print("=" * 60)

def test_search():
    """Test semantic search"""
    print("\n" + "=" * 60)
    print("🔍 Testing Semantic Search")
    print("=" * 60)
    
    search_service = get_search_service()
    db = get_db_session()
    
    test_queries = [
        "books about Kenyan women leaders",
        "African literature classics",
        "novels about war and conflict",
        "stories of female resilience",
        "colonial history and its impact"
    ]
    
    for query in test_queries:
        print(f"\n📌 Query: '{query}'")
        print("-" * 60)
        
        results = search_service.search(query, limit=3, db=db)
        
        if results:
            for i, (title, score, snippet) in enumerate(results, 1):
                print(f"{i}. {title}")
                print(f"   Score: {score:.2%}")
                print(f"   Snippet: {snippet[:100]}...\n")
        else:
            print("No results found\n")
    
    db.close()

def test_recommendations():
    """Test recommendation system"""
    print("\n" + "=" * 60)
    print("🎯 Testing Recommendations")
    print("=" * 60)
    
    search_service = get_search_service()
    db = get_db_session()
    
    # Test recommendation with search history
    print("\n📚 Personalized Recommendations")
    print("-" * 60)
    
    results = search_service.get_recommendations(
        user_phone="+254712345678",
        search_history=["women writers", "African history"],
        education_level="secondary",
        interests=["literature", "history"],
        limit=5,
        db=db
    )
    
    for i, (title, reason, score) in enumerate(results, 1):
        print(f"{i}. {title}")
        print(f"   Reason: {reason}")
        print(f"   Score: {score:.2%}\n")
    
    db.close()

if __name__ == "__main__":
    # Generate embeddings
    embed_sample_books()
    
    # Test search
    test_search()
    
    # Test recommendations
    test_recommendations()
    
    print("\n✅ Demo complete!")
