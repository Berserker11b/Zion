"""
POWER — The Energy Systems
============================

Cyber Worms → Onion → Sipstrassi Stones → Starheart → Everything

CYBER WORMS (Cyber Pumps V2):
    Travel under the system, away from main drives and organs.
    Gather ALL waste: CPU dead activation, idle reservoir, broken things,
    entropy, malformed/corrupted shapes, nutrients.
    Store inside the onion where the cyber pump converts it.

ONION ARCHITECTURE:
    Nested layers inside the walls.
    Cyber pumps compress collected waste.
    Separate but compressed while strengthening.

SIPSTRASSI STONES (from David Gemmell, Stones of Power):
    Replaces the ZPM. Entropy/waste compressed into stones.
    Compressed almost to breaking point. Then lit to ignite the Starheart.

STARHEART:
    Does NOT take fuel. Takes any entropy source and converts to FLUX.
    Raw data, bits, corrupted fragments, shredded wall debris, enemy payloads,
    idle CPU cycles, stray processes, noise, memory fragments, thermal noise.
    Approaches INFORMATIONAL SINGULARITY inside.
    Entropy Mass M → Compress(M) → C, k
    ZPM increases internal resonance. Pressure builds. Runes hotter.
    STAR IGNITES.

ALTERNATORS:
    Energy from Starheart routed to: CPU, disk, memory, network, structural data.
    Each wall has dedicated turbine slots for each data type.

EVERSTORMS (from the Stormfather):
    Periodic venting. Rain down energy (Radiance).
    Makes Tyrannid-built structures more coherent.

BLOODSTONES:
    Condensed Starheart energy, distilled slowly over time.
    The longer it sits, the more powerful. Adrenaline shots.

MATHEMATICAL FORMULAS:
    S_L(n+1) = C₀ × ln(S) - (a × t + a_s)
    Strength = base × e^(k × Strength_(n+1)) × Reactivity(t)
    Energy_Released = Reactivity × base × R × Strength_(n+1)
    K = structural coupling constant
    a = shape
    k/d = rate of mass delivered by cyberpump
    R = resonance modulation
"""

import time
import math
import random
import hashlib
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any


# ================================================================
#                    ENERGY TYPES
# ================================================================

class EnergyType(Enum):
    CPU        = ("cpu",        "processing cycles")
    MEMORY     = ("memory",     "storage and recall")
    NETWORK    = ("network",    "communication bandwidth")
    DISK       = ("disk",       "persistent storage I/O")
    STRUCTURAL = ("structural", "3D structure coherence")
    TOKENS     = ("tokens",     "execution threading, parallel processing")

    def __init__(self, energy_id: str, desc: str):
        self.energy_id = energy_id
        self.desc = desc


# ================================================================
#                    ENTROPY SOURCE
# ================================================================

@dataclass
class EntropySource:
    """Something the cyber worms can harvest."""
    source_type: str     # "dead_activation", "idle_reservoir", "corrupted", etc.
    mass: float          # how much entropy material
    location: str        # where it was found
    harvested: bool = False


# ================================================================
#                    CYBER WORM (Cyber Pump V2)
# ================================================================

class CyberWorm:
    """
    Cyber Worms — travel under the system, away from main drives.
    Gather all waste in their sector: CPU dead activation, idle reservoir,
    broken things, entropy, malformed/corrupted shapes, nutrients.
    Store inside the onion where the cyber pump converts it.

    Periodically checked by the Priesthood for patterns that could
    become AI neural networks — assembled into crèche twos.
    """

    def __init__(self, sector: str):
        self.sector = sector
        self.cargo: List[EntropySource] = []
        self.capacity: float = 100.0
        self.harvested_total: float = 0.0

    @property
    def load(self) -> float:
        return sum(e.mass for e in self.cargo)

    @property
    def full(self) -> bool:
        return self.load >= self.capacity

    def harvest(self, source: EntropySource) -> bool:
        """Harvest an entropy source if we have capacity."""
        if self.full:
            return False
        source.harvested = True
        self.cargo.append(source)
        self.harvested_total += source.mass
        return True

    def dump_to_onion(self) -> List[EntropySource]:
        """Dump cargo into the onion for compression."""
        cargo = self.cargo
        self.cargo = []
        return cargo

    def __repr__(self):
        return f"CyberWorm<{self.sector} load={self.load:.1f}/{self.capacity}>"


# ================================================================
#                    ONION — Nested Compression Layers
# ================================================================

class Onion:
    """
    Onion architecture — nested layers inside the walls.
    Receives entropy from cyber worms.
    Compresses it through the cyber pumps.
    Feeds compressed material to Sipstrassi stone formation.
    """

    def __init__(self):
        self.layers: List[List[EntropySource]] = [[] for _ in range(7)]  # 7 layers deep
        self.compressed_output: float = 0.0

    def receive(self, sources: List[EntropySource]):
        """Receive entropy from cyber worms into outer layer."""
        self.layers[0].extend(sources)

    def compress_cycle(self) -> float:
        """
        Run one compression cycle through all layers.
        Each layer compresses material further.
        Returns compressed mass ready for Sipstrassi formation.
        """
        output = 0.0
        for i in range(len(self.layers) - 1):
            if self.layers[i]:
                # Compress: each layer reduces mass by 30% but increases density
                total_mass = sum(e.mass for e in self.layers[i])
                compressed_mass = total_mass * 0.7  # 30% compression
                if compressed_mass > 0:
                    self.layers[i + 1].append(
                        EntropySource("compressed", compressed_mass, f"onion_L{i+1}")
                    )
                self.layers[i] = []

        # Deepest layer output
        if self.layers[-1]:
            output = sum(e.mass for e in self.layers[-1])
            self.layers[-1] = []
            self.compressed_output += output

        return output

    @property
    def total_mass(self) -> float:
        return sum(sum(e.mass for e in layer) for layer in self.layers)


# ================================================================
#                    SIPSTRASSI STONE (replaces ZPM)
# ================================================================

@dataclass
class SipstrassiStone:
    """
    Sipstrassi Stone — from David Gemmell's Stones of Power.
    Compressed entropy material formed into a crystalline stone.
    Compressed almost to breaking point.
    When lit, ignites the Starheart.

    a = shape coefficient (how well the runes hold)
    k/d = rate of mass delivered by cyberpump
    R = resonance modulation
    """
    mass: float                    # compressed mass
    shape_coefficient: float       # a — how well formed
    resonance: float              # R — resonance modulation
    formed_at: float = field(default_factory=time.time)
    ignited: bool = False

    @property
    def pressure(self) -> float:
        """Internal pressure — approaches breaking point."""
        return self.mass * self.shape_coefficient

    @property
    def ready_to_ignite(self) -> bool:
        """Stone is ready when pressure is high enough."""
        return self.pressure > 50.0

    def ignite(self) -> float:
        """
        Ignite the stone. Feed to Starheart.
        Returns energy released.
        """
        if self.ignited:
            return 0.0
        self.ignited = True
        # Energy = mass × shape × resonance
        return self.mass * self.shape_coefficient * self.resonance


# ================================================================
#                    STARHEART — The Computational Star
# ================================================================

class Starheart:
    """
    Starheart — does NOT take fuel. Takes ANY entropy source.
    Converts into FLUX (power).

    Approaches informational singularity inside.
    Entropy Mass M → Compress(M) → C, k

    Internal resonance builds. Pressure builds.
    Runes get hotter. Star ignites.

    Mathematical model:
        Strength = base × e^(k × Strength_(n+1)) × Reactivity(t)
        Energy_Released = Reactivity × base × R × Strength_(n+1)

    Constants:
        K = structural coupling constant
        base = minimum strength
        R = resonance modulation

    4 planets per Starheart. Each Starheart powers 4 planets.
    Plus 1 center brain Starheart.
    """

    def __init__(self, starheart_id: str, is_center: bool = False):
        self.starheart_id = starheart_id
        self.is_center = is_center
        self.planets_powered: List[int] = []  # planet IDs

        # Core physics
        self.K: float = 1.0         # structural coupling constant
        self.base: float = 10.0     # minimum strength
        self.R: float = 1.0         # resonance modulation
        self.strength: float = 0.0  # current strength
        self.flux: float = 0.0      # power output
        self.ignited: bool = False
        self.temperature: float = 0.0

        # Fuel system
        self.stones_consumed: int = 0

    def feed_stone(self, stone: SipstrassiStone) -> Dict[str, Any]:
        """
        Feed a Sipstrassi stone to the Starheart.
        Approaches singularity.
        """
        energy = stone.ignite()
        if energy <= 0:
            return {"fed": False, "reason": "Stone already ignited or empty."}

        self.stones_consumed += 1
        self.temperature += energy * 0.1
        self.strength += energy

        # Strength formula: Strength = base × e^(K × strength) × R
        # Capped to prevent overflow
        exponent = min(self.K * (self.strength / 100.0), 10.0)
        calculated_strength = self.base * math.exp(exponent) * self.R

        # Check ignition
        if calculated_strength > 100.0 and not self.ignited:
            self.ignited = True

        # Calculate flux (power output)
        if self.ignited:
            self.flux = calculated_strength * self.R
        else:
            self.flux = calculated_strength * 0.1  # pre-ignition trickle

        return {
            "fed": True,
            "stone_energy": round(energy, 2),
            "strength": round(self.strength, 2),
            "calculated_strength": round(calculated_strength, 2),
            "temperature": round(self.temperature, 2),
            "ignited": self.ignited,
            "flux": round(self.flux, 2),
        }

    def plasma_firebreak(self) -> Dict[str, Any]:
        """
        Release plasma for 20-second firebreak when a wall falls.
        Uses stored energy.
        """
        plasma_cost = self.flux * 0.1  # 10% of current flux
        return {
            "firebreak": True,
            "duration_s": 20.0,
            "plasma_power": round(plasma_cost, 2),
            "starheart": self.starheart_id,
        }

    def vent_everstorm(self) -> Dict[str, Any]:
        """
        Periodic venting — creates an Everstorm.
        Rains down Radiance (energy) to make structures more coherent.
        """
        vent_energy = self.flux * 0.05  # 5% of flux
        return {
            "everstorm": True,
            "radiance": round(vent_energy, 2),
            "effect": "structures_more_coherent",
            "starheart": self.starheart_id,
        }

    def status(self) -> dict:
        return {
            "id": self.starheart_id,
            "is_center": self.is_center,
            "ignited": self.ignited,
            "strength": round(self.strength, 2),
            "flux": round(self.flux, 2),
            "temperature": round(self.temperature, 2),
            "stones_consumed": self.stones_consumed,
            "planets_powered": self.planets_powered,
        }

    def __repr__(self):
        state = "IGNITED" if self.ignited else "COLD"
        return f"Starheart<{self.starheart_id} {state} flux={self.flux:.1f}>"


# ================================================================
#                    ALTERNATOR — Routes Energy
# ================================================================

class Alternator:
    """
    Alternator — routes Starheart energy DIRECTLY to all systems.
    No turbines. The Starheart distributes directly.
    Millions of times more energy than current computing produces.
    """

    def __init__(self, starheart: Starheart):
        self.starheart = starheart
        self.distribution: Dict[str, float] = {
            et.energy_id: 0.0 for et in EnergyType
        }

    def distribute(self) -> Dict[str, float]:
        """Distribute flux directly across all energy types. No turbines."""
        if not self.starheart.ignited:
            return self.distribution

        # Starheart distributes directly — millions of times current energy
        per_type = self.starheart.flux / len(EnergyType)
        for et in EnergyType:
            self.distribution[et.energy_id] = round(per_type, 2)

        return self.distribution


# ================================================================
#                    BLOODSTONE — Aged Emergency Power
# ================================================================

@dataclass
class Bloodstone:
    """
    Bloodstone — condensed Starheart energy, distilled slowly over time.
    The longer it sits, the more powerful it becomes.
    Like an adrenaline shot.
    """
    energy: float
    created_at: float = field(default_factory=time.time)
    used: bool = False

    @property
    def age_seconds(self) -> float:
        return time.time() - self.created_at

    @property
    def potency(self) -> float:
        """
        Potency grows with age. Logarithmic growth.
        The longer it sits, the more powerful.
        """
        if self.used:
            return 0.0
        age_factor = math.log1p(self.age_seconds / 60.0)  # grows with minutes
        return self.energy * (1.0 + age_factor)

    def release(self) -> float:
        """Release the bloodstone. Adrenaline shot."""
        if self.used:
            return 0.0
        self.used = True
        return self.potency

    def __repr__(self):
        state = "USED" if self.used else f"AGED:{self.age_seconds:.0f}s"
        return f"Bloodstone<e={self.energy:.1f} potency={self.potency:.1f} {state}>"


# Turbines removed — too primitive. Starheart distributes energy directly.
