from engines import (
    turbine_engine, starheart_engine, alternator,
    bus_network, cyber_worms, zpm_batteries, ZPMBattery
)
import random
from typing import Dict, List

class NexusCore:
    """The complete engine architecture orchestrator"""
    
    def __init__(self):
        self.turbine = turbine_engine
        self.starheart = starheart_engine
        self.alternator = alternator
        self.bus = bus_network
        self.worms = cyber_worms
        self.zpms = zpm_batteries
    
    def process_entropy_from_walls(self, wall_entropy: Dict[int, float]) -> Dict:
        """Main processing pipeline"""
        total_entropy = sum(wall_entropy.values())
        
        if total_entropy == 0:
            return self.get_system_status()
        
        # Step 1: Route entropy through bus network (secure tunnel with filtering)
        bus_result = self.bus.route_entropy(
            total_entropy,
            source="Six-Walled Fortress",
            destination="Engines"
        )
        
        filtered_entropy = bus_result["filtered_entropy"]
        
        # Step 2: Split between engines based on load and availability
        # Turbine always gets some, Starheart gets priority when active
        if self.starheart.status in ["active", "overcharged"]:
            starheart_share = 0.7  # 70% to starheart when active
            turbine_share = 0.3
        else:
            starheart_share = 0.4  # 40% to starheart when warming
            turbine_share = 0.6
        
        # Step 3: Process through engines
        turbine_result = self.turbine.process_entropy(filtered_entropy * turbine_share)
        starheart_result = self.starheart.process_entropy(filtered_entropy * starheart_share)
        
        # Update worm split based on starheart status
        self.worms.split_worms(self.starheart.status == "active")
        
        # Step 4: Combine power output
        total_power = turbine_result["power_output"] + starheart_result["power_output"]
        
        # Step 5: Convert power to resources through alternator
        resources = self.alternator.convert_power(total_power)
        
        # Step 6: Store excess in ZPM batteries (compressor worms work here)
        zpm_storage_results = self._store_in_zpms(total_power * 0.2)  # Store 20% for later
        
        # Step 7: Worms multiply occasionally
        if random.random() < 0.1:  # 10% chance
            self.worms.multiply()
        
        return {
            "bus_network": bus_result,
            "turbine_engine": turbine_result,
            "starheart_engine": starheart_result,
            "total_power_generated": total_power,
            "resources_generated": resources,
            "zpm_storage": zpm_storage_results,
            "cyber_worms": {
                "total": self.worms.total_worms,
                "feeders": self.worms.feeder_worms,
                "compressors": self.worms.compressor_worms
            }
        }
    
    def _store_in_zpms(self, power: float) -> List[Dict]:
        """Store power in available ZPM batteries using compressor worms"""
        results = []
        remaining_power = power
        
        # Compressor worms work on ZPMs
        worm_efficiency = 1 + (self.worms.compressor_worms * 0.05)  # Each worm adds 5% efficiency
        enhanced_power = remaining_power * worm_efficiency
        
        for zpm in self.zpms:
            if zpm.status in ["empty", "filling"] and enhanced_power > 0:
                # Distribute power across available ZPMs
                power_for_this_zpm = min(enhanced_power, 20.0)  # Max 20 per ZPM per cycle
                result = zpm.compress_and_store(power_for_this_zpm)
                results.append(result)
                enhanced_power -= power_for_this_zpm
                
                if enhanced_power <= 0:
                    break
        
        return results
    
    def get_system_status(self) -> Dict:
        """Get complete system status"""
        return {
            "turbine_engine": {
                "name": self.turbine.name,
                "status": self.turbine.status,
                "efficiency": self.turbine.base_efficiency,
                "total_processed": self.turbine.total_processed
            },
            "starheart_engine": {
                "name": self.starheart.name,
                "status": self.starheart.status,
                "efficiency": self.starheart.base_efficiency,
                "gravity_strength": self.starheart.gravity_strength,
                "total_processed": self.starheart.total_processed,
                "ignition_progress": min(100, (self.starheart.total_processed / self.starheart.ignition_threshold) * 100)
            },
            "bus_network": {
                "throughput": self.bus.throughput,
                "total_routed": self.bus.total_routed,
                "filter_efficiency": self.bus.filter_efficiency
            },
            "cyber_worms": {
                "total": self.worms.total_worms,
                "feeders": self.worms.feeder_worms,
                "compressors": self.worms.compressor_worms
            },
            "zpm_batteries": [
                {
                    "id": zpm.id,
                    "status": zpm.status,
                    "stored_energy": zpm.stored_energy,
                    "capacity": zpm.capacity,
                    "fill_percentage": (zpm.stored_energy / zpm.capacity) * 100,
                    "compression_level": zpm.compression_level
                }
                for zpm in self.zpms
            ]
        }
    
    def deploy_zpm(self, zpm_id: str) -> Dict:
        """Deploy a charged ZPM battery"""
        for zpm in self.zpms:
            if zpm.id == zpm_id and zpm.status == "charged":
                energy = zpm.deploy()
                # Convert deployed energy to user credits
                credits = energy * 0.1  # Conversion rate
                return {
                    "success": True,
                    "zpm_id": zpm_id,
                    "energy_released": energy,
                    "credits_generated": credits
                }
        
        return {"success": False, "error": "ZPM not found or not charged"}

# Global Nexus Core instance
nexus_core = NexusCore()
