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

from models import (
    User, UserCreate, UserLogin, UserResponse,
    Transaction, SecurityEvent, PowerGeneration,
    CreditPackage, PurchaseRequest,
    WallStatus, StarheartStatus, SystemStats
)
from security import security_walls


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
app = FastAPI(title="FluxCore API")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

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

# ===== LEGACY/TEST ROUTES =====

@api_router.get("/")
async def root():
    return {"message": "FluxCore API - Where attacks become power ⚡"}

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