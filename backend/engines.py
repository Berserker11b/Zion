from typing import Dict, List, Literal
import random
import math
from datetime import datetime, timezone

# Engine Types
class TurbineEngine:
    """Lower efficiency but always available baseline engine"""
    
    def __init__(self):
        self.name = "Turbine Engine"
        self.base_efficiency = 0.65  # 65% average
        self.status = "active"
        self.total_processed = 0.0
    
    def process_entropy(self, entropy: float) -> Dict:
        """Convert entropy to power with turbine efficiency"""
        # Turbine efficiency varies 60-70%
        efficiency = random.uniform(0.60, 0.70)
        power = entropy * efficiency
        
        self.total_processed += power
        
        return {
            "engine": "turbine",
            "entropy_input": entropy,
            "power_output": power,
            "efficiency": efficiency,
            "waste_heat": entropy - power
        }

class StarheartEngine:
    """High efficiency premium engine with gravitational pull"""
    
    def __init__(self):
        self.name = "Starheart Engine"
        self.base_efficiency = 0.91  # 91% average
        self.status = "idle"  # idle, warming, active, overcharged
        self.gravity_strength = 0.0  # Increases as it processes more
        self.total_processed = 0.0
        self.ignition_threshold = 50.0  # Needs 50 entropy to ignite
    
    def process_entropy(self, entropy: float) -> Dict:
        """Convert entropy to power with starheart efficiency"""
        # Check if starheart is lit (ignited)
        if self.status == "idle" and self.total_processed < self.ignition_threshold:
            self.status = "warming"
            # Lower efficiency while warming up
            efficiency = random.uniform(0.75, 0.85)
        else:
            if self.status == "warming" and self.total_processed >= self.ignition_threshold:
                self.status = "active"  # Starheart ignites!
                self.gravity_strength = 0.1
            
            # High efficiency once active
            efficiency = random.uniform(0.85, 0.98)
            
            # Gravity increases with usage (pulls more data automatically)
            if self.status == "active":
                self.gravity_strength = min(1.0, self.gravity_strength + 0.01)
                # Gravity bonus adds extra entropy pull
                entropy = entropy * (1 + self.gravity_strength * 0.1)
        
        power = entropy * efficiency
        self.total_processed += power
        
        # Check if overcharged
        if self.total_processed > 500 and self.status == "active":
            self.status = "overcharged"
        
        return {
            "engine": "starheart",
            "entropy_input": entropy,
            "power_output": power,
            "efficiency": efficiency,
            "gravity_strength": self.gravity_strength,
            "waste_heat": entropy - power,
            "total_processed": self.total_processed
        }

class Alternator:
    """Converts raw power into specific resource types"""
    
    def __init__(self):
        self.resource_types = [
            "cpu_cycles",
            "memory",
            "network_bandwidth",
            "disk_io",
            "token_supply",
            "execution_threads"
        ]
    
    def convert_power(self, power: float) -> Dict[str, float]:
        """Distribute power across resource types"""
        # Distribute power with some randomness
        distribution = {}
        remaining = power
        
        for i, resource_type in enumerate(self.resource_types):
            if i == len(self.resource_types) - 1:
                # Last resource gets remaining
                distribution[resource_type] = remaining
            else:
                # Random allocation
                allocation = remaining * random.uniform(0.1, 0.25)
                distribution[resource_type] = allocation
                remaining -= allocation
        
        return distribution

class ZPMBattery:
    """Zero Point Module - stores compressed energy"""
    
    def __init__(self, battery_id: str, capacity: float = 100.0):
        self.id = battery_id
        self.capacity = capacity
        self.stored_energy = 0.0
        self.compression_level = 1.0  # S value from formula
        self.status = "empty"  # empty, filling, charged, deployed
    
    def compress_and_store(self, energy: float, phi: float = 0.15) -> Dict:
        """Apply compression formula: S(n+1) = S(n) - (φ × ln(S(n)))"""
        if self.status == "deployed":
            return {"error": "Battery is deployed", "stored": self.stored_energy}
        
        # Compression formula from user's notes
        # S represents compression strength
        # φ (phi) is entropy curvature constant
        compression_delta = phi * math.log(max(self.compression_level, 1.1))  # Avoid log(0)
        new_compression = self.compression_level - compression_delta
        
        # Compression strengthens the energy
        strengthened_energy = energy * (1 + compression_delta)
        
        # Store energy
        space_available = self.capacity - self.stored_energy
        energy_to_store = min(strengthened_energy, space_available)
        
        self.stored_energy += energy_to_store
        self.compression_level = new_compression
        
        # Update status
        fill_percentage = (self.stored_energy / self.capacity) * 100
        if fill_percentage >= 100:
            self.status = "charged"
        elif fill_percentage > 0:
            self.status = "filling"
        
        return {
            "battery_id": self.id,
            "stored_energy": self.stored_energy,
            "capacity": self.capacity,
            "fill_percentage": fill_percentage,
            "compression_level": self.compression_level,
            "status": self.status,
            "overflow": strengthened_energy - energy_to_store if strengthened_energy > energy_to_store else 0
        }
    
    def deploy(self) -> float:
        """Deploy the battery, releasing stored energy"""
        if self.status != "charged":
            return 0.0
        
        energy = self.stored_energy
        self.stored_energy = 0.0
        self.compression_level = 1.0
        self.status = "deployed"
        return energy

class BusNetwork:
    """Nexus highway - routes entropy with filtering"""
    
    def __init__(self):
        self.throughput = 0.0
        self.total_routed = 0.0
        self.filter_efficiency = 0.95  # 95% of data passes filter
    
    def route_entropy(self, entropy: float, source: str, destination: str) -> Dict:
        """Route entropy through the bus with filtering"""
        # Filter the data (Liver/Noms system)
        filtered_entropy = entropy * self.filter_efficiency
        filtered_out = entropy - filtered_entropy
        
        self.total_routed += filtered_entropy
        self.throughput = filtered_entropy
        
        return {
            "source": source,
            "destination": destination,
            "input_entropy": entropy,
            "filtered_entropy": filtered_entropy,
            "filtered_out": filtered_out,
            "filter_efficiency": self.filter_efficiency
        }

class CyberWorms:
    """Split behavior: feeders for Starheart, compressors for ZPMs"""
    
    def __init__(self):
        self.feeder_worms = 0
        self.compressor_worms = 0
        self.total_worms = 10  # Start with 10 worms
    
    def split_worms(self, starheart_active: bool):
        """Split worms based on Starheart status"""
        if starheart_active:
            # Once Starheart is active, split 70/30
            self.feeder_worms = int(self.total_worms * 0.7)
            self.compressor_worms = int(self.total_worms * 0.3)
        else:
            # Before Starheart ignition, all worms compress
            self.feeder_worms = 0
            self.compressor_worms = self.total_worms
    
    def multiply(self):
        """Worms multiply as system grows"""
        self.total_worms += 1

# Global engine instances
turbine_engine = TurbineEngine()
starheart_engine = StarheartEngine()
alternator = Alternator()
bus_network = BusNetwork()
cyber_worms = CyberWorms()

# ZPM battery pool
zpm_batteries: List[ZPMBattery] = [
    ZPMBattery(f"ZPM-{i}", capacity=100.0) for i in range(1, 6)
]
