"""
Configuration settings for the GymPro RAG Chatbot
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Application settings"""
    
    # Basic App Settings
    APP_NAME: str = "GymPro RAG Chatbot"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # API Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Google AI Settings
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    GOOGLE_MODEL: str = "gemini-2.5-flash"
    EMBEDDING_MODEL: str = "models/embedding-001"
    TEMPERATURE: float = 0.3
    
    # RAG Settings
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    SIMILARITY_SEARCH_K: int = 3
    
    # File Paths
    PROJECT_ROOT: Path = Path(__file__).parent.parent.parent
    DATA_DIR: Path = PROJECT_ROOT / "data"
    GYM_DATA_FILE: Path = DATA_DIR / "gym_data.txt"
    
    # FAISS Settings
    VECTOR_STORE_PATH: Path = DATA_DIR / "vector_store"
    
    # Content Filtering
    GYM_KEYWORDS = {
        "exercise", "workout", "fitness", "gym", "muscle", "strength", "cardio", 
        "weight", "lifting", "training", "protein", "nutrition", "diet", "health",
        "bodybuilding", "crossfit", "yoga", "pilates", "running", "cycling",
        "treadmill", "dumbbell", "barbell", "squat", "deadlift", "bench press",
        "abs", "core", "biceps", "triceps", "shoulders", "chest", "back", "legs",
        "calories", "supplements", "recovery", "rest", "stretching", "flexibility",
        "endurance", "stamina", "metabolism", "fat loss", "muscle gain", "reps",
        "sets", "form", "technique", "safety", "injury", "prevention", "warm up",
        "cool down", "hydration", "equipment", "machines", "free weights"
    }

    def validate_settings(self) -> bool:
        """Validate that required settings are properly configured"""
        if not self.GOOGLE_API_KEY or self.GOOGLE_API_KEY == "your_google_api_key_here":
            return False
        if not self.GYM_DATA_FILE.exists():
            return False
        return True

# Create settings instance
settings = Settings()
