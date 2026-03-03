from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional, List, Literal
from datetime import datetime, timezone
import uuid

# User Models
class User(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: EmailStr
    password_hash: str
    credits: float = Field(default=0.0)
    role: Literal["user", "admin"] = "user"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    credits: float
    role: str

# Transaction Models
class Transaction(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    type: Literal["purchase", "usage", "bonus"]
    amount: float
    credits: float
    description: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# Security Event Models (Wall Activity)
class SecurityEvent(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_type: Literal["rate_limit", "blocked", "suspicious", "ddos_attempt"]
    ip_address: str
    endpoint: str
    wall_layer: int  # 1-6 representing which wall caught it
    entropy_generated: float
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# Power Generation Models (Starheart)
class PowerGeneration(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    source: Literal["entropy_conversion", "system_optimization", "idle_resources"]
    power_amount: float
    efficiency: float
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# Marketplace Models
class CreditPackage(BaseModel):
    id: str
    name: str
    credits: float
    price: float  # in USD
    description: str
    popular: bool = False

class PurchaseRequest(BaseModel):
    package_id: str
    user_id: str

# Monitoring Models
class WallStatus(BaseModel):
    wall_number: int
    name: str
    active_threats: int
    total_blocked: int
    entropy_generated: float
    status: Literal["active", "under_attack", "fortified"]

class StarheartStatus(BaseModel):
    current_power: float
    power_generation_rate: float
    efficiency: float
    total_generated: float
    status: Literal["idle", "active", "overcharged"]

class SystemStats(BaseModel):
    total_users: int
    total_credits_distributed: float
    total_entropy_converted: float
    total_attacks_blocked: int
    walls: List[WallStatus]
    starheart: StarheartStatus
