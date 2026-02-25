# 📚 Maktaba Rural - Library Access for Rural Communities

A USSD/SMS-based library system with AI-powered semantic search, enabling rural communities to access books via feature phones.

## 🚀 Features

- **AI Semantic Search**: Natural language book search using embeddings (not just keyword matching)
- **USSD Interface**: Access via `*123#` style codes - no internet required
- **SMS Notifications**: Book summaries, reservation confirmations, and reminders
- **Africa's Talking Integration**: USSD, SMS, and WhatsApp APIs
- **Book Reservations**: Browse, search, and reserve books remotely

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL database
- Africa's Talking account ([Sign up here](https://africastalking.com))

## 🔧 Installation

### 1. Clone and Setup Virtual Environment

```bash
cd /home/clencyc/Dev/Library
python3 -m venv venv
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate  # On Windows
```

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

