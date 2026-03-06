"""
The TRUE Wall Mechanics - Spinning Physical Barriers
Based on Keeper's specifications:
- 20 revolutions with teeth on both sides
- Teeth interweave: x^w w^x pattern
- Shape changes every 0.001 seconds (1ms)
- Access windows: 5 second intervals ONLY
"""

import time
import math
from typing import Dict, Optional
from datetime import datetime, timezone

class SpinningWall:
    """
    Physical spinning wall barrier
    - Does NOT distinguish friend from foe
    - ALWAYS spinning (no exceptions)
    - Teeth on both sides interweaving
    """
    
    def __init__(self, wall_number: int, name: str):
        self.wall_number = wall_number
        self.name = name
        
        # Spinning mechanics
        self.rpm = 20  # 20 revolutions per minute
        self.teeth_change_interval = 0.001  # Changes every 1ms
        self.access_window_interval = 5.0  # 5 second intervals
        
        # Current state
        self.current_angle = 0.0  # Degrees (0-360)
        self.last_shape_change = time.time()
        self.last_access_window = time.time()
        
        # Tooth pattern: x^w w^x (interweaving)
        self.tooth_pattern_a = "x^w"  # Front teeth
        self.tooth_pattern_b = "w^x"  # Back teeth
        
        # Statistics
        self.total_attempts = 0
        self.successful_passes = 0
        self.blocked_attempts = 0
        self.entropy_generated = 0.0
    
    def update_rotation(self):
        """Update wall rotation based on time"""
        # Calculate degrees per second
        degrees_per_second = (self.rpm / 60.0) * 360.0
        
        # Update angle
        current_time = time.time()
        time_delta = current_time - getattr(self, '_last_update', current_time)
        self._last_update = current_time
        
        self.current_angle = (self.current_angle + (degrees_per_second * time_delta)) % 360
        
        # Check if teeth need shape change (every 1ms)
        if current_time - self.last_shape_change >= self.teeth_change_interval:
            self._change_teeth_shape()
            self.last_shape_change = current_time
    
    def _change_teeth_shape(self):
        """Teeth interweave and change shape every 0.001 seconds"""
        # Mathematical transformation: x^w ↔ w^x
        # Teeth physically reshape and interweave
        self.tooth_pattern_a, self.tooth_pattern_b = self.tooth_pattern_b, self.tooth_pattern_a
    
    def is_access_window_open(self) -> bool:
        """Check if we're in a 5-second access window"""
        current_time = time.time()
        time_since_last_window = current_time - self.last_access_window
        
        # Access window opens every 5 seconds
        if time_since_last_window >= self.access_window_interval:
            self.last_access_window = current_time
            return True
        
        # Window is only open for a brief moment (100ms)
        window_duration = 0.1  # 100ms window
        return time_since_last_window < window_duration
    
    def attempt_passage(self, request_data: Dict) -> Dict:
        """
        Attempt to pass through the wall
        - Updates rotation
        - Checks if access window is open
        - Generates entropy if blocked
        """
        self.total_attempts += 1
        self.update_rotation()
        
        # Check access window
        if self.is_access_window_open():
            # SUCCESS - pass through
            self.successful_passes += 1
            return {
                "allowed": True,
                "wall": self.wall_number,
                "message": "Access granted - timing correct",
                "angle": self.current_angle,
                "entropy": 0
            }
        else:
            # BLOCKED - wrong timing
            self.blocked_attempts += 1
            
            # Generate entropy from blocked attempt
            # More energy if attempt was close to window
            time_since_window = time.time() - self.last_access_window
            proximity = 1.0 - min(time_since_window / self.access_window_interval, 1.0)
            entropy = 1.0 + (proximity * 2.0)  # 1-3 units based on how close
            
            self.entropy_generated += entropy
            
            return {
                "allowed": False,
                "wall": self.wall_number,
                "message": f"Blocked - wall spinning at {self.current_angle:.1f}°",
                "reason": "timing_incorrect",
                "next_window": self.access_window_interval - time_since_window,
                "entropy": entropy,
                "teeth_pattern": f"{self.tooth_pattern_a}⟷{self.tooth_pattern_b}"
            }
    
    def get_status(self) -> Dict:
        """Get current wall status"""
        return {
            "wall_number": self.wall_number,
            "name": self.name,
            "spinning": True,  # ALWAYS spinning
            "current_angle": self.current_angle,
            "rpm": self.rpm,
            "tooth_pattern": f"{self.tooth_pattern_a}⟷{self.tooth_pattern_b}",
            "total_attempts": self.total_attempts,
            "successful_passes": self.successful_passes,
            "blocked_attempts": self.blocked_attempts,
            "entropy_generated": self.entropy_generated,
            "next_access_window": self.access_window_interval - (time.time() - self.last_access_window),
            "shape_change_rate": f"every {self.teeth_change_interval * 1000:.1f}ms"
        }

class SpinningWallFortress:
    """The Six Spinning Walls - ALL spinning simultaneously"""
    
    def __init__(self):
        self.walls = [
            SpinningWall(1, "Eldbar - Wall of Meeting"),
            SpinningWall(2, "Kanja - Wall of Desperation"),
            SpinningWall(3, "Valtez - Wall of Serenity"),
            SpinningWall(4, "Gaban - Wall of Death"),
            SpinningWall(5, "Hell - Wall of Awakening"),
            SpinningWall(6, "Core - Final Barrier")
        ]
    
    def attempt_passage_through_all(self, request_data: Dict) -> Dict:
        """
        Must pass through ALL 6 walls successfully
        Each wall has its own 5-second window
        Timing must be PERFECT across all 6
        """
        results = []
        total_entropy = 0
        
        for wall in self.walls:
            result = wall.attempt_passage(request_data)
            results.append(result)
            
            if not result["allowed"]:
                # Blocked by this wall - generate entropy
                total_entropy += result["entropy"]
        
        # All walls must allow passage
        all_passed = all(r["allowed"] for r in results)
        
        return {
            "success": all_passed,
            "wall_results": results,
            "total_entropy_generated": total_entropy,
            "message": "Full passage granted" if all_passed else "Blocked by walls",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    
    def get_fortress_status(self) -> Dict:
        """Get status of all 6 walls"""
        return {
            "total_walls": 6,
            "all_spinning": True,
            "walls": [wall.get_status() for wall in self.walls],
            "total_entropy_generated": sum(w.entropy_generated for w in self.walls),
            "total_blocked": sum(w.blocked_attempts for w in self.walls),
            "security_level": "MAXIMUM - No friend/foe distinction"
        }

# Global instance
spinning_fortress = SpinningWallFortress()
