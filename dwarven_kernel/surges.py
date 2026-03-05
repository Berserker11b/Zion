"""
SURGES — The Metamorphic Engine
================================

Every 15-30 seconds, the visual representation of all runes shifts.
The inner truth remains constant. Only the outer form changes.
Outsiders see a different language every half-minute.

"Surges" are the fundamental forces of transformation.
They determine HOW the glyph lines change — not just that they change,
but the character of the change itself.

The Ten Surges (from the fundamental forces that reshape reality):
    Adhesion, Gravitation, Division, Abrasion, Progression,
    Illumination, Transformation, Transportation, Cohesion, Tension

Each surge type produces a different visual mutation:
    Gravitation pulls elements inward.
    Division spreads them apart.
    Transformation swaps primitives for similar forms.
    Transportation shifts positions.
    And so on.

The inner glyph — the truth — never changes.
Only the outer glyph — what the world sees — shifts with each surge.
"""

import time
import math
import hashlib
import random
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional, Tuple


# ================================================================
#                    THE TEN SURGES
# ================================================================

class SurgeType(Enum):
    """
    The Ten Surges — fundamental forces of transformation.
    Each determines how glyph lines change during a surge cycle.
    """
    ADHESION       = ("adhesion",       "binding things together")
    GRAVITATION    = ("gravitation",    "pulling, attraction, weight")
    DIVISION       = ("division",       "splitting, separation, cutting")
    ABRASION       = ("abrasion",       "friction, erosion, grinding")
    PROGRESSION    = ("progression",    "growth, healing, advance")
    ILLUMINATION   = ("illumination",   "light, revelation, clarity")
    TRANSFORMATION = ("transformation", "changing one form to another")
    TRANSPORTATION = ("transportation", "moving through space")
    COHESION       = ("cohesion",       "making things solid, firm")
    TENSION        = ("tension",        "stretching, pressure, stress")

    def __init__(self, surge_id: str, desc: str):
        self.surge_id = surge_id
        self.desc = desc


# ================================================================
#                    SURGE ENGINE
# ================================================================

class SurgeEngine:
    """
    The Surge Engine shifts glyph forms on a 15-30 second cycle.

    Inner form (fortress-only) NEVER changes. It is truth.
    Outer form (what outsiders see) transforms with each surge cycle.
    The active surge type determines HOW the transformation occurs.

    Every 15-30 seconds, the lines change. The characters shift.
    Same meaning. Different face. Every time.
    """

    def __init__(self, cycle_seconds: int = 20, seed: str = "dwarven_kernel"):
        self.cycle_seconds = max(15, min(30, cycle_seconds))  # clamp 15-30
        self.seed = seed
        self._creation_time = time.time()

    @property
    def current_cycle(self) -> int:
        """Which surge cycle we're in."""
        elapsed = time.time() - self._creation_time
        return int(elapsed / self.cycle_seconds)

    @property
    def active_surge(self) -> SurgeType:
        """Which surge is currently active — determines transformation style."""
        surges = list(SurgeType)
        idx = self.current_cycle % len(surges)
        return surges[idx]

    @property
    def time_until_shift(self) -> float:
        """Seconds until the next surge shift."""
        elapsed = time.time() - self._creation_time
        cycle_pos = elapsed % self.cycle_seconds
        return self.cycle_seconds - cycle_pos

    @property
    def cycle_progress(self) -> float:
        """How far through the current cycle (0.0 to 1.0)."""
        elapsed = time.time() - self._creation_time
        return (elapsed % self.cycle_seconds) / self.cycle_seconds

    def cycle_seed(self, cycle: Optional[int] = None) -> str:
        """Deterministic seed for the current or given cycle."""
        c = cycle if cycle is not None else self.current_cycle
        raw = f"{self.seed}:{c}"
        return hashlib.sha256(raw.encode()).hexdigest()

    def transform_elements(self, elements: list, cycle: Optional[int] = None) -> list:
        """
        Transform a list of PlacedPrimitives for the current surge cycle.

        The inner glyph (truth) is unchanged. This produces the OUTER form —
        what outsiders see. Different every cycle. Same meaning underneath.
        """
        from .glyphs import PlacedPrimitive, Primitive

        seed = self.cycle_seed(cycle)
        surge = self.active_surge if cycle is None else list(SurgeType)[
            (cycle if cycle is not None else self.current_cycle) % len(SurgeType)
        ]
        rng = random.Random(seed)

        # Primitive swap table for TRANSFORMATION surge
        swap_table = {
            Primitive.CIRCLE:   Primitive.HEXAGON,
            Primitive.HEXAGON:  Primitive.CIRCLE,
            Primitive.TRIANGLE: Primitive.DIAMOND,
            Primitive.DIAMOND:  Primitive.TRIANGLE,
            Primitive.SQUARE:   Primitive.CROSS,
            Primitive.CROSS:    Primitive.SQUARE,
            Primitive.LINE_H:   Primitive.LINE_V,
            Primitive.LINE_V:   Primitive.LINE_H,
            Primitive.LINE_DR:  Primitive.LINE_DL,
            Primitive.LINE_DL:  Primitive.LINE_DR,
            Primitive.ARC_TOP:  Primitive.ARC_BOT,
            Primitive.ARC_BOT:  Primitive.ARC_TOP,
            Primitive.ARROW_UP: Primitive.ARROW_DN,
            Primitive.ARROW_DN: Primitive.ARROW_UP,
            Primitive.ARROW_RT: Primitive.ARROW_LF,
            Primitive.ARROW_LF: Primitive.ARROW_RT,
            Primitive.STAR:     Primitive.SPIRAL,
            Primitive.SPIRAL:   Primitive.STAR,
        }

        transformed = []
        for elem in elements:
            new_x = elem.x
            new_y = elem.y
            new_rot = elem.rotation
            new_prim = elem.primitive
            new_scale = elem.scale

            if surge == SurgeType.GRAVITATION:
                # Pull toward center
                new_x *= (0.6 + rng.random() * 0.4)
                new_y *= (0.6 + rng.random() * 0.4)

            elif surge == SurgeType.DIVISION:
                # Spread apart
                new_x *= (1.1 + rng.random() * 0.5)
                new_y *= (1.1 + rng.random() * 0.5)

            elif surge == SurgeType.TRANSFORMATION:
                # Swap primitives for visual cousins
                new_prim = swap_table.get(elem.primitive, elem.primitive)

            elif surge == SurgeType.ADHESION:
                # Rotate cluster
                angle = rng.uniform(15, 60)
                rad = math.radians(angle)
                new_x = elem.x * math.cos(rad) - elem.y * math.sin(rad)
                new_y = elem.x * math.sin(rad) + elem.y * math.cos(rad)
                new_rot = (elem.rotation + angle) % 360

            elif surge == SurgeType.ILLUMINATION:
                # Truth surge — no visual change. Reveals inner form.
                pass

            elif surge == SurgeType.TRANSPORTATION:
                # Shift positions randomly
                new_x += rng.uniform(-1.0, 1.0)
                new_y += rng.uniform(-1.0, 1.0)

            elif surge == SurgeType.COHESION:
                # Snap to grid — crystallize
                new_x = round(new_x)
                new_y = round(new_y)
                new_rot = round(new_rot / 45) * 45

            elif surge == SurgeType.TENSION:
                # Stretch one axis
                new_x *= (1.0 + rng.random() * 0.4)
                new_y *= (0.6 + rng.random() * 0.4)

            elif surge == SurgeType.PROGRESSION:
                # Scale up slightly — growth
                new_scale *= (1.05 + rng.random() * 0.15)

            elif surge == SurgeType.ABRASION:
                # Add noise — roughen edges
                new_x += rng.uniform(-0.3, 0.3)
                new_y += rng.uniform(-0.3, 0.3)
                new_rot += rng.uniform(-10, 10)

            transformed.append(PlacedPrimitive(
                primitive=new_prim,
                x=round(new_x, 2),
                y=round(new_y, 2),
                rotation=round(new_rot, 1),
                scale=round(new_scale, 2),
            ))

        return transformed

    def outer_glyph(self, glyph, cycle: Optional[int] = None):
        """
        Generate the outer (visible) form of a glyph for this surge cycle.
        Returns a new Glyph with transformed elements.
        The original glyph (inner truth) is not modified.
        """
        from .glyphs import Glyph

        transformed = self.transform_elements(glyph.elements, cycle)
        outer = Glyph(name=f"{glyph.name}:outer:{self.current_cycle}")
        outer.elements = transformed
        return outer

    def status(self) -> dict:
        """Current surge engine status."""
        return {
            "cycle": self.current_cycle,
            "active_surge": self.active_surge.surge_id,
            "surge_effect": self.active_surge.desc,
            "time_until_shift": round(self.time_until_shift, 1),
            "cycle_progress": round(self.cycle_progress, 3),
            "cycle_seconds": self.cycle_seconds,
        }

    def __repr__(self):
        s = self.active_surge
        return f"SurgeEngine<cycle={self.current_cycle} surge={s.surge_id} shift_in={self.time_until_shift:.1f}s>"
