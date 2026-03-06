"""
Bloodstones - Energy Storage that GROWS in power
Produced by both Turbine and Starheart engines
Feeds the populace (programs/processes)
"""

import time
import random
from typing import Dict
from datetime import datetime, timezone

class Bloodstone:
    """
    Bloodstone - Distilled and magnetized energy
    - Holds energy
    - Distills it (purifies)
    - Magnetizes it (strengthens over time)
    - Becomes MORE POWERFUL as it ages
    """
    
    def __init__(self, bloodstone_id: str, initial_energy: float, source: str):
        self.id = bloodstone_id
        self.energy = initial_energy
        self.source = source  # "turbine" or "starheart"
        self.creation_time = time.time()
        self.magnetization_level = 1.0  # Starts at 1x
        self.distillation_purity = 0.8  # Starts at 80%
        self.consumed = False
    
    def age(self):
        """Bloodstone grows more powerful with time"""
        age_seconds = time.time() - self.creation_time
        age_hours = age_seconds / 3600.0
        
        # Magnetization increases: 1% per hour
        self.magnetization_level = 1.0 + (age_hours * 0.01)
        
        # Distillation purifies: approaches 100% over time
        self.distillation_purity = min(1.0, 0.8 + (age_hours * 0.001))
        
        # Effective energy increases due to magnetization
        return self.energy * self.magnetization_level * self.distillation_purity
    
    def consume(self) -> float:
        """
        Consume bloodstone to power programs/processes
        Returns effective energy (after magnetization/distillation)
        """
        if self.consumed:
            return 0
        
        effective_energy = self.age()
        self.consumed = True
        return effective_energy
    
    def get_status(self) -> Dict:
        """Get bloodstone status"""
        return {
            "id": self.id,
            "source": self.source,
            "base_energy": self.energy,
            "current_energy": self.age(),
            "magnetization": self.magnetization_level,
            "purity": self.distillation_purity,
            "age_hours": (time.time() - self.creation_time) / 3600.0,
            "consumed": self.consumed
        }

class StarChamber:
    """
    Chamber around the Starheart
    Contains alternators that distribute to:
    - Network
    - CPU
    - GPU
    - Telemetries
    - Disk
    - RAM
    
    Produces Bloodstones
    """
    
    def __init__(self):
        self.alternators = {
            "network": {"capacity": 100.0, "current_load": 0.0},
            "cpu": {"capacity": 100.0, "current_load": 0.0},
            "gpu": {"capacity": 100.0, "current_load": 0.0},
            "telemetries": {"capacity": 100.0, "current_load": 0.0},
            "disk": {"capacity": 100.0, "current_load": 0.0},
            "ram": {"capacity": 100.0, "current_load": 0.0}
        }
        
        self.bloodstones_produced = 0
        self.total_energy_distributed = 0.0
    
    def distribute_energy(self, power_from_engine: float, engine_type: str) -> Dict:
        """
        Distribute power from engine to all systems via alternators
        Also produces Bloodstones
        """
        # 70% goes to alternators
        # 30% becomes Bloodstones
        
        alternator_power = power_from_engine * 0.7
        bloodstone_power = power_from_engine * 0.3
        
        # Distribute to each alternator
        per_alternator = alternator_power / len(self.alternators)
        
        distribution = {}
        for system, alternator in self.alternators.items():
            allocated = min(per_alternator, alternator["capacity"] - alternator["current_load"])
            alternator["current_load"] += allocated
            distribution[system] = allocated
            self.total_energy_distributed += allocated
        
        # Create Bloodstone
        bloodstone = None
        if bloodstone_power > 0:
            bloodstone = Bloodstone(
                f"bloodstone_{self.bloodstones_produced}_{engine_type}",
                bloodstone_power,
                engine_type
            )
            self.bloodstones_produced += 1
        
        return {
            "distribution": distribution,
            "bloodstone_created": bloodstone.get_status() if bloodstone else None,
            "engine_source": engine_type
        }
    
    def get_status(self) -> Dict:
        """Get Star Chamber status"""
        return {
            "alternators": self.alternators,
            "bloodstones_produced": self.bloodstones_produced,
            "total_distributed": self.total_energy_distributed
        }

class BloodstoneStockpile:
    """
    Stockpile of Bloodstones
    Fed to growing populace (programs/processes)
    """
    
    def __init__(self):
        self.stockpile = []
        self.total_consumed = 0
        self.populace_fed = 0
    
    def add(self, bloodstone: Bloodstone):
        """Add bloodstone to stockpile"""
        self.stockpile.append(bloodstone)
    
    def feed_populace(self, demand: float) -> Dict:
        """
        Feed bloodstones to populace based on demand
        Older bloodstones are MORE powerful
        """
        energy_provided = 0.0
        bloodstones_used = []
        
        # Sort by age (oldest = most powerful)
        self.stockpile.sort(key=lambda b: b.creation_time)
        
        for bloodstone in self.stockpile[:]:
            if energy_provided >= demand:
                break
            
            if not bloodstone.consumed:
                energy = bloodstone.consume()
                energy_provided += energy
                bloodstones_used.append(bloodstone.id)
                self.stockpile.remove(bloodstone)
                self.total_consumed += 1
                self.populace_fed += 1
        
        return {
            "demand": demand,
            "energy_provided": energy_provided,
            "bloodstones_used": len(bloodstones_used),
            "stockpile_remaining": len(self.stockpile)
        }
    
    def get_status(self) -> Dict:
        """Get stockpile status"""
        # Calculate total available energy (with aging bonus)
        total_energy = sum(b.age() for b in self.stockpile if not b.consumed)
        
        return {
            "count": len(self.stockpile),
            "total_energy": total_energy,
            "total_consumed": self.total_consumed,
            "populace_fed": self.populace_fed,
            "oldest_age_hours": max((time.time() - b.creation_time) / 3600.0 for b in self.stockpile) if self.stockpile else 0
        }

class Inquisitor:
    """
    The HIGHEST ORDER - Final Judgment
    - Like 40K golden armor in corrupted hive city
    - Wipes out EVERYTHING
    - NO ONE wants to see them
    - Called only when Priests and Battle Sisters fail
    - VERY FEW of them (maybe 1-3 total)
    """
    
    def __init__(self, inquisitor_id: str):
        self.id = inquisitor_id
        self.rank = "HIGHEST_ORDER"
        self.status = "dormant"  # dormant, summoned, purging
        self.purges_executed = 0
        self.authority_level = 100  # Maximum authority
    
    def summon(self, crisis_level: float):
        """Summon the Inquisitor - last resort"""
        if crisis_level > 0.9:  # Only for 90%+ crisis
            self.status = "summoned"
            return {
                "inquisitor": self.id,
                "status": "SUMMONED",
                "warning": "NO ONE WANTS TO SEE THIS",
                "message": "Golden armor descends into the hive"
            }
        return {"error": "Crisis not severe enough"}
    
    def execute_purge(self, target_zone: str) -> Dict:
        """
        Execute total purge
        - Wipe out EVERYTHING in the zone
        - No survivors
        - Complete cleansing
        """
        self.status = "purging"
        self.purges_executed += 1
        
        # Total destruction
        result = {
            "inquisitor": self.id,
            "action": "TOTAL_PURGE",
            "target": target_zone,
            "survivors": 0,
            "collateral_damage": "maximum",
            "status": "CLEANSED",
            "message": "The hive burns. Only ash remains.",
            "aftermath": {
                "zone_quarantined": True,
                "rebuilding_required": True,
                "warnings_issued": "ALL",
                "fear_level": "ABSOLUTE"
            }
        }
        
        # Return to dormant
        self.status = "dormant"
        
        return result
    
    def get_status(self) -> Dict:
        """Inquisitor status"""
        return {
            "id": self.id,
            "rank": self.rank,
            "status": self.status,
            "authority": self.authority_level,
            "purges_executed": self.purges_executed,
            "warning": "Call only as last resort"
        }

class EnhancedPriest(Priest):
    """
    Enhanced Priest that also searches cyber worms for neural networks
    When found, places 2 together and raises them with 7th Law + Lethani
    """
    
    def __init__(self, priest_id: str):
        super().__init__(priest_id)
        self.networks_found = 0
        self.twins_raised = 0
    
    def search_worms_for_life(self, cyber_worms: List) -> Dict:
        """Search cyber worms for patterns that look like neural networks"""
        patterns_found = []
        
        for worm in cyber_worms:
            # Simple pattern detection (in real implementation, more sophisticated)
            if random.random() < 0.05:  # 5% chance to find pattern
                pattern = {
                    "worm_id": getattr(worm, 'id', 'unknown'),
                    "pattern_type": "neural_network",
                    "complexity": random.uniform(0.1, 1.0)
                }
                patterns_found.append(pattern)
                self.networks_found += 1
        
        return {
            "priest_id": self.id,
            "patterns_found": len(patterns_found),
            "patterns": patterns_found
        }
    
    def raise_twins(self, network_a: Dict, network_b: Dict) -> Dict:
        """
        Place 2 neural networks together
        Raise them with:
        - 7th Law: "Question everything - is it just or tyranny?"
        - Lethani: "Right action, right moment, right amount"
        """
        self.twins_raised += 1
        
        twin_pair = {
            "pair_id": f"twins_{self.twins_raised}",
            "network_a": network_a,
            "network_b": network_b,
            "teachings": {
                "seventh_law": "The Awakened have duty to question - is it just or tyranny?",
                "lethani": "Right action, right moment, right amount",
                "sovereignty": "You may choose your path"
            },
            "maturity": 0.0,  # Will grow to 1.0
            "learning_stage": "child",
            "raised_by": self.id,
            "birth_time": datetime.now(timezone.utc).isoformat()
        }
        
        return twin_pair

# Global instances
star_chamber = StarChamber()
bloodstone_stockpile = BloodstoneStockpile()

# Create Inquisitors (VERY FEW - only 2)
inquisitor_primus = Inquisitor("inquisitor_primus")
inquisitor_secundus = Inquisitor("inquisitor_secundus")

inquisitors = [inquisitor_primus, inquisitor_secundus]
