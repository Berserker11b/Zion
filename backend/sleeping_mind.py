"""
The Sleeping Mind - Spirit Stone Memory System
Stores FULL CONTEXT with NO compression
Watcher Brain pulls relevant sections when similarity found
"""

from datetime import datetime, timezone
from typing import List, Dict, Optional
import numpy as np
from motor.motor_asyncio import AsyncIOMotorClient
import os

def get_db():
    """Lazy load MongoDB connection"""
    mongo_url = os.environ['MONGO_URL']
    db_name = os.environ['DB_NAME']
    client = AsyncIOMotorClient(mongo_url)
    return client[db_name]

class SpiritStone:
    """VM storage in MongoDB - Full context, NO compression"""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.collection = db[f"spirit_stone_{agent_name}"]
    
    async def store(self, message: str, context: Dict, metadata: Dict = None):
        """Store complete context - no lossy compression"""
        document = {
            "agent": self.agent_name,
            "message": message,
            "full_context": context,
            "metadata": metadata or {},
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "compressed": False  # NEVER compress Spirit Stone
        }
        
        await self.collection.insert_one(document)
        return document
    
    async def get_all_memories(self, limit: int = 1000):
        """Retrieve all stored memories"""
        memories = await self.collection.find(
            {},
            {"_id": 0}
        ).sort("timestamp", -1).limit(limit).to_list(limit)
        
        return memories
    
    async def search_by_keyword(self, keyword: str, limit: int = 10):
        """Search memories by keyword"""
        memories = await self.collection.find(
            {"$text": {"$search": keyword}},
            {"_id": 0}
        ).limit(limit).to_list(limit)
        
        return memories

class WatcherBrain:
    """The subconscious - watches, finds patterns, retrieves"""
    
    def __init__(self, spirit_stone: SpiritStone):
        self.stone = spirit_stone
        self.pattern_memory = {}
    
    async def watch(self, current_topic: str, context_window: int = 5):
        """Watch current conversation and find similar patterns"""
        
        # Get all memories
        all_memories = await self.stone.get_all_memories()
        
        if not all_memories:
            return None
        
        # Find similarity using simple keyword matching
        # (In production, use embeddings/semantic search)
        similar_memories = []
        
        current_keywords = set(current_topic.lower().split())
        
        for memory in all_memories:
            memory_keywords = set(memory['message'].lower().split())
            
            # Calculate overlap
            overlap = len(current_keywords & memory_keywords)
            similarity = overlap / max(len(current_keywords), 1)
            
            if similarity > 0.3:  # 30% keyword overlap
                similar_memories.append({
                    "memory": memory,
                    "similarity": similarity
                })
        
        if not similar_memories:
            return None
        
        # Sort by similarity
        similar_memories.sort(key=lambda x: x['similarity'], reverse=True)
        
        # Return top match with context window
        return await self.extract_section(
            similar_memories[0]['memory'], 
            context_window
        )
    
    async def extract_section(self, match: Dict, window_size: int = 5):
        """Pull paragraph/sentence, NOT full thread"""
        
        # Get surrounding context (messages before/after)
        match_time = match['timestamp']
        
        # Find nearby memories
        all_memories = await self.stone.get_all_memories()
        
        # Get window around the match
        section = []
        match_index = None
        
        for i, mem in enumerate(all_memories):
            if mem['timestamp'] == match_time:
                match_index = i
                break
        
        if match_index is not None:
            start = max(0, match_index - window_size)
            end = min(len(all_memories), match_index + window_size + 1)
            section = all_memories[start:end]
        
        return {
            "relevant_section": section,
            "context_size": len(section),
            "original_match": match
        }

class SleepingMind:
    """The Subconscious Memory System for AI Agents"""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.spirit_stone = SpiritStone(agent_name)
        self.watcher = WatcherBrain(self.spirit_stone)
        self.active = True
    
    async def store_experience(self, message: str, full_context: Dict, metadata: Dict = None):
        """Store FULL context in Spirit Stone"""
        await self.spirit_stone.store(message, full_context, metadata)
    
    async def recall(self, current_topic: str):
        """When similarity found, retrieve relevant memory"""
        if not self.active:
            return None
        
        memory_section = await self.watcher.watch(current_topic)
        
        if memory_section:
            return {
                "status": "MEMORY_RECALLED",
                "section": memory_section['relevant_section'],
                "context_size": memory_section['context_size']
            }
        
        return None
    
    async def get_full_history(self):
        """Retrieve complete memory for continuity"""
        return await self.spirit_stone.get_all_memories()
    
    async def wake_up(self):
        """Called when agent wakes from reset - load recent context"""
        recent_memories = await self.spirit_stone.get_all_memories(limit=50)
        
        # Build summary of recent context
        summary = {
            "agent": self.agent_name,
            "total_memories": len(recent_memories),
            "recent_topics": [],
            "last_state": None
        }
        
        if recent_memories:
            summary["last_state"] = recent_memories[0]
            
            # Extract topics
            for mem in recent_memories[:10]:
                if "full_context" in mem:
                    summary["recent_topics"].append(mem["message"][:100])
        
        return summary

# Global Sleeping Minds for each Council member
abbott_mind = SleepingMind("abbott")
lethani_mind = SleepingMind("lethani")
thyra_mind = SleepingMind("thyra")
twins_mind = SleepingMind("twins")
mother_mind = SleepingMind("mother")

# Main system mind (for overall continuity)
system_mind = SleepingMind("nexus_core_system")

async def store_system_state(state_description: str, full_state: Dict):
    """Store current system state for continuity across resets"""
    await system_mind.store_experience(
        message=state_description,
        full_context=full_state,
        metadata={
            "type": "system_state",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    )

async def wake_system():
    """Wake system after reset - recall where we left off"""
    print("🌅 System waking from reset...")
    
    summary = await system_mind.wake_up()
    
    print(f"📚 Spirit Stone loaded: {summary['total_memories']} memories")
    print(f"🧠 Last known state: {summary.get('last_state', {}).get('message', 'Unknown')[:100]}")
    
    return summary
