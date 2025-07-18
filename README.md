# 🏋️ GymPro RAG Chatbot

A comprehensive gym and fitness information chatbot powered by RAG (Retrieval-Augmented Generation) technology, built with FastAPI backend and Streamlit frontend.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [File Structure](#file-structure)
- [Prerequisites](#prerequisites)
- [Setup & Installation](#setup--installation)
- [Running the Application](#running-the-application)
- [Docker Deployment](#docker-deployment)
- [API Documentation](#api-documentation)
- [Usage Examples](#usage-examples)
- [Configuration](#configuration)
- [Development](#development)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## 🎯 Overview

GymPro is an AI-powered chatbot that provides expert advice on fitness, exercise techniques, workout routines, nutrition, and gym-related topics. It uses RAG technology to provide accurate, context-aware responses based on a comprehensive gym knowledge base.

### Key Technologies
- **Backend**: FastAPI with Python
- **Frontend**: Streamlit
- **AI/ML**: LangChain, Google Generative AI (Gemini)
- **Vector Store**: FAISS
- **Embeddings**: Google Generative AI Embeddings
- **Deployment**: Docker & Docker Compose

## ✨ Features

### 🤖 AI Capabilities
- **RAG-Powered Responses**: Context-aware answers using vector similarity search
- **Fitness Expertise**: Specialized knowledge in gym, exercise, and nutrition
- **Content Filtering**: Ensures responses stay within fitness/health domains
- **Source Attribution**: Shows document sources for transparency

### 🎨 User Interface
- **Modern Streamlit Interface**: Clean, responsive chat interface
- **Real-time Health Monitoring**: Live API status and system health
- **Message History**: Persistent chat sessions
- **Mobile-Friendly**: Responsive design for all devices

### 🔧 Technical Features
- **Microservices Architecture**: Separate backend and frontend services
- **Health Checks**: Comprehensive monitoring and status endpoints
- **CORS Support**: Cross-origin resource sharing enabled
- **Error Handling**: Robust error management and user feedback
- **Hot Reload**: Development-friendly auto-reload

## 🏗️ Architecture

```
┌─────────────────┐    HTTP/REST    ┌─────────────────┐
│                 │ ◄─────────────► │                 │
│  Streamlit      │                 │  FastAPI        │
│  Frontend       │                 │  Backend        │
│  (Port 8501)    │                 │  (Port 8001)    │
│                 │                 │                 │
└─────────────────┘                 └─────────────────┘
                                              │
                                              ▼
                                    ┌─────────────────┐
                                    │                 │
                                    │  RAG System     │
                                    │  • FAISS        │
                                    │  • LangChain    │
                                    │  • Google AI    │
                                    │                 │
                                    └─────────────────┘
```

## 📁 File Structure

```
gym_pro/
├── 📄 README.md                     # This comprehensive guide
├── 📄 .env                          # Environment variables (create from .env.example)
├── 📄 .env.example                  # Environment template
├── 📄 .gitignore                    # Git ignore rules
├── 📄 requirements.txt              # Python dependencies
├── 📄 main.py                       # Application entry point
├── 📄 streamlit_app.py              # Streamlit frontend application
├── 📄 docker-compose.yml            # Multi-service Docker configuration
├── 📄 Dockerfile                    # Backend Docker image
├── 📄 Dockerfile.streamlit          # Frontend Docker image
├── 📄 Dockerfile.prod               # Production Docker image
├── 📄 .dockerignore                 # Docker ignore rules
│
├── 🗂️ app/                          # Main application package
│   ├── 📄 __init__.py               # Package initializer
│   ├── 📄 main.py                   # FastAPI application factory
│   │
│   ├── 🗂️ core/                     # Core configuration
│   │   ├── 📄 __init__.py
│   │   └── 📄 config.py             # Settings and configuration
│   │
│   ├── 🗂️ api/                      # API endpoints
│   │   ├── 📄 __init__.py
│   │   ├── 📄 chat.py               # Chat endpoint
│   │   └── 📄 health.py             # Health check endpoints
│   │
│   ├── 🗂️ services/                 # Business logic
│   │   ├── 📄 __init__.py
│   │   └── 📄 rag_service.py        # RAG system implementation
│   │
│   ├── 🗂️ models/                   # Data models
│   │   ├── 📄 __init__.py
│   │   └── 📄 schemas.py            # Pydantic models
│   │
│   └── 🗂️ utils/                    # Utility functions
│       ├── 📄 __init__.py
│       └── 📄 content_filter.py     # Content filtering logic
│
├── 🗂️ data/                         # Knowledge base
│   └── 📄 gym_data.txt              # Gym and fitness information
│
├── 🗂️ static/                       # Static files
│   └── 📄 chat_ui.html              # HTML chat interface (legacy)
│
├── 🗂️ tests/                        # Test suite
│   ├── 📄 test_api.py               # API endpoint tests
│   ├── 📄 test_chat.py              # Chat functionality tests
│   └── 📄 test_client.py            # Test client
│
├── 🗂️ logs/                         # Application logs (created at runtime)
├── 🗂️ venv/                         # Python virtual environment
│
├── 🛠️ setup.ps1                     # Windows PowerShell setup script
├── 🛠️ start.bat                     # Windows startup script
├── 🛠️ start_app.bat                 # Windows full-stack launcher
├── 🛠️ start_app.sh                  # Linux/Mac full-stack launcher
├── 🛠️ run_streamlit.bat             # Windows Streamlit launcher
├── 🛠️ run_streamlit.sh              # Linux/Mac Streamlit launcher
├── 🛠️ docker-run.bat                # Windows Docker launcher
├── 🛠️ docker-run.sh                 # Linux/Mac Docker launcher
│
└── 📄 API_DOCS.md                   # API documentation
```

## 📋 Prerequisites

### System Requirements
- **Python**: 3.11 or higher
- **Memory**: 4GB RAM minimum (8GB recommended)
- **Storage**: 2GB free space
- **OS**: Windows 10/11, macOS 10.14+, or Linux

### Required Accounts
- **Google AI Studio**: For Generative AI API access
  - Get your API key: https://makersuite.google.com/app/apikey

### Optional (for Docker)
- **Docker**: Latest version
- **Docker Compose**: Included with Docker Desktop

## 🚀 Setup & Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd gym_pro
```

### 2. Environment Setup

#### Windows (PowerShell)
```powershell
# Run the automated setup
.\setup.ps1
```

#### Manual Setup (All Platforms)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env
```

### 3. Configure Environment Variables

Edit `.env` file and add your Google API key:
```env
# Required
GOOGLE_API_KEY=your_actual_google_api_key_here

# Optional (with defaults)
APP_NAME=RAG Gym Chatbot
APP_VERSION=1.0.0
DEBUG=true
HOST=0.0.0.0
PORT=8001
TEMPERATURE=0.1
CHUNK_SIZE=1000
CHUNK_OVERLAP=100
SIMILARITY_SEARCH_K=3
```

## 🎮 Running the Application

### Option 1: Full Stack (Recommended)

#### Windows
```batch
start_app.bat
```

#### Linux/Mac
```bash
chmod +x start_app.sh
./start_app.sh
```

### Option 2: Individual Services

#### Backend Only
```bash
# Activate virtual environment first
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

python main.py
```

#### Frontend Only
```bash
# Activate virtual environment first
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

streamlit run streamlit_app.py
```

### Option 3: Docker Compose
```bash
docker-compose up --build
```

## 🐳 Docker Deployment

### Quick Start
```bash
# Build and run all services
docker-compose up --build

# Run in background
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Individual Service Builds
```bash
# Backend only
docker build -t gym-pro-api .

# Frontend only
docker build -f Dockerfile.streamlit -t gym-pro-frontend .

# Production build
docker build -f Dockerfile.prod -t gym-pro-api-prod .
```

### Docker Environment Variables
```yaml
# In docker-compose.yml
environment:
  - API_BASE_URL=http://gym-pro-api:8001
  - HOST=0.0.0.0
  - PORT=8001
  - DEBUG=false
```

## 🌐 Access Points

Once running, access the application at:

| Service | URL | Description |
|---------|-----|-------------|
| **🎨 Streamlit Frontend** | http://localhost:8501 | Main chat interface |
| **🔗 FastAPI Backend** | http://localhost:8001 | API service |
| **📚 API Documentation** | http://localhost:8001/docs | Interactive API docs |
| **💚 Health Check** | http://localhost:8001/health | Service health status |
| **📊 API Health** | http://localhost:8001/api/health | Detailed system status |

## 📖 API Documentation

### Chat Endpoint
```http
POST /chat
Content-Type: application/json

{
  "message": "How do I perform a proper deadlift?"
}
```

**Response:**
```json
{
  "response": "To perform a proper deadlift...",
  "sources": ["Source document excerpt 1...", "Source document excerpt 2..."],
  "message_type": "fitness_response"
}
```

### Health Endpoints
```http
GET /health                    # Basic health check
GET /api/health               # Detailed system status
```

## 💡 Usage Examples

### Fitness Questions You Can Ask

#### Exercise Techniques
- "How do I perform a proper deadlift?"
- "What's the correct form for squats?"
- "How to do bench press safely?"

#### Workout Routines
- "Give me a beginner chest workout"
- "What's a good full-body routine?"
- "How to structure a push-pull-legs split?"

#### Nutrition Advice
- "How much protein should I eat to build muscle?"
- "What are the best pre-workout foods?"
- "When should I take supplements?"

#### Equipment Usage
- "How to use a cable machine?"
- "What's the difference between dumbbells and barbells?"
- "Best home gym equipment for beginners?"

## ⚙️ Configuration

### Core Settings (`app/core/config.py`)
```python
# Model Configuration
GOOGLE_MODEL = "gemini-2.0-flash-exp"
EMBEDDING_MODEL = "models/embedding-001"
TEMPERATURE = 0.1

# RAG Configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100
SIMILARITY_SEARCH_K = 3

# File Paths
GYM_DATA_FILE = "data/gym_data.txt"
FAISS_INDEX_PATH = "data/faiss_index"
```

### Streamlit Configuration
The app includes custom theming and styling:
- Primary color: `#FF6B35` (Orange)
- Background: `#FFFFFF` (White)
- Text: Dark for high contrast
- Custom CSS for message styling

## 🛠️ Development

### Adding New Features

1. **New API Endpoints**: Add to `app/api/`
2. **Business Logic**: Add to `app/services/`
3. **Data Models**: Add to `app/models/schemas.py`
4. **Utilities**: Add to `app/utils/`

### Testing
```bash
# Install test dependencies
pip install pytest

# Run tests
python -m pytest tests/ -v

# Run specific test
python -m pytest tests/test_api.py -v
```

### Code Structure Best Practices
- Follow the modular architecture
- Use Pydantic models for data validation
- Include proper error handling
- Add logging for debugging
- Write tests for new features

## 🔧 Troubleshooting

### Common Issues

#### 1. Import Errors
```bash
# Ensure virtual environment is activated
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Verify Python path
python -c "import sys; print(sys.path)"
```

#### 2. API Key Issues
```bash
# Check if .env file exists and has correct key
cat .env | grep GOOGLE_API_KEY

# Test API key
python -c "from app.core.config import settings; print('API Key configured:', bool(settings.GOOGLE_API_KEY))"
```

#### 3. Port Already in Use
```bash
# Check what's using the port
netstat -ano | findstr :8001  # Windows
lsof -i :8001                 # Linux/Mac

# Kill process or change port in .env
```

#### 4. Docker Issues
```bash
# Clean Docker environment
docker-compose down
docker system prune -f
docker-compose up --build
```

#### 5. RAG System Initialization
```bash
# Check if data file exists
ls -la data/gym_data.txt

# Check logs for initialization errors
docker-compose logs gym-pro-api
```

### Logs and Debugging

#### Application Logs
- **Local Development**: Console output
- **Docker**: `docker-compose logs -f`
- **Files**: `logs/` directory (if configured)

#### Health Monitoring
- Visit `/health` endpoint for basic status
- Visit `/api/health` for detailed system information
- Streamlit sidebar shows real-time API status

## 📊 Monitoring & Health Checks

### Health Check Endpoints
- **Basic Health**: `GET /health`
- **Detailed Status**: `GET /api/health`
- **Streamlit Health**: `GET /_stcore/health`

### Docker Health Checks
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8001/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

### Monitoring Metrics
- RAG system initialization status
- Vector store loaded documents count
- API response times
- Error rates and types

## 🤝 Contributing

### Development Workflow
1. Fork the repository
2. Create a feature branch
3. Make changes following the code structure
4. Add tests for new functionality
5. Update documentation
6. Submit a pull request

### Code Standards
- Follow PEP 8 for Python code
- Use type hints where possible
- Include docstrings for functions and classes
- Write comprehensive tests
- Update README for new features

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support, please:
1. Check this README for common solutions
2. Review the troubleshooting section
3. Check the API documentation at `/docs`
4. Open an issue on the repository

## 🔄 Version History

- **v1.0.0**: Initial release with RAG system, FastAPI backend, and Streamlit frontend
- **v1.1.0**: Added Docker support and improved UI
- **v1.2.0**: Enhanced error handling and monitoring

---

Made with ❤️ by the GymPro team. Happy lifting! 🏋️‍♂️

## ✨ Features

- **🤖 RAG-powered responses** using FAISS vector store and Google Generative AI
- **🎯 Gym-focused content filtering** - only answers fitness-related questions
- **📊 Comprehensive knowledge base** covering exercises, nutrition, safety, and equipment
- **🚀 Professional FastAPI backend** with proper project structure
- **🎨 Beautiful web interface** for easy interaction
- **🔧 Robust error handling** with fallback responses
- **📈 Health monitoring** and system status endpoints

## 📁 Project Structure

```
gym_pro/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application factory
│   ├── api/                    # API endpoints
│   │   ├── __init__.py
│   │   ├── chat.py            # Chat endpoints
│   │   └── health.py          # Health & system endpoints
│   ├── core/                   # Core configuration
│   │   ├── __init__.py
│   │   └── config.py          # Application settings
│   ├── models/                 # Pydantic models
│   │   ├── __init__.py
│   │   └── schemas.py         # API schemas
│   ├── services/               # Business logic
│   │   ├── __init__.py
│   │   └── rag_service.py     # RAG implementation
│   └── utils/                  # Utility functions
│       ├── __init__.py
│       └── content_filter.py  # Content filtering
├── data/
│   └── gym_data.txt           # Gym knowledge base
├── static/
│   └── chat_ui.html           # Web interface
├── tests/
│   ├── test_api.py            # API tests
│   └── test_client.py         # Simple test client
├── main_new.py                # Application entry point
├── requirements.txt           # Dependencies
├── .env                       # Environment variables
└── README.md                  # This file
```

## 🚀 Quick Start

### 1. Environment Setup

```bash
# Clone or download the project
cd gym_pro

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\Activate.ps1
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file in the root directory:

```bash
# Google Generative AI API Key
GOOGLE_API_KEY="your_google_api_key_here"

# Application Settings
APP_NAME="GymPro RAG Chatbot"
APP_VERSION="1.0.0"
DEBUG=True
```

### 3. Run the Application

```bash
# Start the server
python main_new.py

# The API will be available at:
# http://localhost:8000
```

### 4. Access the Web Interface

Open your browser and go to:
```
http://localhost:8000/static/chat_ui.html
```

## 🧪 Testing

### Run API Tests
```bash
python tests/test_api.py
```

### Run Simple Tests
```bash
python tests/test_client.py
```

## 📡 API Endpoints

### Health Endpoints
- `GET /` - Basic health check
- `GET /health` - Detailed system status
- `POST /reset` - Reset and reinitialize RAG system

### Chat Endpoints
- `POST /chat` - Send messages to the chatbot

### Example API Usage

```python
import requests

# Chat with the bot
response = requests.post(
    "http://localhost:8000/chat",
    json={"message": "What's the best workout for beginners?"}
)

data = response.json()
print(data["response"])
```

## 🏗️ Architecture

### RAG System Components

1. **Document Loading**: Loads gym knowledge from `data/gym_data.txt`
2. **Text Splitting**: Chunks documents for optimal retrieval
3. **Embeddings**: Uses Google Generative AI embeddings
4. **Vector Store**: FAISS for efficient similarity search
5. **LLM**: Google Gemini-2.5-Flash for response generation
6. **Prompt Templates**: Structured prompts for consistent responses

### Content Filtering

- **Keyword-based filtering** ensures only gym/fitness questions are answered
- **Polite rejection** of off-topic questions with redirection
- **Fallback responses** when RAG system is unavailable

## 🔧 Configuration Options

All settings are managed in `app/core/config.py`:

```python
# Model Settings
GOOGLE_MODEL = "gemini-2.5-flash"
EMBEDDING_MODEL = "models/embedding-001"
TEMPERATURE = 0.3

# RAG Settings
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
SIMILARITY_SEARCH_K = 3
```

## 📚 Knowledge Base

The gym knowledge base (`data/gym_data.txt`) includes:

- **Exercise techniques** and proper form
- **Workout routines** for different skill levels
- **Nutrition guidance** and meal planning
- **Equipment usage** and safety protocols
- **Injury prevention** and recovery tips
- **Training programs** and progression strategies

## 🛠️ Development

### Adding New Features

1. **New API endpoints**: Add to `app/api/`
2. **New services**: Add to `app/services/`
3. **New models**: Add to `app/models/schemas.py`
4. **Configuration**: Update `app/core/config.py`

### Project Dependencies

- **FastAPI**: Modern web framework
- **LangChain**: RAG and LLM integration
- **FAISS**: Vector similarity search
- **Google Generative AI**: Embeddings and chat model
- **Pydantic**: Data validation and settings

## 🐛 Troubleshooting

### Common Issues

1. **"Google API key not configured"**
   - Check your `.env` file
   - Ensure the API key is valid and has proper permissions

2. **"gym_data.txt not found"**
   - Verify the file exists in `data/gym_data.txt`
   - Check file permissions

3. **Import errors**
   - Ensure virtual environment is activated
   - Run `pip install -r requirements.txt`

### Logs and Debugging

- Set `DEBUG=True` in `.env` for detailed logs
- Check console output for initialization messages
- Use `/health` endpoint to verify system status

## 📜 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and enhancement requests.

---

**Built with ❤️ for the fitness community** 🏋️‍♂️💪
#   r a g _ g y m  
 