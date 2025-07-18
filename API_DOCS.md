# Gym Pro API Documentation

## Overview
Gym Pro is a RAG-based chatbot API that provides gym and fitness information using FastAPI, LangChain, FAISS vector store, and Google Generative AI.

## Features
- ✅ RAG (Retrieval-Augmented Generation) implementation
- ✅ FAISS vector database for document retrieval
- ✅ Google Generative AI integration
- ✅ Content filtering for gym/fitness topics only
- ✅ Comprehensive gym information dataset
- ✅ Conversation history tracking
- ✅ Error handling and logging
- ✅ Fallback mode when dependencies unavailable

## Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   - Copy `.env.example` to `.env`
   - Add your Google API key to `.env`:
     ```
     GOOGLE_API_KEY=your_google_api_key_here
     ```

3. **Get Google API Key:**
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Copy the key to your `.env` file

4. **Run the application:**
   ```bash
   python main.py
   ```
   Or use the startup script:
   ```bash
   start.bat
   ```

## API Endpoints

### 1. Welcome Endpoint
- **URL:** `GET /`
- **Description:** Welcome message and API information
- **Response:**
  ```json
  {
    "message": "Welcome to Gym Pro - Your AI Fitness Assistant!",
    "description": "Ask me anything about gym equipment, exercises, workouts, nutrition, and fitness!",
    "endpoints": {
      "chat": "POST /chat - Ask fitness questions",
      "health": "GET /health - Check system status",
      "reset": "POST /reset - Clear conversation history"
    },
    "rag_enabled": true
  }
  ```

### 2. Health Check
- **URL:** `GET /health`
- **Description:** Check system status and RAG initialization
- **Response:**
  ```json
  {
    "status": "healthy",
    "message": "Gym Pro chatbot is running normally"
  }
  ```

### 3. Chat Endpoint
- **URL:** `POST /chat`
- **Description:** Main chat endpoint for gym-related questions
- **Request Body:**
  ```json
  {
    "message": "What are the best exercises for chest?"
  }
  ```
- **Response:**
  ```json
  {
    "response": "For chest development, the best exercises include: 1. Bench Press - targets the entire chest...",
    "source_documents": [
      "Bench Press: Lie on bench, grip barbell slightly wider than shoulders...",
      "Push-ups: Start in plank position, lower chest to floor..."
    ]
  }
  ```

### 4. Reset Conversation
- **URL:** `POST /reset`
- **Description:** Clear conversation history
- **Response:**
  ```json
  {
    "message": "Conversation history has been reset"
  }
  ```

### 5. Conversation History (Debug)
- **URL:** `GET /conversation-history`
- **Description:** Get conversation history for debugging
- **Response:**
  ```json
  {
    "history": [
      {
        "question": "What are squats?",
        "answer": "Squats are a fundamental compound exercise...",
        "timestamp": "..."
      }
    ]
  }
  ```

## Content Filtering

The chatbot only responds to gym and fitness-related topics including:
- Gym equipment and machines
- Exercise techniques and form
- Workout routines and programs
- Nutrition and diet advice
- Supplements and protein
- Cardio and strength training
- Injury prevention and safety
- Membership and gym etiquette

### Non-gym questions will receive:
```json
{
  "response": "I'm a specialized gym and fitness assistant. I can only help with questions about gym equipment, exercises, workout routines, nutrition, and fitness topics. Please ask me something related to fitness or gym training!",
  "source_documents": []
}
```

## Example Usage

### Using cURL:
```bash
# Health check
curl -X GET "http://localhost:8000/health"

# Ask a fitness question
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "How do I perform a proper squat?"}'

# Reset conversation
curl -X POST "http://localhost:8000/reset"
```

### Using Python requests:
```python
import requests

# Chat example
response = requests.post(
    "http://localhost:8000/chat",
    json={"message": "What's the best workout for beginners?"}
)
print(response.json())
```

## RAG Implementation Details

### Vector Store: FAISS
- Uses Facebook AI Similarity Search for efficient vector similarity
- Stores embeddings of gym-related documents
- Enables fast retrieval of relevant content

### Embeddings: HuggingFace
- Model: `sentence-transformers/all-MiniLM-L6-v2`
- Converts text to vector representations
- Optimized for semantic similarity search

### LLM: Google Generative AI
- Model: `gemini-pro`
- Temperature: 0.3 (balanced creativity and accuracy)
- Processes retrieved context to generate responses

### Document Processing
- Chunk size: 1000 characters
- Chunk overlap: 200 characters
- Recursive character text splitting for optimal chunks

## Error Handling

### Common Error Responses:
- **400:** Empty message
- **500:** RAG system not initialized
- **500:** Google API key missing or invalid

### Fallback Mode:
If LangChain dependencies are unavailable, the system runs in fallback mode with:
- Simple keyword-based responses
- Basic content filtering
- Reduced functionality but still operational

## Data Sources

The system includes comprehensive gym information covering:
- Equipment guides (cardio, strength training)
- Exercise instructions with proper form
- Workout programs (beginner to advanced)
- Nutrition and supplementation advice
- Safety protocols and injury prevention
- Gym etiquette and membership information

## Testing

Use the included test client:
```bash
python test_client.py
```

This will test all endpoints with various gym-related questions and verify the content filtering works correctly.

## Logging

The application logs:
- System initialization status
- Chat request processing
- RAG chain operations
- Error conditions and fallbacks
- Conversation history operations

Logs are output to console with INFO level by default.

## Architecture

```
User Request → Content Filter → RAG Chain → Response
                    ↓              ↓
              Non-gym topics   Gym Data Retrieval
                    ↓              ↓
              Rejection Msg    Vector Search (FAISS)
                                   ↓
                              Context + LLM → Answer
```

## Performance Considerations

- First request may be slower due to model loading
- Subsequent requests are fast due to cached embeddings
- FAISS provides efficient similarity search at scale
- Vector store can be persisted to disk for faster startup

## Security Notes

- API keys should be kept secure in environment variables
- No user authentication implemented (add if needed)
- Input validation prevents empty messages
- Content filtering prevents off-topic responses

## Future Enhancements

Potential improvements:
- User authentication and session management
- Rate limiting and API usage tracking
- Custom embedding fine-tuning on gym data
- Multi-language support
- Advanced conversation memory
- Integration with fitness tracking APIs
