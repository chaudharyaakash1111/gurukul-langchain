/**
 * Vector Store Memory System for Akash Gurukul Agents
 * Implements LangChain-based memory with local vector storage and Pinecone fallback
 */

const { OpenAI } = require('langchain/llms/openai');
const { OpenAIEmbeddings } = require('langchain/embeddings/openai');
const { Chroma } = require('langchain/vectorstores/chroma');
const { PineconeStore } = require('langchain/vectorstores/pinecone');
const { ConversationBufferWindowMemory } = require('langchain/memory');
const { MemoryVectorStore } = require('langchain/vectorstores/memory');
const fs = require('fs').promises;
const path = require('path');

class AgentMemorySystem {
  constructor(agentType, studentId, config = {}) {
    this.agentType = agentType; // 'seed', 'tree', or 'sky'
    this.studentId = studentId;
    this.config = {
      useLocal: config.useLocal !== false, // Default to local storage
      memoryWindow: config.memoryWindow || 20,
      embeddingModel: config.embeddingModel || 'text-embedding-ada-002',
      persistDirectory: config.persistDirectory || './memory',
      ...config
    };
    
    this.embeddings = new OpenAIEmbeddings({
      modelName: this.config.embeddingModel
    });
    
    this.vectorStore = null;
    this.conversationMemory = null;
    this.agentProfile = null;
    
    this.initialize();
  }

  async initialize() {
    try {
      // Setup conversation memory
      this.conversationMemory = new ConversationBufferWindowMemory({
        k: this.config.memoryWindow,
        returnMessages: true,
        memoryKey: 'chat_history'
      });

      // Setup vector store
      await this.initializeVectorStore();
      
      // Load agent profile
      await this.loadAgentProfile();
      
      console.log(`Memory system initialized for ${this.agentType} agent serving student ${this.studentId}`);
    } catch (error) {
      console.error('Error initializing memory system:', error);
      throw error;
    }
  }

  async initializeVectorStore() {
    const memoryPath = path.join(this.config.persistDirectory, this.agentType, this.studentId);
    
    try {
      if (this.config.useLocal) {
        // Try to use Chroma for local vector storage
        try {
          await fs.mkdir(memoryPath, { recursive: true });
          this.vectorStore = new Chroma(this.embeddings, {
            collectionName: `${this.agentType}_${this.studentId}`,
            persistDirectory: memoryPath
          });
          console.log('Using Chroma local vector store');
        } catch (chromaError) {
          console.warn('Chroma not available, falling back to in-memory store:', chromaError.message);
          this.vectorStore = new MemoryVectorStore(this.embeddings);
        }
      } else {
        // Use Pinecone for cloud storage
        if (process.env.PINECONE_API_KEY) {
          this.vectorStore = await PineconeStore.fromExistingIndex(
            this.embeddings,
            {
              pineconeIndex: process.env.PINECONE_INDEX,
              namespace: `${this.agentType}_${this.studentId}`
            }
          );
          console.log('Using Pinecone cloud vector store');
        } else {
          console.warn('Pinecone credentials not found, using in-memory store');
          this.vectorStore = new MemoryVectorStore(this.embeddings);
        }
      }
    } catch (error) {
      console.error('Error setting up vector store, using in-memory fallback:', error);
      this.vectorStore = new MemoryVectorStore(this.embeddings);
    }
  }

  async loadAgentProfile() {
    const profilePath = path.join(this.config.persistDirectory, this.agentType, this.studentId, 'profile.json');
    
    try {
      const profileData = await fs.readFile(profilePath, 'utf8');
      this.agentProfile = JSON.parse(profileData);
    } catch (error) {
      // Create new profile if doesn't exist
      this.agentProfile = this.createDefaultProfile();
      await this.saveAgentProfile();
    }
  }

  createDefaultProfile() {
    const baseProfile = {
      studentId: this.studentId,
      agentType: this.agentType,
      createdAt: new Date().toISOString(),
      lastInteraction: null,
      totalInteractions: 0,
      learningPreferences: {},
      emotionalState: 'neutral',
      progressMarkers: []
    };

    // Agent-specific profile extensions
    switch (this.agentType) {
      case 'seed':
        return {
          ...baseProfile,
          confidenceLevel: 0.5,
          encouragementStyle: 'verbal',
          commonMistakes: [],
          breakthroughMoments: [],
          supportLevel: 'high'
        };
      
      case 'tree':
        return {
          ...baseProfile,
          masteredConcepts: [],
          skillProgression: {},
          learningConnections: {},
          assessmentPreferences: [],
          optimalLessonLength: 45
        };
      
      case 'sky':
        return {
          ...baseProfile,
          worldviewEvolution: [],
          coreQuestions: [],
          wisdomTraditions: [],
          personalInsights: [],
          transformationMarkers: []
        };
      
      default:
        return baseProfile;
    }
  }

  async saveAgentProfile() {
    const profilePath = path.join(this.config.persistDirectory, this.agentType, this.studentId, 'profile.json');
    
    try {
      await fs.mkdir(path.dirname(profilePath), { recursive: true });
      await fs.writeFile(profilePath, JSON.stringify(this.agentProfile, null, 2));
    } catch (error) {
      console.error('Error saving agent profile:', error);
    }
  }

  async addMemory(content, metadata = {}) {
    try {
      const document = {
        pageContent: content,
        metadata: {
          timestamp: new Date().toISOString(),
          agentType: this.agentType,
          studentId: this.studentId,
          interactionType: metadata.type || 'conversation',
          ...metadata
        }
      };

      await this.vectorStore.addDocuments([document]);
      
      // Update agent profile
      this.agentProfile.lastInteraction = new Date().toISOString();
      this.agentProfile.totalInteractions += 1;
      await this.saveAgentProfile();
      
      console.log(`Memory added for ${this.agentType} agent`);
    } catch (error) {
      console.error('Error adding memory:', error);
      throw error;
    }
  }

  async searchMemory(query, options = {}) {
    try {
      const searchOptions = {
        k: options.limit || 5,
        filter: {
          agentType: this.agentType,
          studentId: this.studentId,
          ...options.filter
        }
      };

      const results = await this.vectorStore.similaritySearch(query, searchOptions.k);
      
      return results.map(doc => ({
        content: doc.pageContent,
        metadata: doc.metadata,
        relevance: doc.score || 0
      }));
    } catch (error) {
      console.error('Error searching memory:', error);
      return [];
    }
  }

  async getConversationHistory() {
    try {
      const history = await this.conversationMemory.loadMemoryVariables({});
      return history.chat_history || [];
    } catch (error) {
      console.error('Error retrieving conversation history:', error);
      return [];
    }
  }

  async addToConversation(humanMessage, aiMessage) {
    try {
      await this.conversationMemory.saveContext(
        { input: humanMessage },
        { output: aiMessage }
      );
      
      // Also store in vector memory for long-term retrieval
      await this.addMemory(`Human: ${humanMessage}\nAI: ${aiMessage}`, {
        type: 'conversation',
        humanMessage,
        aiMessage
      });
    } catch (error) {
      console.error('Error adding to conversation:', error);
    }
  }

  async updateLearningProgress(lessonId, performance, insights = {}) {
    try {
      const progressEntry = {
        lessonId,
        performance,
        timestamp: new Date().toISOString(),
        insights
      };

      this.agentProfile.progressMarkers.push(progressEntry);
      
      // Agent-specific progress tracking
      if (this.agentType === 'tree' && insights.masteredConcepts) {
        this.agentProfile.masteredConcepts = [
          ...new Set([...this.agentProfile.masteredConcepts, ...insights.masteredConcepts])
        ];
      }
      
      await this.saveAgentProfile();
      
      // Store detailed progress in vector memory
      await this.addMemory(
        `Lesson ${lessonId} completed with performance ${performance}. Insights: ${JSON.stringify(insights)}`,
        { type: 'progress', lessonId, performance }
      );
    } catch (error) {
      console.error('Error updating learning progress:', error);
    }
  }

  async getPersonalizedContext(query) {
    try {
      // Get relevant memories
      const memories = await this.searchMemory(query, { limit: 3 });
      
      // Get recent conversation
      const recentConversation = await this.getConversationHistory();
      const lastFewMessages = recentConversation.slice(-4);
      
      // Combine with agent profile
      return {
        agentProfile: this.agentProfile,
        relevantMemories: memories,
        recentConversation: lastFewMessages,
        contextSummary: this.generateContextSummary(memories, lastFewMessages)
      };
    } catch (error) {
      console.error('Error getting personalized context:', error);
      return {
        agentProfile: this.agentProfile,
        relevantMemories: [],
        recentConversation: [],
        contextSummary: 'No context available'
      };
    }
  }

  generateContextSummary(memories, conversation) {
    // Simple context summary generation
    const memoryTopics = memories.map(m => m.metadata.type || 'general').join(', ');
    const conversationLength = conversation.length;
    
    return `Recent interactions: ${conversationLength} messages. Memory topics: ${memoryTopics}. Student progress: ${this.agentProfile.totalInteractions} total interactions.`;
  }

  async clearMemory() {
    try {
      // Clear conversation memory
      await this.conversationMemory.clear();
      
      // Reset agent profile
      this.agentProfile = this.createDefaultProfile();
      await this.saveAgentProfile();
      
      console.log(`Memory cleared for ${this.agentType} agent`);
    } catch (error) {
      console.error('Error clearing memory:', error);
    }
  }
}

module.exports = AgentMemorySystem;
