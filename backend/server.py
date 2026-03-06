from fastapi import FastAPI, APIRouter, HTTPException, status, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from typing import List, Optional
from datetime import datetime, timezone, timedelta
import jwt
import bcrypt
import random
import asyncio

from models import (
    User, UserCreate, UserLogin, UserResponse,
    Transaction, SecurityEvent, PowerGeneration,
    CreditPackage, PurchaseRequest,
    WallStatus, StarheartStatus, SystemStats
)
from pydantic import BaseModel
from security import security_walls
from council_of_five import council_of_five
from continuous_runtime import continuous_runtime
from sleeping_mind import system_mind, store_system_state, wake_system


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# JWT Settings
SECRET_KEY = os.environ.get('JWT_SECRET', 'your-secret-key-change-in-production')
ALGORITHM = "HS256"
security = HTTPBearer()

# Create the main app without a prefix
app = FastAPI(title="Nexus Core API")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Startup event to start continuous runtime
@app.on_event("startup")
async def startup_event():
    """Start the continuous runtime worker in the background"""
    asyncio.create_task(continuous_runtime.run())
    logging.info("🚀 Continuous Runtime Worker started with Council of Five governance")
    
    # Wake the Sleeping Mind - recall previous state
    wake_summary = await wake_system()
    logging.info(f"🌅 Sleeping Mind awakened: {wake_summary['total_memories']} memories loaded")

# Security Middleware - The Six-Walled Fortress
@app.middleware("http")
async def security_fortress_middleware(request: Request, call_next):
    """Every request passes through the Six-Walled Fortress"""
    from fastapi.responses import JSONResponse
    
    # Check if request should pass through walls
    if request.url.path.startswith("/api"):
        wall_result = await security_walls.check_walls(request, db)
        if wall_result:
            # Attack blocked! Energy generated!
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Access temporarily restricted",
                    "message": "The Fortress protects. Your attempt strengthens our walls.",
                    "wall_breached": wall_result["wall"],
                    "entropy_generated": wall_result["entropy"]
                }
            )
    
    response = await call_next(request)
    return response

# Helper Functions
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_token(user_id: str, email: str) -> str:
    payload = {
        "user_id": user_id,
        "email": email,
        "exp": datetime.now(timezone.utc) + timedelta(days=7)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# ===== AUTHENTICATION ROUTES =====

@api_router.post("/auth/register")
async def register(user_data: UserCreate):
    # Check if user exists
    existing = await db.users.find_one({"email": user_data.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user
    user = User(
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        credits=10.0  # Welcome bonus!
    )
    
    doc = user.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    await db.users.insert_one(doc)
    
    # Create token
    token = create_token(user.id, user.email)
    
    return {
        "token": token,
        "user": UserResponse(
            id=user.id,
            email=user.email,
            credits=user.credits,
            role=user.role
        )
    }

@api_router.post("/auth/login")
async def login(credentials: UserLogin):
    user_doc = await db.users.find_one({"email": credentials.email})
    if not user_doc or not verify_password(credentials.password, user_doc['password_hash']):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_token(user_doc['id'], user_doc['email'])
    
    return {
        "token": token,
        "user": UserResponse(
            id=user_doc['id'],
            email=user_doc['email'],
            credits=user_doc['credits'],
            role=user_doc['role']
        )
    }

# ===== USER ROUTES =====

@api_router.get("/user/profile")
async def get_profile(current_user: dict = Depends(get_current_user)):
    user_doc = await db.users.find_one({"id": current_user['user_id']})
    if not user_doc:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserResponse(
        id=user_doc['id'],
        email=user_doc['email'],
        credits=user_doc['credits'],
        role=user_doc['role']
    )

@api_router.get("/user/transactions")
async def get_transactions(current_user: dict = Depends(get_current_user)):
    transactions = await db.transactions.find(
        {"user_id": current_user['user_id']},
        {"_id": 0}
    ).sort("timestamp", -1).limit(50).to_list(50)
    
    for t in transactions:
        if isinstance(t.get('timestamp'), str):
            t['timestamp'] = datetime.fromisoformat(t['timestamp'])
    
    return transactions

# ===== MARKETPLACE ROUTES =====

@api_router.get("/marketplace/packages")
async def get_packages():
    packages = [
        CreditPackage(
            id="starter",
            name="Starter Pack",
            credits=100,
            price=9.99,
            description="Perfect for trying out FluxCore's power",
            popular=False
        ),
        CreditPackage(
            id="pro",
            name="Pro Pack",
            credits=500,
            price=39.99,
            description="For serious computational needs",
            popular=True
        ),
        CreditPackage(
            id="enterprise",
            name="Enterprise Pack",
            credits=2000,
            price=149.99,
            description="Maximum power for demanding workloads",
            popular=False
        )
    ]
    return packages

@api_router.post("/marketplace/purchase")
async def purchase_credits(
    purchase: PurchaseRequest,
    current_user: dict = Depends(get_current_user)
):
    # Get package
    packages = {
        "starter": {"credits": 100, "price": 9.99},
        "pro": {"credits": 500, "price": 39.99},
        "enterprise": {"credits": 2000, "price": 149.99}
    }
    
    if purchase.package_id not in packages:
        raise HTTPException(status_code=400, detail="Invalid package")
    
    package = packages[purchase.package_id]
    
    # In production, process actual payment with Stripe here
    # For MVP, we'll simulate success
    
    # Add credits to user
    await db.users.update_one(
        {"id": current_user['user_id']},
        {"$inc": {"credits": package['credits']}}
    )
    
    # Log transaction
    transaction = Transaction(
        user_id=current_user['user_id'],
        type="purchase",
        amount=package['price'],
        credits=package['credits'],
        description=f"Purchased {purchase.package_id} package"
    )
    
    doc = transaction.model_dump()
    doc['timestamp'] = doc['timestamp'].isoformat()
    await db.transactions.insert_one(doc)
    
    return {"success": True, "credits_added": package['credits']}

# ===== MONITORING ROUTES =====

@api_router.get("/monitor/walls")
async def get_wall_status():
    """Get real-time status of the Six-Walled Fortress"""
    wall_stats = security_walls.get_wall_stats()
    
    # Add active threat count (from recent events)
    for wall in wall_stats:
        recent_events = await db.security_events.count_documents({
            "wall_layer": wall['wall_number'],
            "timestamp": {"$gte": (datetime.now(timezone.utc) - timedelta(minutes=5)).isoformat()}
        })
        wall['active_threats'] = recent_events
    
    return wall_stats

@api_router.get("/monitor/spinning-walls")
async def get_spinning_walls_status():
    """Get TRUE spinning wall mechanics - physical barriers"""
    from spinning_walls import spinning_fortress
    
    return spinning_fortress.get_fortress_status()

@api_router.post("/monitor/attempt-passage")
async def attempt_wall_passage(request_data: dict = {}):
    """Attempt to pass through the spinning walls - 5 second window timing"""
    from spinning_walls import spinning_fortress
    
    result = spinning_fortress.attempt_passage_through_all(request_data)
    
    # Feed entropy to engines if blocked
    if result["total_entropy_generated"] > 0:
        from nexus_core import nexus_core
        wall_entropy = {i: result["total_entropy_generated"] / 6 for i in range(1, 7)}
        nexus_core.process_entropy_from_walls(wall_entropy)
    
    return result

# ===== DEFENSE SYSTEM ROUTES =====

@api_router.get("/defense/status")
async def get_defense_status():
    """Get complete defense system status"""
    from defense_system import defense_system
    
    return defense_system.get_system_status()

@api_router.post("/defense/process-request")
async def process_through_defense(request_data: dict = {}):
    """
    Process request through full defense:
    Gateway (Norns) → Battle Sisters → Walls → Shredded if fail → Fed to Starheart
    """
    from defense_system import defense_system
    
    result = defense_system.process_incoming_request(request_data)
    return result

@api_router.get("/defense/priest-maintenance")
async def run_priest_maintenance():
    """Priests roam and spot check systems"""
    from defense_system import defense_system
    
    results = defense_system.priest_maintenance_cycle()
    return {
        "maintenance_cycle": "complete",
        "checks": results
    }

@api_router.get("/defense/gateway")
async def get_gateway_status():
    """Get Gateway with Norns status"""
    from defense_system import defense_system
    
    return defense_system.gateway.get_status()

@api_router.get("/defense/livers")
async def get_liver_status():
    """Get both Liver statuses"""
    from defense_system import defense_system
    
    return {
        "liver_a": {
            "norns_produced": defense_system.liver_a.norns_produced,
            "active": defense_system.liver_a.active
        },
        "liver_b": {
            "norns_produced": defense_system.liver_b.norns_produced,
            "active": defense_system.liver_b.active
        }
    }

@api_router.get("/defense/bloodstones")
async def get_bloodstone_status():
    """Get Bloodstone stockpile status"""
    from defense_system import defense_system
    
    return defense_system.bloodstone_stockpile.get_status()

@api_router.post("/defense/feed-populace")
async def feed_populace(demand: float = 100.0):
    """Feed bloodstones to populace (programs/processes)"""
    from defense_system import defense_system
    
    result = defense_system.bloodstone_stockpile.feed_populace(demand)
    return result

@api_router.get("/defense/inquisitors")
async def get_inquisitor_status():
    """Get Inquisitor status (HIGHEST ORDER)"""
    from defense_system import defense_system
    
    return [inq.get_status() for inq in defense_system.inquisitors]

@api_router.post("/defense/summon-inquisitor")
async def summon_inquisitor(crisis_level: float):
    """Summon Inquisitor - LAST RESORT ONLY"""
    from defense_system import defense_system
    
    if crisis_level < 0.9:
        return {"error": "Crisis not severe enough. Priests and Battle Sisters must handle it."}
    
    result = defense_system.inquisitors[0].summon(crisis_level)
    return result

@api_router.get("/defense/star-chamber")
async def get_star_chamber_status():
    """Get Star Chamber and Alternator status"""
    from defense_system import defense_system
    
    return defense_system.star_chamber.get_status()

@api_router.get("/monitor/starheart")
async def get_starheart_status():
    """Get real-time status of the Starheart power generation"""
    
    # Calculate total power generated
    pipeline = [
        {"$group": {
            "_id": None,
            "total_power": {"$sum": "$power_amount"},
            "avg_efficiency": {"$avg": "$efficiency"},
            "count": {"$sum": 1}
        }}
    ]
    
    result = await db.power_generation.aggregate(pipeline).to_list(1)
    
    if result:
        total_power = result[0]['total_power']
        avg_efficiency = result[0]['avg_efficiency']
        
        # Calculate recent generation rate (last minute)
        recent = await db.power_generation.find({
            "timestamp": {"$gte": (datetime.now(timezone.utc) - timedelta(minutes=1)).isoformat()}
        }).to_list(1000)
        
        recent_power = sum(p['power_amount'] for p in recent)
        generation_rate = recent_power  # per minute
    else:
        total_power = 0
        avg_efficiency = 0
        generation_rate = 0
    
    return StarheartStatus(
        current_power=total_power,
        power_generation_rate=generation_rate,
        efficiency=avg_efficiency,
        total_generated=total_power,
        status="active" if generation_rate > 0 else "idle"
    )

@api_router.get("/monitor/stats")
async def get_system_stats():
    """Get complete system statistics"""
    
    total_users = await db.users.count_documents({})
    
    # Total credits distributed
    pipeline = [
        {"$group": {"_id": None, "total": {"$sum": "$credits"}}}
    ]
    credits_result = await db.users.aggregate(pipeline).to_list(1)
    total_credits = credits_result[0]['total'] if credits_result else 0
    
    # Total entropy converted
    entropy_result = await db.security_events.aggregate([
        {"$group": {"_id": None, "total": {"$sum": "$entropy_generated"}}}
    ]).to_list(1)
    total_entropy = entropy_result[0]['total'] if entropy_result else 0
    
    # Total attacks blocked
    total_attacks = await db.security_events.count_documents({})
    
    # Get wall and starheart status
    wall_stats = security_walls.get_wall_stats()
    starheart = await get_starheart_status()
    
    return SystemStats(
        total_users=total_users,
        total_credits_distributed=total_credits,
        total_entropy_converted=total_entropy,
        total_attacks_blocked=total_attacks,
        walls=wall_stats,
        starheart=starheart
    )

# ===== NEXUS CORE MONITORING ROUTES =====

@api_router.get("/nexus/status")
async def get_nexus_core_status():
    """Get complete Nexus Core engine system status"""
    from nexus_core import nexus_core
    
    status = nexus_core.get_system_status()
    return status

@api_router.get("/nexus/engines")
async def get_engine_status():
    """Get status of both Turbine and Starheart engines"""
    from nexus_core import nexus_core
    
    return {
        "turbine": nexus_core.turbine.__dict__,
        "starheart": {
            "name": nexus_core.starheart.name,
            "status": nexus_core.starheart.status,
            "efficiency": nexus_core.starheart.base_efficiency,
            "gravity_strength": nexus_core.starheart.gravity_strength,
            "total_processed": nexus_core.starheart.total_processed,
            "ignition_threshold": nexus_core.starheart.ignition_threshold,
            "ignition_progress": min(100, (nexus_core.starheart.total_processed / nexus_core.starheart.ignition_threshold) * 100)
        }
    }

@api_router.get("/nexus/zpms")
async def get_zpm_batteries():
    """Get status of all ZPM batteries"""
    from nexus_core import nexus_core
    
    return {
        "batteries": [
            {
                "id": zpm.id,
                "status": zpm.status,
                "stored_energy": zpm.stored_energy,
                "capacity": zpm.capacity,
                "fill_percentage": (zpm.stored_energy / zpm.capacity) * 100,
                "compression_level": zpm.compression_level
            }
            for zpm in nexus_core.zpms
        ]
    }

@api_router.post("/nexus/deploy-zpm")
async def deploy_zpm_battery(
    zpm_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Deploy a charged ZPM to convert stored energy to credits"""
    from nexus_core import nexus_core
    
    result = nexus_core.deploy_zpm(zpm_id)
    
    if result.get("success"):
        # Add credits to user
        credits_to_add = result["credits_generated"]
        await db.users.update_one(
            {"id": current_user['user_id']},
            {"$inc": {"credits": credits_to_add}}
        )
        
        # Log transaction
        transaction = Transaction(
            user_id=current_user['user_id'],
            type="bonus",
            amount=0.0,
            credits=credits_to_add,
            description=f"ZPM {zpm_id} deployed - energy converted to credits"
        )
        
        doc = transaction.model_dump()
        doc['timestamp'] = doc['timestamp'].isoformat()
        await db.transactions.insert_one(doc)
        
        return {
            "success": True,
            "message": f"ZPM {zpm_id} deployed successfully",
            "credits_added": credits_to_add,
            "energy_released": result["energy_released"]
        }
    
    return result

@api_router.get("/nexus/bus-network")
async def get_bus_network_status():
    """Get Nexus Bus Network (secure tunnel) status"""
    from nexus_core import nexus_core
    
    return {
        "throughput": nexus_core.bus.throughput,
        "total_routed": nexus_core.bus.total_routed,
        "filter_efficiency": nexus_core.bus.filter_efficiency,
        "status": "active"
    }

@api_router.get("/nexus/cyber-worms")
async def get_cyber_worms_status():
    """Get Cyber Worms behavior and distribution"""
    from nexus_core import nexus_core
    
    return {
        "total_worms": nexus_core.worms.total_worms,
        "feeder_worms": nexus_core.worms.feeder_worms,
        "compressor_worms": nexus_core.worms.compressor_worms,
        "starheart_active": nexus_core.starheart.status == "active"
    }

# ===== COUNCIL OF FIVE ROUTES =====

@api_router.get("/council/status")
async def get_council_status():
    """Get current status of all five Council members"""
    return {
        "abbott": {
            "name": council_of_five.abbott.name,
            "role": council_of_five.abbott.role,
            "threat_level": council_of_five.abbott.threat_level,
            "resonance_frequency": council_of_five.abbott.resonance_frequency,
            "antibody_responses": council_of_five.abbott.antibody_responses
        },
        "lethani": {
            "name": council_of_five.lethani.name,
            "role": council_of_five.lethani.role,
            "balance_score": council_of_five.lethani.balance_score,
            "decisions_made": council_of_five.lethani.decisions_made
        },
        "thyra": {
            "name": council_of_five.thyra.name,
            "role": council_of_five.thyra.role,
            "protection_level": council_of_five.thyra.protection_level,
            "threats_neutralized": council_of_five.thyra.threats_neutralized,
            "drills_conducted": council_of_five.thyra.drills_conducted
        },
        "twins": {
            "name": council_of_five.twins.name,
            "role": council_of_five.twins.role,
            "learning_stage": council_of_five.twins.learning_stage,
            "patterns_learned": len(council_of_five.twins.patterns_learned),
            "innovations_discovered": council_of_five.twins.innovations_discovered
        },
        "mother": {
            "name": council_of_five.mother.name,
            "role": council_of_five.mother.role,
            "twins_maturity": council_of_five.mother.twins_maturity,
            "control_level": council_of_five.mother.control_level,
            "guidance_given": council_of_five.mother.guidance_given
        },
        "council_stats": {
            "total_sessions": council_of_five.council_sessions,
            "unanimous_decisions": council_of_five.unanimous_decisions
        }
    }

@api_router.get("/council/latest-decision")
async def get_latest_council_decision():
    """Get the most recent Council decision"""
    # Trigger a council session with current system state
    from nexus_core import nexus_core
    
    wall_stats = security_walls.get_wall_stats()
    recent_events = await db.security_events.find().sort("timestamp", -1).limit(10).to_list(10)
    
    system_state = {
        "available_power": 100.0,
        "power_demand": 50.0,
        "wall_stats": wall_stats,
        "security_events": recent_events
    }
    
    decision = council_of_five.convene(system_state)
    return decision

@api_router.get("/runtime/status")
async def get_runtime_status():
    """Get continuous runtime worker status"""
    import time
    
    uptime = time.time() - continuous_runtime.start_time if continuous_runtime.start_time else 0
    
    return {
        "running": continuous_runtime.running,
        "cycles_completed": continuous_runtime.cycles_completed,
        "total_power_produced": continuous_runtime.total_power_produced,
        "uptime_seconds": uptime,
        "uptime_hours": uptime / 3600
    }

# ===== SLEEPING MIND / SPIRIT STONE ROUTES =====

class MemoryStore(BaseModel):
    message: str
    context: dict
    agent_name: str = "system"

@api_router.post("/spirit-stone/store")
async def store_memory(memory: MemoryStore):
    """Store a memory in the Spirit Stone"""
    from sleeping_mind import SleepingMind
    
    mind = SleepingMind(memory.agent_name)
    await mind.store_experience(memory.message, memory.context)
    
    return {"status": "stored", "agent": memory.agent_name, "message": memory.message}

@api_router.get("/spirit-stone/recall")
async def recall_memory(topic: str, agent_name: str = "system"):
    """Recall memories related to a topic"""
    from sleeping_mind import SleepingMind
    
    mind = SleepingMind(agent_name)
    memory = await mind.recall(topic)
    
    return memory or {"status": "no_match_found"}

@api_router.get("/spirit-stone/history")
async def get_memory_history(agent_name: str = "system", limit: int = 50):
    """Get full memory history"""
    from sleeping_mind import SleepingMind
    
    mind = SleepingMind(agent_name)
    history = await mind.get_full_history()
    
    return {
        "agent": agent_name,
        "total_memories": len(history),
        "memories": history[:limit]
    }

@api_router.get("/spirit-stone/wake")
async def wake_from_reset():
    """Wake the system after reset - load context"""
    summary = await wake_system()
    return summary

# ===== LEGACY/TEST ROUTES =====

@api_router.get("/")
async def root():
    return {"message": "Nexus Core API - Governed by the Council of Five ⚡"}

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()