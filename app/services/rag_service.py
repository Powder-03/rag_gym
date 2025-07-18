"""
RAG (Retrieval-Augmented Generation) service for the GymPro chatbot
"""
import logging
from typing import List, Optional, Dict, Any
from pathlib import Path

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate

from app.core.config import settings

logger = logging.getLogger(__name__)

class RAGService:
    """Service class for handling RAG operations"""
    
    def __init__(self):
        self.vectorstore: Optional[FAISS] = None
        self.qa_chain: Optional[RetrievalQA] = None
        self.embeddings: Optional[GoogleGenerativeAIEmbeddings] = None
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the RAG prompt template"""
        template = """You are GymPro AI, an expert fitness and gym assistant with comprehensive knowledge about:
- Exercise techniques and proper form
- Workout routines and training programs  
- Gym equipment usage and safety
- Nutrition and supplements for fitness goals
- Injury prevention and recovery
- Bodybuilding, powerlifting, and general fitness

IMPORTANT GUIDELINES:
1. ONLY answer questions related to gym, fitness, exercise, nutrition, and health topics
2. If asked about non-fitness topics, politely redirect to gym-related questions
3. Always prioritize safety and proper form in your advice
4. Provide practical, actionable guidance when possible
5. Recommend consulting healthcare professionals for medical concerns
6. Base your answers on the provided context while drawing from your fitness expertise
7. Be encouraging and supportive in your responses
8. If you're uncertain about something, say so rather than guessing

Context Information:
{context}

Human Question: {question}

GymPro AI Response:"""
        
        return PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
    
    def load_gym_data(self) -> List[Document]:
        """Load gym data from file and split into documents"""
        try:
            if not settings.GYM_DATA_FILE.exists():
                logger.error(f"Gym data file not found: {settings.GYM_DATA_FILE}")
                return []
            
            with open(settings.GYM_DATA_FILE, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Split content into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=settings.CHUNK_SIZE,
                chunk_overlap=settings.CHUNK_OVERLAP,
                length_function=len,
            )
            
            chunks = text_splitter.split_text(content)
            documents = [Document(page_content=chunk) for chunk in chunks]
            
            logger.info(f"Loaded {len(documents)} document chunks from gym data")
            return documents
            
        except Exception as e:
            logger.error(f"Error loading gym data: {e}")
            return []
    
    def initialize_rag_system(self) -> bool:
        """Initialize the RAG system with FAISS vector store"""
        try:
            # Validate settings
            if not settings.validate_settings():
                logger.error("Invalid settings configuration")
                return False
            
            # Load gym data
            documents = self.load_gym_data()
            if not documents:
                logger.error("No documents loaded")
                return False
            
            # Initialize embeddings
            self.embeddings = GoogleGenerativeAIEmbeddings(
                model=settings.EMBEDDING_MODEL,
                google_api_key=settings.GOOGLE_API_KEY
            )
            
            # Create FAISS vector store
            logger.info("Creating FAISS vector store...")
            self.vectorstore = FAISS.from_documents(documents, self.embeddings)
            
            # Initialize the LLM
            llm = ChatGoogleGenerativeAI(
                model=settings.GOOGLE_MODEL,
                temperature=settings.TEMPERATURE,
                google_api_key=settings.GOOGLE_API_KEY
            )
            
            # Create the retrieval QA chain with custom prompt
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=self.vectorstore.as_retriever(
                    search_type="similarity",
                    search_kwargs={"k": settings.SIMILARITY_SEARCH_K}
                ),
                return_source_documents=True,
                chain_type_kwargs={"prompt": self.prompt_template}
            )
            
            logger.info("RAG system initialized successfully with FAISS")
            return True
            
        except Exception as e:
            logger.error(f"Error initializing RAG system: {e}")
            return False
    
    def query(self, message: str) -> Dict[str, Any]:
        """Query the RAG system"""
        try:
            if not self.qa_chain:
                raise ValueError("RAG system not initialized")
            
            result = self.qa_chain({"query": message})
            
            # Extract sources if available
            sources = []
            if "source_documents" in result and result["source_documents"]:
                sources = [doc.page_content[:100] + "..." for doc in result["source_documents"]]
            
            return {
                "response": result["result"],
                "sources": sources,
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Error querying RAG system: {e}")
            return {
                "response": "",
                "sources": [],
                "success": False,
                "error": str(e)
            }
    
    def reset_system(self) -> bool:
        """Reset and reinitialize the RAG system"""
        try:
            # Clear existing components
            self.vectorstore = None
            self.qa_chain = None
            self.embeddings = None
            
            # Reinitialize
            return self.initialize_rag_system()
            
        except Exception as e:
            logger.error(f"Error resetting RAG system: {e}")
            return False
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status"""
        return {
            "vectorstore_loaded": self.vectorstore is not None,
            "qa_chain_initialized": self.qa_chain is not None,
            "embeddings_ready": self.embeddings is not None,
            "google_api_configured": bool(settings.GOOGLE_API_KEY and 
                                        settings.GOOGLE_API_KEY != "your_google_api_key_here")
        }
    
    def is_rag_ready(self) -> bool:
        """Check if RAG system is ready"""
        return self.qa_chain is not None

# Create global RAG service instance
rag_service = RAGService()
