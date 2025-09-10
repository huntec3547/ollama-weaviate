# ollama-weaviate
RAG Service with Weaviate and ollama
> **Intelligent Question-Answering System with Retrieval-Augmented Generation**

A FastAPI-based microservice that processes research articles about Ian Campbell's genetic mutation studies and provides AI-powered question answering using OpenAI's GPT models and Weaviate vector database.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688.svg?style=flat&logo=FastAPI)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?style=flat&logo=python)](https://python.org)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5-412991.svg?style=flat)](https://openai.com)
[![Weaviate](https://img.shields.io/badge/Weaviate-Vector_DB-00C9A7.svg?style=flat)](https://weaviate.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=flat)](LICENSE)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Development](#development)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## 🎯 Overview

This RAG (Retrieval-Augmented Generation) microservice automatically processes research articles from PubMed, creates vector embeddings, and provides an intelligent Q&A interface. The system focuses on Ian Campbell's research in genetic mutations, somatic mosaicism, and genomic disorders.

### Key Capabilities

- **Automated Data Ingestion**: Downloads and processes research articles from configured URLs
- **Intelligent Chunking**: Splits documents into optimal segments for vector storage
- **Vector Search**: Uses Weaviate for similarity-based context retrieval
- **AI-Powered Answers**: Generates responses using OpenAI's GPT-3.5-turbo model
- **RESTful API**: Clean, documented API interface with automatic OpenAPI documentation

---

## ✨ Features

- 🚀 **FastAPI Framework**: High-performance async API with automatic documentation
- 🦜 **LangChain Integration**: Advanced document processing and retrieval chains
- 🗄️ **Vector Database**: Weaviate for efficient similarity search
- 🤖 **OpenAI Integration**: GPT-3.5-turbo for text generation and embeddings
- 🌐 **Web Scraping**: Automated article extraction from research URLs
- 📊 **Health Monitoring**: System health checks and status endpoints
- 🔍 **Comprehensive Logging**: Detailed logging for debugging and monitoring
- 📝 **Type Safety**: Full Pydantic model validation for requests/responses
- 🐳 **Docker Ready**: Easy containerization and deployment

---

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FastAPI App   │────│   RAG Manager   │────│   RAG Chain     │
│   (main.py)     │    │   (routes.py)   │    │ (rag_chain.py)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Models   │    │   RAG Worker    │    │   OpenAI API    │
│   (models.py)   │    │(rag_worker.py)  │    │  GPT-3.5-turbo  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Utilities     │    │  Weaviate DB    │    │   PubMed URLs   │
│ (loader, utils) │    │   Port: 8080    │    │ (config.json)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Data Flow

1. **Ingestion** → Download articles from PubMed URLs
2. **Processing** → Clean and chunk text into 100-character segments
3. **Embedding** → Generate vector embeddings using OpenAI
4. **Storage** → Store vectors in Weaviate database
5. **Retrieval** → Query-time similarity search for relevant context
6. **Generation** → Use GPT-3.5-turbo to generate answers

---

## 📋 Prerequisites

- **Python 3.8+**
- **Docker** (for Weaviate database)
- **OpenAI API Key**
- **Git**

### System Requirements

- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space
- **Network**: Internet connection for API calls and data download

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/rag-microservice.git
cd rag-microservice
```

### 2. Create Virtual Environment

```bash
# Using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Or using conda
conda create -n rag-microservice python=3.9
conda activate rag-microservice
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Start Weaviate Database

```bash
# Using Docker (recommended)
docker run -d \
  -p 8080:8080 \
  -e QUERY_DEFAULTS_LIMIT=25 \
  -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true \
  -e PERSISTENCE_DATA_PATH='/var/lib/weaviate' \
  --name weaviate \
  weaviate/weaviate:latest

# Or using Docker Compose
docker-compose up -d weaviate
```

### 5. Set Environment Variables

Create a `.env` file in the project root:

```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Weaviate Configuration (optional)
WEAVIATE_URL=http://localhost:8080

# Application Configuration (optional)
DEBUG=true
LOG_LEVEL=INFO
```

---

## ⚙️ Configuration

### Main Configuration File

Edit `app/config/config.json`:

```json
{
  "source_urls": [
    "https://pubmed.ncbi.nlm.nih.gov/25242496/",
    "https://pubmed.ncbi.nlm.nih.gov/25087610/",
    "https://pubmed.ncbi.nlm.nih.gov/25910407/"
  ],
  "filename": "ian_campbell.txt",
  "tenant": "ian_campbell"
}
```

### Configuration Options

| Parameter | Description | Default |
|-----------|-------------|---------|
| `source_urls` | List of PubMed article URLs to process | See config.json |
| `filename` | Output filename for processed data | `ian_campbell.txt` |
| `tenant` | Weaviate tenant identifier | `ian_campbell` |
| `chunk_size` | Text chunk size for processing | `100` characters |
| `chunk_overlap` | Overlap between chunks | `0` characters |

---

## 🏃‍♂️ Usage

### 1. Start the Application

```bash
# Development mode with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 2. Access the API

- **API Documentation**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/rag/healthCheck
- **Root Endpoint**: http://localhost:8000/

### 3. Make API Calls

#### Health Check

```bash
curl -X GET "http://localhost:8000/rag/healthCheck"
```

#### Ask RAG Question

```bash
curl -X POST "http://localhost:8000/rag/askrag" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are Ian Campbell'\''s main research areas?",
    "context": "genetic mutations and genomic disorders"
  }'
```

#### Using Python Requests

```python
import requests

# Health check
response = requests.get("http://localhost:8000/rag/healthCheck")
print(response.json())

# Ask a question
payload = {
    "question": "What is somatic mosaicism?",
    "context": "genetic research"
}
response = requests.post("http://localhost:8000/rag/askrag", json=payload)
print(response.json())
```

---

## 📚 API Documentation

### Endpoints Overview

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| `GET` | `/` | Root endpoint | None | Welcome message |
| `GET` | `/rag/healthCheck` | Health status | None | `HealthStatus` |
| `POST` | `/rag/askrag` | Process RAG query | `RagRequest` | `RagResponse` |
| `GET` | `/docs` | Swagger UI | None | Interactive docs |
| `GET` | `/redoc` | ReDoc UI | None | Alternative docs |

### Data Models

#### RagRequest

```python
{
  "question": "string",  # Required: User's question
  "context": "string"    # Required: Additional context
}
```

#### RagResponse

```python
{
  "question": "string",  # Original question
  "context": "string",   # Provided context
  "answer": "string"     # AI-generated answer
}
```

#### HealthStatus

```python
{
  "status": "string",              # Service status
  "timestamp": "datetime",         # Current timestamp
  "version": "string",            # API version
  "external_services": {          # External service status
    "openai": "online",
    "weaviate": "online"
  }
}
```

### Response Codes

- **200**: Success
- **400**: Bad Request (validation error)
- **401**: Unauthorized (invalid API key)
- **404**: Not Found
- **422**: Unprocessable Entity (validation failed)
- **500**: Internal Server Error
- **503**: Service Unavailable (external service down)

---

## 📁 Project Structure

```
rag-microservice/
├── 📄 main.py                    # FastAPI application entry point
├── 📄 models.py                  # Pydantic data models
├── 📄 requirements.txt           # Python dependencies
├── 📄 .env.example              # Environment variables template
├── 📄 docker-compose.yml        # Docker services configuration
├── 📄 Dockerfile               # Container configuration
├── 📄 README.md                # This file
├── 📄 LICENSE                  # MIT License
├── 📁 rag/                     # Main application package
│   ├── 📄 __init__.py
│   ├── 📄 routes.py            # API endpoints and RAG manager
│   └── 📁 tools/               # RAG processing tools
│       ├── 📄 __init__.py
│       ├── 📄 rag_chain.py     # LangChain RAG implementation
│       └── 📄 rag_worker.py    # Document processing worker
├── 📁 util/                    # Utility modules
│   ├── 📄 __init__.py
│   ├── 📄 loader.py            # Document loading utilities
│   └── 📄 rag_util.py          # Helper functions
├── 📁 app/                     # Application configuration
│   └── 📁 config/
│       └── 📄 config.json      # Application settings
├── 📁 data/                    # Data storage
│   └── 📄 ian_campbell.txt     # Processed research articles
├── 📁 tests/                   # Test suite
│   ├── 📄 test_api.py
│   ├── 📄 test_rag_chain.py
│   └── 📄 test_utils.py
└── 📁 docs/                    # Additional documentation
    ├── 📄 API.md               # Detailed API documentation
    ├── 📄 DEPLOYMENT.md        # Deployment guide
    └── 📄 ARCHITECTURE.md      # Architecture documentation
```

---

## 🛠️ Development

### Setting Up Development Environment

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run tests
pytest

# Run tests with coverage
pytest --cov=rag --cov-report=html

# Format code
black .
isort .

# Lint code
flake8
mypy .
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_api.py

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=rag --cov-report=term-missing
```

### Code Quality Tools

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking
- **pre-commit**: Git hooks for code quality

### Environment Variables for Development

```bash
# .env file for development
OPENAI_API_KEY=your_development_key
DEBUG=true
LOG_LEVEL=DEBUG
WEAVIATE_URL=http://localhost:8080
```

---

## 🐳 Deployment

### Docker Deployment

#### Build and Run with Docker

```bash
# Build the image
docker build -t rag-microservice .

# Run the container
docker run -d \
  --name rag-app \
  -p 8000:8000 \
  -e OPENAI_API_KEY=your_api_key \
  rag-microservice
```

#### Using Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  weaviate:
    image: weaviate/weaviate:latest
    ports:
      - "8080:8080"
    environment:
      - QUERY_DEFAULTS_LIMIT=25
      - AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true
      - PERSISTENCE_DATA_PATH=/var/lib/weaviate
    volumes:
      - weaviate_data:/var/lib/weaviate

  rag-app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - WEAVIATE_URL=http://weaviate:8080
    depends_on:
      - weaviate
    volumes:
      - ./data:/app/data

volumes:
  weaviate_data:
```

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Cloud Deployment

#### AWS ECS

```bash
# Build and push to ECR
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin <account>.dkr.ecr.us-west-2.amazonaws.com
docker build -t rag-microservice .
docker tag rag-microservice:latest <account>.dkr.ecr.us-west-2.amazonaws.com/rag-microservice:latest
docker push <account>.dkr.ecr.us-west-2.amazonaws.com/rag-microservice:latest
```

#### Kubernetes

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rag-microservice
spec:
  replicas: 3
  selector:
    matchLabels:
      app: rag-microservice
  template:
    metadata:
      labels:
        app: rag-microservice
    spec:
      containers:
      - name: rag-app
        image: rag-microservice:latest
        ports:
        - containerPort: 8000
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: openai-secret
              key: api-key
```

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Quick Start for Contributors

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Add tests** for new functionality
5. **Run the test suite**: `pytest`
6. **Commit your changes**: `git commit -m 'Add amazing feature'`
7. **Push to the branch**: `git push origin feature/amazing-feature`
8. **Open a Pull Request**

### Development Guidelines

- Follow [PEP 8](https://pep8.org/) style guidelines
- Write comprehensive tests for new features
- Update documentation for API changes
- Use meaningful commit messages
- Ensure all tests pass before submitting PR

---

## 🐛 Troubleshooting

### Common Issues

#### Weaviate Connection Error

```bash
# Error: Connection to Weaviate failed
# Solution: Ensure Weaviate is running
docker ps | grep weaviate
docker run -d -p 8080:8080 weaviate/weaviate:latest
```

#### OpenAI API Errors

```bash
# Error: OpenAI API authentication failed
# Solution: Check your API key
export OPENAI_API_KEY="your-valid-api-key"
```

#### Import Errors

```bash
# Error: ModuleNotFoundError
# Solution: Ensure you're in the right directory and virtual environment
cd rag-microservice
source venv/bin/activate
pip install -r requirements.txt
```

#### Port Already in Use

```bash
# Error: Port 8000 already in use
# Solution: Kill process or use different port
lsof -ti:8000 | xargs kill -9
# Or run on different port
uvicorn main:app --port 8001
```

### Debug Mode

Enable debug mode for detailed error information:

```bash
# Set environment variable
export DEBUG=true

# Or in .env file
DEBUG=true
LOG_LEVEL=DEBUG
```

### Health Check Endpoint

Use the health check endpoint to diagnose issues:

```bash
curl http://localhost:8000/rag/healthCheck
```

### Logs

Check application logs for detailed error information:

```bash
# View logs in development
uvicorn main:app --log-level debug

# View Docker logs
docker logs rag-app

# View Docker Compose logs
docker-compose logs -f rag-app
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 RAG Microservice

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 🙏 Acknowledgments

- **FastAPI** - The web framework that made this API a joy to build
- **LangChain** - For excellent RAG and document processing capabilities
- **Weaviate** - For providing a powerful vector database solution
- **OpenAI** - For GPT models and embedding services
- **Ian Campbell** - For the research that inspired this project

---

## 📞 Support

- **Documentation**: Check the `/docs` endpoint when running the service
- **Issues**: Report bugs and request features via GitHub Issues
- **Discussions**: Join our GitHub Discussions for questions and ideas

---

## 🔗 Links

- **Live Demo**: [https://rag-microservice-demo.com](https://rag-microservice-demo.com)
- **API Documentation**: [https://rag-microservice-demo.com/docs](https://rag-microservice-demo.com/docs)
- **Docker Hub**: [https://hub.docker.com/r/username/rag-microservice](https://hub.docker.com/r/username/rag-microservice)

---

<div align="center">

**Built with ❤️ by the RAG Microservice Team**

[![FastAPI](https://img.shields.io/badge/FastAPI-009688.svg?style=for-the-badge&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3776AB.svg?style=for-the-badge&logo=Python&logoColor=white)](https://python.org)
[![OpenAI](https://img.shields.io/badge/OpenAI-412991.svg?style=for-the-badge&logo=OpenAI&logoColor=white)](https://openai.com)
[![Docker](https://img.shields.io/badge/Docker-2496ED.svg?style=for-the-badge&logo=Docker&logoColor=white)](https://docker.com)

⭐ **Star this repo if you found it helpful!** ⭐

</div>
