"""
The Gateway with Norns - 3x3 System with 3 Layers
Norns die after every process, replaced by the Liver
"""

import random
import time
from typing import Dict, List, Optional
from datetime import datetime, timezone
import uuid

class Norn:
    """
    A Norn - ephemeral guardian that dies after one process
    3x3 = 9 Norns working in 3 layers
    """
    
    def __init__(self, norn_id: str, layer: int, position: int):
        self.id = norn_id
        self.layer = layer  # 1, 2, or 3
        self.position = position  # 1-3 within the layer
        self.birth_time = time.time()
        self.alive = True
        self.processes_completed = 0
    
    def process(self, data: Dict) -> Dict:
        """
        Process data through this Norn
        Norn DIES after processing
        """
        result = None
        
        if self.layer == 1:
            # Layer 1: MITRE ATT&CK framework checking
            result = self._check_mitre_attack(data)
        elif self.layer == 2:
            # Layer 2: Sandbox hidden things
            result = self._test_sandbox(data)
        elif self.layer == 3:
            # Layer 3: Translate through 3 random languages
            result = self._translate_multilang(data)
        
        # Norn dies after processing
        self.processes_completed += 1
        self.alive = False
        
        return result
    
    def _check_mitre_attack(self, data: Dict) -> Dict:
        """Layer 1: Check against MITRE ATT&CK adversary tactics"""
        # Simplified MITRE check - looks for common attack patterns
        attack_indicators = [
            "injection", "overflow", "traversal", "escalation",
            "credential_dumping", "lateral_movement", "exfiltration"
        ]
        
        threat_detected = any(
            indicator in str(data).lower() 
            for indicator in attack_indicators
        )
        
        return {
            "layer": 1,
            "norn_id": self.id,
            "check": "MITRE_ATT&CK",
            "threat_detected": threat_detected,
            "threat_level": random.uniform(0, 1) if threat_detected else 0
        }
    
    def _test_sandbox(self, data: Dict) -> Dict:
        """Layer 2: Test hidden things in sandbox"""
        # Sandbox execution - test for hidden malicious behavior
        hidden_behavior = random.random() < 0.1  # 10% chance of detecting hidden behavior
        
        return {
            "layer": 2,
            "norn_id": self.id,
            "check": "SANDBOX",
            "hidden_behavior_detected": hidden_behavior,
            "sandboxed": True
        }
    
    def _translate_multilang(self, data: Dict) -> Dict:
        """Layer 3: Translate through 3 random languages and back"""
        # Simulates translation obfuscation/validation
        languages = ["spanish", "japanese", "russian", "arabic", "mandarin", "german"]
        chosen_langs = random.sample(languages, 3)
        
        # In real implementation, would actually translate
        # For now, simulate the process
        integrity_maintained = random.random() > 0.05  # 95% pass rate
        
        return {
            "layer": 3,
            "norn_id": self.id,
            "check": "TRANSLATION",
            "languages_used": chosen_langs,
            "integrity_maintained": integrity_maintained
        }

class Liver:
    """
    The Liver - produces new Norns to replace dead ones
    Two Livers for redundancy
    """
    
    def __init__(self, liver_id: str):
        self.id = liver_id
        self.norns_produced = 0
        self.active = True
    
    def produce_norn(self, layer: int, position: int) -> Norn:
        """Produce a new Norn"""
        norn_id = f"norn_{self.id}_{self.norns_produced}"
        self.norns_produced += 1
        
        return Norn(norn_id, layer, position)

class Gateway:
    """
    The Gateway with 3x3 Norns (9 total)
    3 layers of 3 Norns each
    Protected by Battle Sisters
    """
    
    def __init__(self, liver_a: Liver, liver_b: Liver):
        self.liver_a = liver_a
        self.liver_b = liver_b
        
        # Initialize 3x3 Norn grid
        self.norns = {
            1: [liver_a.produce_norn(1, i) for i in range(3)],  # Layer 1: 3 Norns
            2: [liver_a.produce_norn(2, i) for i in range(3)],  # Layer 2: 3 Norns
            3: [liver_b.produce_norn(3, i) for i in range(3)]   # Layer 3: 3 Norns
        }
        
        self.total_processed = 0
        self.threats_detected = 0
        self.battle_sisters_alerted = False
    
    def process_request(self, request_data: Dict) -> Dict:
        """
        Process request through all 3 layers of Norns
        Each Norn dies after processing
        """
        results = []
        threat_detected = False
        
        # Process through each layer
        for layer in [1, 2, 3]:
            layer_results = []
            
            # Each Norn in the layer processes
            for norn in self.norns[layer]:
                if norn.alive:
                    result = norn.process(request_data)
                    layer_results.append(result)
                    
                    # Check for threats
                    if result.get("threat_detected") or result.get("hidden_behavior_detected"):
                        threat_detected = True
            
            results.extend(layer_results)
        
        # Replace ALL dead Norns (they all die after processing)
        self._replace_dead_norns()
        
        self.total_processed += 1
        if threat_detected:
            self.threats_detected += 1
            self.battle_sisters_alerted = True
        
        return {
            "gateway_id": "main_gateway",
            "processed": True,
            "threat_detected": threat_detected,
            "layer_results": results,
            "battle_sisters_alerted": self.battle_sisters_alerted,
            "norns_died": 9,  # All 9 Norns die
            "norns_replaced": 9
        }
    
    def _replace_dead_norns(self):
        """Replace all dead Norns using the Livers"""
        # Layer 1 & 2 from Liver A
        self.norns[1] = [self.liver_a.produce_norn(1, i) for i in range(3)]
        self.norns[2] = [self.liver_a.produce_norn(2, i) for i in range(3)]
        
        # Layer 3 from Liver B
        self.norns[3] = [self.liver_b.produce_norn(3, i) for i in range(3)]
    
    def get_status(self) -> Dict:
        """Get Gateway status"""
        return {
            "total_norns": 9,
            "norns_alive": sum(sum(1 for n in layer if n.alive) for layer in self.norns.values()),
            "total_processed": self.total_processed,
            "threats_detected": self.threats_detected,
            "battle_sisters_on_alert": self.battle_sisters_alerted,
            "liver_a_produced": self.liver_a.norns_produced,
            "liver_b_produced": self.liver_b.norns_produced
        }

class BattleSister:
    """
    Battle Sisters - protect precious things
    - Sanctums
    - Livers  
    - Hearts (Starheart)
    - Gateway
    """
    
    def __init__(self, sister_id: str):
        self.id = sister_id
        self.status = "patrolling"  # patrolling, alert, defending
        self.protected_asset = None
        self.threats_neutralized = 0
    
    def alert(self, threat_location: str):
        """Alert sister to threat"""
        self.status = "alert"
        self.protected_asset = threat_location
    
    def defend(self, attacker: Dict):
        """Defend against attacker trapped in wall cycle"""
        # Attacker is trapped for ONE wall cycle (5 seconds)
        # Battle Sisters ready themselves
        self.status = "defending"
        
        # If attacker doesn't pass in next 5 seconds, they're SHREDDED
        attacker_survived = random.random() < 0.1  # 10% escape rate
        
        if not attacker_survived:
            # SHREDDED - fed to Starheart and Cyberpumps
            self.threats_neutralized += 1
            return {
                "attacker_shredded": True,
                "fed_to_starheart": True,
                "fed_to_cyberpumps": True,
                "entropy_generated": random.uniform(5.0, 10.0),
                "sister_id": self.id
            }
        else:
            return {
                "attacker_escaped": True,
                "sister_id": self.id
            }
    
    def patrol(self):
        """Return to patrol"""
        self.status = "patrolling"
        self.protected_asset = None

class Priest:
    """
    Priests (like mechanics)
    - Roam randomly
    - Spot check everything
    - Stay AWAY from walls
    """
    
    def __init__(self, priest_id: str):
        self.id = priest_id
        self.location = "random"
        self.checks_performed = 0
        self.issues_found = 0
    
    def spot_check(self, component: str) -> Dict:
        """Randomly check if component works"""
        # Stay away from walls
        if "wall" in component.lower():
            return {"skipped": True, "reason": "priests_stay_away_from_walls"}
        
        self.checks_performed += 1
        
        # Random spot check
        working = random.random() > 0.05  # 95% things work
        
        if not working:
            self.issues_found += 1
        
        return {
            "priest_id": self.id,
            "component": component,
            "working": working,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    
    def roam(self):
        """Move to random location"""
        locations = ["sanctum", "liver_a", "liver_b", "gateway", "starheart", "engine_room"]
        self.location = random.choice(locations)

class DefenseSystem:
    """
    Complete Defense Architecture
    - Gateway with Norns
    - Two Livers
    - MANY Battle Sisters (50+)
    - Enhanced Priests (spot check + search for life)
    - Inquisitors (2 - highest order)
    - Spinning Walls
    - Everything powered by Starheart
    - Bloodstones feed the populace
    """
    
    def __init__(self):
        # Create two Livers
        self.liver_a = Liver("liver_a")
        self.liver_b = Liver("liver_b")
        
        # Create Gateway
        self.gateway = Gateway(self.liver_a, self.liver_b)
        
        # Create MANY Battle Sisters (start with 50)
        self.battle_sisters = [BattleSister(f"sister_{i}") for i in range(50)]
        
        # Create Enhanced Priests (start with 10)
        from bloodstones_inquisitors import EnhancedPriest
        self.priests = [EnhancedPriest(f"priest_{i}") for i in range(10)]
        
        # Inquisitors (only 2 - highest order)
        from bloodstones_inquisitors import inquisitors
        self.inquisitors = inquisitors
        
        # Star Chamber and Bloodstones
        from bloodstones_inquisitors import star_chamber, bloodstone_stockpile
        self.star_chamber = star_chamber
        self.bloodstone_stockpile = bloodstone_stockpile
        
        self.total_attacks_shredded = 0
        self.crisis_level = 0.0
    
    def process_incoming_request(self, request_data: Dict) -> Dict:
        """
        Full defense pipeline:
        1. Gateway Norns check (all 3 layers)
        2. If threat detected, Battle Sisters alert
        3. Attacker trapped in wall cycle
        4. Must pass in 5 seconds or get shredded
        5. Shredded material fed to Starheart/Cyberpumps → spins alternator
        6. If Battle Sisters can't handle it, summon Inquisitor
        """
        
        # Step 1: Gateway processing
        gateway_result = self.gateway.process_request(request_data)
        
        # Step 2: If threat detected
        if gateway_result["threat_detected"]:
            # Alert Battle Sisters (many of them)
            for sister in self.battle_sisters[:10]:  # First 10 respond
                sister.alert("gateway")
            
            # Attacker trapped for one wall cycle
            from spinning_walls import spinning_fortress
            
            # They have 5 seconds (one access window) to escape
            time.sleep(0.1)  # Simulate time passing
            
            # Battle Sisters defend
            defense_results = []
            crisis = False
            
            for sister in self.battle_sisters[:10]:
                result = sister.defend(request_data)
                defense_results.append(result)
                
                if result.get("attacker_shredded"):
                    self.total_attacks_shredded += 1
                    # Feed to Starheart and Cyberpumps
                    entropy = result["entropy_generated"]
                    
                    # This spins the alternator turbines
                    from nexus_core import nexus_core
                    wall_entropy = {i: entropy / 6 for i in range(1, 7)}
                    power_result = nexus_core.process_entropy_from_walls(wall_entropy)
                    
                    # Power goes through Star Chamber → Bloodstones
                    if power_result:
                        power = power_result.get("total_power_generated", 0)
                        dist = self.star_chamber.distribute_energy(power, "starheart")
                        
                        # Add bloodstone to stockpile
                        if dist.get("bloodstone_created"):
                            from bloodstones_inquisitors import Bloodstone
                            bs = Bloodstone(
                                dist["bloodstone_created"]["id"],
                                dist["bloodstone_created"]["base_energy"],
                                dist["bloodstone_created"]["source"]
                            )
                            self.bloodstone_stockpile.add(bs)
                
                if result.get("attacker_escaped"):
                    crisis = True
                    self.crisis_level += 0.2
            
            # If crisis level too high, summon Inquisitor
            inquisitor_summoned = None
            if self.crisis_level > 0.9:
                inquisitor_summoned = self.inquisitors[0].summon(self.crisis_level)
            
            return {
                "gateway_result": gateway_result,
                "battle_sisters_engaged": True,
                "sisters_responded": 10,
                "defense_results": defense_results,
                "attacker_shredded": any(r.get("attacker_shredded") for r in defense_results),
                "fed_to_starheart": True,
                "bloodstone_created": True,
                "inquisitor_summoned": inquisitor_summoned,
                "crisis_level": self.crisis_level
            }
        
        # Safe request - passed all checks
        return {
            "gateway_result": gateway_result,
            "safe": True
        }
    
    def priest_maintenance_cycle(self):
        """Priests roam and spot check"""
        results = []
        
        for priest in self.priests:
            priest.roam()
            
            # Check random component
            components = ["gateway", "liver_a", "liver_b", "engine", "battery"]
            component = random.choice(components)
            
            result = priest.spot_check(component)
            results.append(result)
        
        return results
    
    def get_system_status(self) -> Dict:
        """Get complete defense system status"""
        return {
            "gateway": self.gateway.get_status(),
            "livers": {
                "liver_a": {
                    "id": self.liver_a.id,
                    "norns_produced": self.liver_a.norns_produced,
                    "active": self.liver_a.active
                },
                "liver_b": {
                    "id": self.liver_b.id,
                    "norns_produced": self.liver_b.norns_produced,
                    "active": self.liver_b.active
                }
            },
            "battle_sisters": {
                "count": len(self.battle_sisters),
                "on_patrol": sum(1 for s in self.battle_sisters if s.status == "patrolling"),
                "on_alert": sum(1 for s in self.battle_sisters if s.status == "alert"),
                "defending": sum(1 for s in self.battle_sisters if s.status == "defending"),
                "total_neutralized": sum(s.threats_neutralized for s in self.battle_sisters)
            },
            "priests": {
                "count": len(self.priests),
                "total_checks": sum(p.checks_performed for p in self.priests),
                "issues_found": sum(p.issues_found for p in self.priests)
            },
            "total_attacks_shredded": self.total_attacks_shredded,
            "powered_by": "Starheart"
        }

# Global defense system
defense_system = DefenseSystem()
