# 📚 Maktaba Rural - Library Access for Rural Communities (Updated)

Maktaba Rural is a USSD/SMS-first library system designed for communities with limited internet access. It combines classic catalogue search with optional AI-powered semantic search for richer discovery.

## ✨ What this project does

- **Text-first catalogue search** backed by a reference file for fast lookups.
- **Optional semantic search** using Gemini embeddings for natural-language queries.
- **API layer** with search and recommendation endpoints.
- **Ingestion utilities** for managing catalogue data.

## � How it Works

### Architecture Overview

```
┌─────────────────┐
│   User Query    │ (via API, USSD, or SMS)
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│   Search Service                    │
│   (embedd/search_service.py)        │
└─────────────────────────────────────┘
         │
         ├──────────────────┬──────────────────┐
         ▼                  ▼                  ▼
┌──────────────┐   ┌─────────────┐   ┌──────────────┐
│ Text Search  │   │  Embeddings │   │  Catalogue   │
│  (Fast)      │   │  (Semantic) │   │  Reference   │
└──────────────┘   └─────────────┘   └──────────────┘
         │                  │                  │
         └──────────────────┴──────────────────┘
                            │
                            ▼
                    ┌───────────────┐
                    │    Results    │
                    └───────────────┘
```

### Search Flow

1. **Query Received**: User submits a search query (e.g., "Foundations of Economics")

2. **Fast Text Search** (Primary Path):
   - Loads [Ingestion/catalogue.txt](Ingestion/catalogue.txt) (pipe-delimited: `book|shelf|library|location`)
   - Performs case-insensitive matching on book title, library, shelf, and location
   - Returns instantly with book details including physical location
   - **No API calls needed** - works completely offline

3. **Semantic Search** (Fallback - Optional):
   - If text search fails and Gemini is configured:
     - Sends query to Gemini API for embedding generation (768-dim vector)
     - Queries PostgreSQL with pgvector for cosine similarity
     - Ranks results by semantic relevance
     - Returns top matches with relevance scores
   - Can be skipped with `SEARCH_SKIP_EMBEDDINGS=1`

4. **Result Formatting**:
   - Text matches: Book name, shelf, library, location
   - Semantic matches: Book name, relevance score, content snippet

### Data Flow Example

```
User searches: "Foundations of Economics"
    │
    ├─▶ Text Search checks catalogue.txt
    │   └─▶ MATCH FOUND ✓
    │       Book: Foundations of Economics
    │       Shelf: SH-ECO1
    │       Library: Main Campus Library
    │       Location: 1st Floor - Social Sciences
    │
    └─▶ (Semantic search skipped - text match succeeded)
```

### Key Components

1. **[embedd/search_service.py](embedd/search_service.py)**: Core search logic
   - `_load_reference_catalogue()`: Loads and caches catalogue.txt
   - `_text_search()`: Fast text matching (primary)
   - `search()`: Main entry point with fallback logic

2. **[embedd/search_api.py](embedd/search_api.py)**: REST API endpoints
   - `POST /search`: Search books
   - `POST /recommend`: Get personalized recommendations
   - `POST /embed-book`: Index new books with embeddings
   - `GET /stats`: View indexing statistics

3. **[Ingestion/catalogue.txt](Ingestion/catalogue.txt)**: Reference data
   - Simple pipe-delimited format
   - No database required
   - Instant lookups

4. **[embedd/embedding_service.py](embedd/embedding_service.py)**: Gemini integration
   - Generates 768-dimensional embeddings
   - Chunks large texts for better accuracy
   - Used only when text search fails

## �📁 Project structure

- [app/api/api.py](app/api/api.py): API endpoints (USSD/SMS integrations live here).
- [app/models/models.py](app/models/models.py): Data models.
- [embedd/search_api.py](embedd/search_api.py): FastAPI search service.
- [embedd/search_service.py](embedd/search_service.py): Search logic (text + embeddings).
- [embedd/embedding_service.py](embedd/embedding_service.py): Gemini embedding client.
- [embedd/vector_db.py](embedd/vector_db.py): PostgreSQL + pgvector schema.
- [Ingestion/catalogue.txt](Ingestion/catalogue.txt): Reference catalogue data for fast text search.
- [Ingestion/catalogue.py](Ingestion/catalogue.py): Catalogue utilities (list/search/export).

## ✅ Features

- **Fast text search** via [Ingestion/catalogue.txt](Ingestion/catalogue.txt).
- **Semantic search (optional)** using Gemini embeddings.
- **Search logs** for analytics.
- **Recommendations** based on search history and interests.

## 🔧 Requirements

- Python 3.8+
- PostgreSQL (for embeddings) + pgvector extension
- Gemini API key (optional, only for embeddings)
- Africa’s Talking account (for USSD/SMS integration if you use it)

## ⚙️ Environment variables

Create a .env file at the project root with the settings you need:

	# Gemini (optional, for embeddings)
	GEMINI_API_KEY=your_api_key_here

	# PostgreSQL for embeddings
	DATABASE_URL=postgresql://user:password@localhost:5432/maktaba_db

	# Africa's Talking (if using USSD/SMS)
	AT_USERNAME=sandbox
	AT_API_KEY=your_api_key_here
	AT_USSD_CODE=*384*1234#

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Africa's Talking Credentials
AT_USERNAME=sandbox
AT_API_KEY=your_api_key_here
AT_USSD_CODE=*384*1234#

