"""
Vector Store Memory System for Akash Gurukul Agents
Implements LangChain-based memory with local vector storage and Pinecone fallback
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

from langchain_openai import OpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma, FAISS
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.documents import Document
try:
    from langchain_pinecone import Pinecone
except ImportError:
    Pinecone = None


class AgentMemorySystem:
    def __init__(self, agent_type: str, student_id: str, config: Dict[str, Any] = None):
        """
        Initialize the memory system for a specific agent and student
        
        Args:
            agent_type: 'seed', 'tree', or 'sky'
            student_id: Unique identifier for the student
            config: Configuration dictionary
        """
        self.agent_type = agent_type
        self.student_id = student_id
        self.config = config or {}
        
        # Default configuration
        self.config.setdefault('use_local', True)
        self.config.setdefault('memory_window', 20)
        self.config.setdefault('embedding_model', 'text-embedding-ada-002')
        self.config.setdefault('persist_directory', './memory')
        
        # Initialize components
        try:
            self.embeddings = OpenAIEmbeddings(model=self.config['embedding_model'])
        except Exception as e:
            print(f"OpenAI embeddings not available: {e}")
            print("Using FAISS with dummy embeddings for testing")
            from langchain_community.embeddings import FakeEmbeddings
            self.embeddings = FakeEmbeddings(size=1536)

        self.vector_store = None
        self.conversation_memory = None
        self.agent_profile = None
        
        # Initialize the system
        self._initialize()

    def _initialize(self):
        """Initialize all memory components"""
        try:
            # Setup conversation memory
            self.conversation_memory = ConversationBufferWindowMemory(
                k=self.config['memory_window'],
                return_messages=True,
                memory_key='chat_history'
            )
            
            # Setup vector store
            self._initialize_vector_store()
            
            # Load agent profile
            self._load_agent_profile()
            
            print(f"Memory system initialized for {self.agent_type} agent serving student {self.student_id}")
        except Exception as e:
            print(f"Error initializing memory system: {e}")
            raise

    def _initialize_vector_store(self):
        """Initialize the vector store with fallback options"""
        memory_path = Path(self.config['persist_directory']) / self.agent_type / self.student_id
        
        try:
            if self.config['use_local']:
                # Try to use Chroma for local vector storage
                try:
                    memory_path.mkdir(parents=True, exist_ok=True)
                    self.vector_store = Chroma(
                        embedding_function=self.embeddings,
                        persist_directory=str(memory_path),
                        collection_name=f"{self.agent_type}_{self.student_id}"
                    )
                    print("Using Chroma local vector store")
                except Exception as chroma_error:
                    print(f"Chroma not available, falling back to FAISS: {chroma_error}")
                    # Fallback to FAISS
                    self.vector_store = FAISS.from_texts(
                        ["Initial memory"], 
                        self.embeddings,
                        metadatas=[{"type": "initialization"}]
                    )
            else:
                # Use Pinecone for cloud storage
                if os.getenv('PINECONE_API_KEY') and Pinecone is not None:
                    try:
                        from pinecone import Pinecone as PineconeClient
                        pc = PineconeClient(api_key=os.getenv('PINECONE_API_KEY'))
                        index_name = os.getenv('PINECONE_INDEX', 'akash-gurukul')
                        index = pc.Index(index_name)
                        self.vector_store = Pinecone(
                            index=index,
                            embedding=self.embeddings,
                            text_key="text",
                            namespace=f"{self.agent_type}_{self.student_id}"
                        )
                        print("Using Pinecone cloud vector store")
                    except Exception as e:
                        print(f"Pinecone setup failed: {e}, using FAISS fallback")
                        self.vector_store = FAISS.from_texts(
                            ["Initial memory"],
                            self.embeddings,
                            metadatas=[{"type": "initialization"}]
                        )
                else:
                    print("Pinecone not available, using FAISS fallback")
                    self.vector_store = FAISS.from_texts(
                        ["Initial memory"],
                        self.embeddings,
                        metadatas=[{"type": "initialization"}]
                    )
        except Exception as e:
            print(f"Error setting up vector store, using FAISS fallback: {e}")
            self.vector_store = FAISS.from_texts(
                ["Initial memory"], 
                self.embeddings,
                metadatas=[{"type": "initialization"}]
            )

    def _load_agent_profile(self):
        """Load or create agent profile"""
        profile_path = Path(self.config['persist_directory']) / self.agent_type / self.student_id / 'profile.json'
        
        try:
            if profile_path.exists():
                with open(profile_path, 'r', encoding='utf-8') as f:
                    self.agent_profile = json.load(f)
            else:
                self.agent_profile = self._create_default_profile()
                self._save_agent_profile()
        except Exception as e:
            print(f"Error loading agent profile: {e}")
            self.agent_profile = self._create_default_profile()

    def _create_default_profile(self) -> Dict[str, Any]:
        """Create default profile based on agent type"""
        base_profile = {
            "student_id": self.student_id,
            "agent_type": self.agent_type,
            "created_at": datetime.now().isoformat(),
            "last_interaction": None,
            "total_interactions": 0,
            "learning_preferences": {},
            "emotional_state": "neutral",
            "progress_markers": []
        }

        # Agent-specific profile extensions
        if self.agent_type == 'seed':
            return {
                **base_profile,
                "confidence_level": 0.5,
                "encouragement_style": "verbal",
                "common_mistakes": [],
                "breakthrough_moments": [],
                "support_level": "high"
            }
        elif self.agent_type == 'tree':
            return {
                **base_profile,
                "mastered_concepts": [],
                "skill_progression": {},
                "learning_connections": {},
                "assessment_preferences": [],
                "optimal_lesson_length": 45
            }
        elif self.agent_type == 'sky':
            return {
                **base_profile,
                "worldview_evolution": [],
                "core_questions": [],
                "wisdom_traditions": [],
                "personal_insights": [],
                "transformation_markers": []
            }
        else:
            return base_profile

    def _save_agent_profile(self):
        """Save agent profile to disk"""
        profile_path = Path(self.config['persist_directory']) / self.agent_type / self.student_id / 'profile.json'
        
        try:
            profile_path.parent.mkdir(parents=True, exist_ok=True)
            with open(profile_path, 'w', encoding='utf-8') as f:
                json.dump(self.agent_profile, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving agent profile: {e}")

    def add_memory(self, content: str, metadata: Dict[str, Any] = None) -> None:
        """Add a memory to the vector store"""
        try:
            metadata = metadata or {}
            document_metadata = {
                "timestamp": datetime.now().isoformat(),
                "agent_type": self.agent_type,
                "student_id": self.student_id,
                "interaction_type": metadata.get('type', 'conversation'),
                **metadata
            }

            document = Document(
                page_content=content,
                metadata=document_metadata
            )

            self.vector_store.add_documents([document])
            
            # Update agent profile
            self.agent_profile['last_interaction'] = datetime.now().isoformat()
            self.agent_profile['total_interactions'] += 1
            self._save_agent_profile()
            
            print(f"Memory added for {self.agent_type} agent")
        except Exception as e:
            print(f"Error adding memory: {e}")
            raise

    def search_memory(self, query: str, limit: int = 5, filter_dict: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Search for relevant memories"""
        try:
            # Perform similarity search
            results = self.vector_store.similarity_search(query, k=limit)
            
            # Filter results if needed
            if filter_dict:
                filtered_results = []
                for doc in results:
                    if all(doc.metadata.get(k) == v for k, v in filter_dict.items()):
                        filtered_results.append(doc)
                results = filtered_results
            
            return [
                {
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "relevance": getattr(doc, 'score', 0)
                }
                for doc in results
            ]
        except Exception as e:
            print(f"Error searching memory: {e}")
            return []

    def get_conversation_history(self) -> List[Any]:
        """Get recent conversation history"""
        try:
            history = self.conversation_memory.load_memory_variables({})
            return history.get('chat_history', [])
        except Exception as e:
            print(f"Error retrieving conversation history: {e}")
            return []

    def add_to_conversation(self, human_message: str, ai_message: str) -> None:
        """Add exchange to conversation memory"""
        try:
            self.conversation_memory.save_context(
                {"input": human_message},
                {"output": ai_message}
            )
            
            # Also store in vector memory for long-term retrieval
            self.add_memory(
                f"Human: {human_message}\nAI: {ai_message}",
                {"type": "conversation", "human_message": human_message, "ai_message": ai_message}
            )
        except Exception as e:
            print(f"Error adding to conversation: {e}")

    def update_learning_progress(self, lesson_id: str, performance: float, insights: Dict[str, Any] = None) -> None:
        """Update learning progress tracking"""
        try:
            insights = insights or {}
            progress_entry = {
                "lesson_id": lesson_id,
                "performance": performance,
                "timestamp": datetime.now().isoformat(),
                "insights": insights
            }

            self.agent_profile['progress_markers'].append(progress_entry)
            
            # Agent-specific progress tracking
            if self.agent_type == 'tree' and insights.get('mastered_concepts'):
                current_concepts = set(self.agent_profile.get('mastered_concepts', []))
                new_concepts = set(insights['mastered_concepts'])
                self.agent_profile['mastered_concepts'] = list(current_concepts | new_concepts)
            
            self._save_agent_profile()
            
            # Store detailed progress in vector memory
            self.add_memory(
                f"Lesson {lesson_id} completed with performance {performance}. Insights: {json.dumps(insights)}",
                {"type": "progress", "lesson_id": lesson_id, "performance": performance}
            )
        except Exception as e:
            print(f"Error updating learning progress: {e}")

    def get_personalized_context(self, query: str) -> Dict[str, Any]:
        """Get personalized context for the agent"""
        try:
            # Get relevant memories
            memories = self.search_memory(query, limit=3)
            
            # Get recent conversation
            recent_conversation = self.get_conversation_history()
            last_few_messages = recent_conversation[-4:] if len(recent_conversation) > 4 else recent_conversation
            
            # Generate context summary
            context_summary = self._generate_context_summary(memories, last_few_messages)
            
            return {
                "agent_profile": self.agent_profile,
                "relevant_memories": memories,
                "recent_conversation": last_few_messages,
                "context_summary": context_summary
            }
        except Exception as e:
            print(f"Error getting personalized context: {e}")
            return {
                "agent_profile": self.agent_profile,
                "relevant_memories": [],
                "recent_conversation": [],
                "context_summary": "No context available"
            }

    def _generate_context_summary(self, memories: List[Dict], conversation: List[Any]) -> str:
        """Generate a summary of the current context"""
        memory_types = [m.get('metadata', {}).get('type', 'general') for m in memories]
        memory_topics = ', '.join(set(memory_types))
        conversation_length = len(conversation)
        
        return (f"Recent interactions: {conversation_length} messages. "
                f"Memory topics: {memory_topics}. "
                f"Student progress: {self.agent_profile['total_interactions']} total interactions.")

    def clear_memory(self) -> None:
        """Clear all memory (use with caution)"""
        try:
            # Clear conversation memory
            self.conversation_memory.clear()
            
            # Reset agent profile
            self.agent_profile = self._create_default_profile()
            self._save_agent_profile()
            
            print(f"Memory cleared for {self.agent_type} agent")
        except Exception as e:
            print(f"Error clearing memory: {e}")


# Example usage and testing
if __name__ == "__main__":
    # Test the memory system
    memory_system = AgentMemorySystem("seed", "test_student_001")
    
    # Add some test memories
    memory_system.add_memory("Student showed interest in kindness lesson", {"type": "observation"})
    memory_system.add_to_conversation("What is kindness?", "Kindness is like sunshine for the heart...")
    
    # Search memories
    results = memory_system.search_memory("kindness")
    print(f"Found {len(results)} relevant memories")
    
    # Get personalized context
    context = memory_system.get_personalized_context("kindness lesson")
    print(f"Context summary: {context['context_summary']}")
