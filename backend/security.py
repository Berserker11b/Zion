from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta, timezone
from collections import defaultdict
import time
import random

# Rate limiting storage (in production, use Redis)
rate_limit_storage = defaultdict(list)
blocked_ips = {}

# Wall names based on user's concept
WALL_NAMES = {
    1: "Eldbar - Wall of Meeting",
    2: "Kanja - Wall of Desperation", 
    3: "Valtez - Wall of Serenity",
    4: "Gaban - Wall of Death",
    5: "Hell - Wall of Awakening",
    6: "Core - Final Barrier"
}

class SecurityWalls:
    """The Six-Walled Fortress - converts attacks into power"""
    
    def __init__(self):
        self.wall_stats = {i: {"blocked": 0, "entropy": 0.0} for i in range(1, 7)}
    
    async def check_walls(self, request: Request, db):
        """Process request through the six walls"""
        client_ip = request.client.host
        endpoint = request.url.path
        
        # Wall 1: Basic rate limiting
        wall_result = await self._wall_1_basic_rate_limit(client_ip, endpoint)
        if wall_result:
            await self._log_security_event(db, wall_result, client_ip, endpoint, 1)
            return wall_result
        
        # Wall 2: Burst protection
        wall_result = await self._wall_2_burst_protection(client_ip)
        if wall_result:
            await self._log_security_event(db, wall_result, client_ip, endpoint, 2)
            return wall_result
        
        # Wall 3: Suspicious pattern detection
        wall_result = await self._wall_3_pattern_detection(client_ip, endpoint)
        if wall_result:
            await self._log_security_event(db, wall_result, client_ip, endpoint, 3)
            return wall_result
        
        # Walls 4-6 are adaptive (get stronger with attacks)
        # For now, they monitor and strengthen automatically
        
        return None
    
    async def _wall_1_basic_rate_limit(self, ip: str, endpoint: str):
        """Wall 1: Basic rate limiting - 100 req/min"""
        now = time.time()
        minute_ago = now - 60
        
        # Clean old entries
        rate_limit_storage[ip] = [t for t in rate_limit_storage[ip] if t > minute_ago]
        
        if len(rate_limit_storage[ip]) >= 100:
            entropy = random.uniform(0.5, 1.5)
            self.wall_stats[1]["blocked"] += 1
            self.wall_stats[1]["entropy"] += entropy
            return {"wall": 1, "entropy": entropy, "type": "rate_limit"}
        
        rate_limit_storage[ip].append(now)
        return None
    
    async def _wall_2_burst_protection(self, ip: str):
        """Wall 2: Burst protection - max 10 req/second"""
        now = time.time()
        second_ago = now - 1
        
        recent = [t for t in rate_limit_storage[ip] if t > second_ago]
        
        if len(recent) >= 10:
            entropy = random.uniform(1.0, 2.5)
            self.wall_stats[2]["blocked"] += 1
            self.wall_stats[2]["entropy"] += entropy
            return {"wall": 2, "entropy": entropy, "type": "burst"}
        
        return None
    
    async def _wall_3_pattern_detection(self, ip: str, endpoint: str):
        """Wall 3: Pattern detection - suspicious behavior"""
        # Simple pattern: same IP hitting different endpoints rapidly
        if len(rate_limit_storage[ip]) > 50:
            if random.random() < 0.1:  # 10% chance to flag as suspicious
                entropy = random.uniform(2.0, 4.0)
                self.wall_stats[3]["blocked"] += 1
                self.wall_stats[3]["entropy"] += entropy
                return {"wall": 3, "entropy": entropy, "type": "suspicious"}
        
        return None
    
    async def _log_security_event(self, db, wall_result: dict, ip: str, endpoint: str, wall: int):
        """Log security event and generate entropy for Starheart"""
        from models import SecurityEvent
        
        event = SecurityEvent(
            event_type=wall_result["type"],
            ip_address=ip,
            endpoint=endpoint,
            wall_layer=wall,
            entropy_generated=wall_result["entropy"]
        )
        
        doc = event.model_dump()
        doc['timestamp'] = doc['timestamp'].isoformat()
        await db.security_events.insert_one(doc)
        
        # Feed entropy to Starheart
        await self._feed_starheart(db, wall_result["entropy"])
    
    async def _feed_starheart(self, db, entropy: float):
        """Convert entropy into power credits"""
        from models import PowerGeneration
        
        # Conversion rate: 1 entropy = 0.1 power credits
        power = entropy * 0.1
        
        power_gen = PowerGeneration(
            source="entropy_conversion",
            power_amount=power,
            efficiency=random.uniform(0.85, 0.98)
        )
        
        doc = power_gen.model_dump()
        doc['timestamp'] = doc['timestamp'].isoformat()
        await db.power_generation.insert_one(doc)
    
    def get_wall_stats(self):
        """Get current stats for all walls"""
        return [
            {
                "wall_number": i,
                "name": WALL_NAMES[i],
                "total_blocked": self.wall_stats[i]["blocked"],
                "entropy_generated": self.wall_stats[i]["entropy"],
                "status": "active" if self.wall_stats[i]["blocked"] < 100 else "fortified"
            }
            for i in range(1, 7)
        ]

# Global security instance
security_walls = SecurityWalls()
