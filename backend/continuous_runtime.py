"""
Continuous Runtime Worker
Runs 24/7 producing power until all ZPMs are fully stockpiled
Everything goes through the Council of Five for governance
"""

import asyncio
import time
import random
from motor.motor_asyncio import AsyncIOMotorClient
import os
from datetime import datetime, timezone
from typing import Dict

from nexus_core import nexus_core
from security import security_walls
from council_of_five import council_of_five

# MongoDB connection
mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
db_name = os.environ.get('DB_NAME', 'fluxcore_db')
client = AsyncIOMotorClient(mongo_url)
db = client[db_name]

class ContinuousRuntime:
    """Manages continuous 24/7 operation of the Nexus Core system"""
    
    def __init__(self):
        self.running = False
        self.cycles_completed = 0
        self.total_power_produced = 0.0
        self.start_time = None
    
    async def simulate_entropy_generation(self) -> float:
        """Simulate continuous entropy generation even without active attacks"""
        # Base entropy from system operations
        base_entropy = random.uniform(5.0, 15.0)
        
        # Add entropy from wall stats (real attacks)
        wall_entropy = sum(
            security_walls.wall_stats[i]["entropy"] 
            for i in range(1, 7)
        )
        
        return base_entropy + (wall_entropy * 0.1)
    
    async def check_stockpile_status(self) -> Dict:
        """Check if all ZPMs are fully stockpiled"""
        all_charged = all(
            zpm.status == "charged" 
            for zpm in nexus_core.zpms
        )
        
        total_capacity = sum(zpm.capacity for zpm in nexus_core.zpms)
        total_stored = sum(zpm.stored_energy for zpm in nexus_core.zpms)
        
        fill_percentage = (total_stored / total_capacity) * 100 if total_capacity > 0 else 0
        
        return {
            "all_charged": all_charged,
            "fill_percentage": fill_percentage,
            "total_stored": total_stored,
            "total_capacity": total_capacity
        }
    
    async def production_cycle(self):
        """Single production cycle - runs through Council governance"""
        self.cycles_completed += 1
        
        # Step 1: Simulate entropy generation
        entropy = await self.simulate_entropy_generation()
        
        # Step 2: Get system state for Council review
        wall_stats = security_walls.get_wall_stats()
        stockpile = await self.check_stockpile_status()
        
        # Get recent security events
        recent_events = await db.security_events.find().sort("timestamp", -1).limit(20).to_list(20)
        
        system_state = {
            "available_power": entropy,
            "power_demand": 50.0,
            "wall_stats": wall_stats,
            "security_events": recent_events,
            "stockpile_status": stockpile
        }
        
        # Step 3: Council of Five convenes to govern this cycle
        council_decision = council_of_five.convene(system_state)
        
        # Step 4: Execute based on Council decision
        if council_decision["decision"] == "continue_all_operations":
            # Process entropy through Nexus Core
            wall_entropy_dict = {
                i: security_walls.wall_stats[i]["entropy"] 
                for i in range(1, 7)
            }
            wall_entropy_dict[1] = entropy  # Add simulated entropy to Wall 1
            
            result = nexus_core.process_entropy_from_walls(wall_entropy_dict)
            power_produced = result.get("total_power_generated", 0)
            self.total_power_produced += power_produced
            
            # Log to database
            if power_produced > 0:
                from models import PowerGeneration
                power_gen = PowerGeneration(
                    source="continuous_runtime",
                    power_amount=power_produced,
                    efficiency=random.uniform(0.85, 0.98)
                )
                doc = power_gen.model_dump()
                doc['timestamp'] = doc['timestamp'].isoformat()
                await db.power_generation.insert_one(doc)
            
            return {
                "cycle": self.cycles_completed,
                "entropy_generated": entropy,
                "power_produced": power_produced,
                "council_decision": council_decision,
                "stockpile": stockpile
            }
        else:
            # Council decided to adjust operations
            return {
                "cycle": self.cycles_completed,
                "status": "adjusted_by_council",
                "council_decision": council_decision,
                "stockpile": stockpile
            }
    
    async def run(self):
        """Main continuous runtime loop"""
        self.running = True
        self.start_time = time.time()
        
        print("🚀 Continuous Runtime Started - Council of Five Governing")
        print(f"   Started at: {datetime.now(timezone.utc).isoformat()}")
        
        while self.running:
            try:
                # Check stockpile status
                stockpile = await self.check_stockpile_status()
                
                if stockpile["all_charged"]:
                    # All ZPMs fully charged - maintain stockpile
                    print(f"✅ Cycle {self.cycles_completed}: All ZPMs fully stockpiled ({stockpile['fill_percentage']:.1f}%)")
                    # Continue running to maintain levels
                else:
                    # Continue producing
                    result = await self.production_cycle()
                    
                    if self.cycles_completed % 10 == 0:
                        print(f"⚡ Cycle {self.cycles_completed}: Stockpile at {stockpile['fill_percentage']:.1f}% | Total Power: {self.total_power_produced:.2f}")
                
                # Sleep for a short interval (simulate continuous but not overwhelming)
                await asyncio.sleep(5)  # 5 seconds between cycles
                
            except Exception as e:
                print(f"❌ Error in production cycle: {str(e)}")
                await asyncio.sleep(10)
    
    def stop(self):
        """Stop the continuous runtime"""
        self.running = False
        uptime = time.time() - self.start_time if self.start_time else 0
        print(f"🛑 Continuous Runtime Stopped")
        print(f"   Uptime: {uptime/3600:.2f} hours")
        print(f"   Cycles: {self.cycles_completed}")
        print(f"   Total Power: {self.total_power_produced:.2f}")

# Global runtime instance
continuous_runtime = ContinuousRuntime()

# Start function for integration
async def start_continuous_runtime():
    """Start the continuous runtime worker"""
    await continuous_runtime.run()

if __name__ == "__main__":
    # For testing
    asyncio.run(start_continuous_runtime())
