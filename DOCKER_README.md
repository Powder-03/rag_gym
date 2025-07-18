# Docker Deployment Guide for GymPro RAG Chatbot

## Prerequisites

- Docker installed on your system
- Docker Compose (included with Docker Desktop)
- Your Google API key

## Quick Start

### 1. Environment Setup

First, create your `.env` file from the example:

```bash
cp .env.example .env
```

Edit `.env` and add your Google API key:
```env
GOOGLE_API_KEY=your_actual_google_api_key_here
```

### 2. Build and Run with Docker Compose (Recommended)

```bash
# Build and start the application
docker-compose up --build

# Run in detached mode (background)
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

### 3. Manual Docker Commands

```bash
# Build the image
docker build -t gym-pro-chatbot .

# Run the container
docker run -d \
  --name gym-pro-rag-chatbot \
  -p 8001:8001 \
  --env-file .env \
  -v $(pwd)/data:/app/data:ro \
  -v $(pwd)/logs:/app/logs \
  gym-pro-chatbot

# View logs
docker logs -f gym-pro-rag-chatbot

# Stop and remove container
docker stop gym-pro-rag-chatbot
docker rm gym-pro-rag-chatbot
```

## Application Access

Once running, the application will be available at:
- **Streamlit Frontend**: http://localhost:8501 (Primary UI)
- **FastAPI Backend**: http://localhost:8001
- **API Documentation**: http://localhost:8001/docs
- **Health Check**: http://localhost:8001/health

## Environment Variables

Key environment variables you can configure:

```env
# Required
GOOGLE_API_KEY=your_google_api_key_here

# Optional (with defaults)
HOST=0.0.0.0
PORT=8001
DEBUG=false
TEMPERATURE=0.1
CHUNK_SIZE=1000
CHUNK_OVERLAP=100
SIMILARITY_SEARCH_K=3
```

## Volume Mounts

- `./data:/app/data:ro` - Mount gym data directory (read-only)
- `./logs:/app/logs` - Mount logs directory for persistence

## Troubleshooting

### Check container status
```bash
docker-compose ps
```

### View detailed logs
```bash
docker-compose logs gym-pro-chatbot
```

### Restart the service
```bash
docker-compose restart gym-pro-chatbot
```

### Rebuild after code changes
```bash
docker-compose down
docker-compose up --build
```

### Access container shell
```bash
docker-compose exec gym-pro-chatbot /bin/bash
```

## Production Deployment

For production deployment:

1. Set `DEBUG=false` in your `.env` file
2. Use a reverse proxy (nginx) for SSL termination
3. Set up proper logging and monitoring
4. Consider using Docker secrets for sensitive data
5. Set resource limits in docker-compose.yml:

```yaml
services:
  gym-pro-chatbot:
    # ... other config ...
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
```

## Health Monitoring

The application includes health checks:
- Container health check every 30 seconds
- Health endpoint: `/health`
- API status endpoint: `/api/health`

## Security Notes

- Never commit your `.env` file with real API keys
- Use Docker secrets in production
- Run containers as non-root user in production
- Keep your Docker images updated
