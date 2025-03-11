# AI Chatbot with RAG

## Functionality

The application provides the following key features:

### Chat Interface
- Interactive chat interface with streaming responses
- System prompt customization to define chatbot behavior
- Chat history preservation and management
- Ability to create new chat sessions
- Option to stop response generation mid-stream

### RAG (Retrieval-Augmented Generation)
- Document upload and management through ChromaDB vector database
- Automatic document chunking with customizable size and overlap
- Semantic search across uploaded documents

### Document Management
- Support for multiple document formats
- Document metadata tracking
- Document-chat association

### User Experience
- Real-time response streaming
- Chat history navigation
- Document management interface
- Customizable model settings

## Prerequisites

- Python 3.10+
- Required packages (see requirements.txt)
- Docker
- Ollama server

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## NLTK Setup

```bash
python setup_nltk.py
```

## Run the application  

```bash
streamlit run app.py
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/TuringCollegeSubmissions/hharch-AE.2.5.git
cd hharch-AE.1.4
```

2. Create and activate a virtual environment:
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Docker Compose

1. Start the Docker service:
```bash
docker compose up
```

