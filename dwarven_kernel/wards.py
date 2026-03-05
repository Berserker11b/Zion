"""
WARDS — The Logic Layer
========================

Warding is from Peter Brett (The Warded Man / The Demon Cycle).

Wards determine what is ALLOWED IN and what is NOT ALLOWED IN.
That line that goes around it — you must have the KEY to even alter it.
Wards define what reality is permitted inside their boundary.

Ward circles are geometric: circles containing runes.
Shape-based. The circle IS the containment. The runes inside
define what the containment does.

"Binding wards — shaping reality logic.
 Define what is real and allowed inside
 any given region."

Ward Types (from the Grimoire, repurposed):
    Impact      — resist force, absorb attacks
    Siphon      — drain energy, redirect power
    Test        — probe, verify, validate
    Containment — hold, isolate, quarantine
    Cold        — nullify, freeze, dampen
    Energy      — power routing, electric flow
    Sealing     — permanent closure, immutability
    Binding     — shape reality, define rules

Additional Grimoire wards (repurposed as logic):
    Protection  — general defense
    Light       — visibility, logging, illumination
    Prophecy    — prediction, pattern forecasting
    Resonance   — sound/signal wave control
    Unsight     — invisibility, stealth
    Wardsight   — see in magical spectrum, read auras/state
    Magnetic    — attraction/repulsion of data
    Moisture    — flow control, fluid dynamics
    Piercing    — penetration, cutting through barriers
    Pressure    — compression, force application
    Perception  — alter how things are sensed/read
    Blending    — camouflage, adaptation
    Confusion   — disorientation, obfuscation
"""

import hashlib
import time
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Set


# ================================================================
#                    WARD TYPES
# ================================================================

class WardType(Enum):
    """
    All ward types from the Grimoire, repurposed as logic primitives.
    Each ward type defines a specific kind of boundary enforcement.
    """
    # Core 8 (from the Keeper's notes)
    IMPACT      = ("impact",      "resist force, absorb attacks")
    SIPHON      = ("siphon",      "drain energy, redirect power")
    TEST        = ("test",        "probe, verify, validate")
    CONTAINMENT = ("containment", "hold, isolate, quarantine")
    COLD        = ("cold",        "nullify, freeze, dampen")
    ENERGY      = ("energy",      "power routing, electric flow")
    SEALING     = ("sealing",     "permanent closure, immutability")
    BINDING     = ("binding",     "shape reality, define allowed rules")

    # Extended Grimoire (repurposed)
    PROTECTION  = ("protection",  "general defense barrier")
    LIGHT       = ("light",       "visibility, logging, illumination")
    PROPHECY    = ("prophecy",    "prediction, pattern forecasting")
    RESONANCE   = ("resonance",   "signal wave control, amplification/silence")
    UNSIGHT     = ("unsight",     "invisibility, stealth, hidden from scans")
    WARDSIGHT   = ("wardsight",   "see true state, read auras, pierce deception")
    MAGNETIC    = ("magnetic",    "attraction/repulsion of data flows")
    MOISTURE    = ("moisture",    "flow control, fluid data dynamics")
    PIERCING    = ("piercing",    "penetration, cutting through barriers")
    PRESSURE    = ("pressure",    "compression, force application")
    PERCEPTION  = ("perception",  "alter how things are sensed/reported")
    BLENDING    = ("blending",    "camouflage, adaptive appearance")
    CONFUSION   = ("confusion",   "disorientation, obfuscation of attackers")

    def __init__(self, ward_id: str, desc: str):
        self.ward_id = ward_id
        self.desc = desc


# ================================================================
#                    WARD KEY
# ================================================================

@dataclass
class WardKey:
    """
    A key that grants permission to alter a ward circle.
    Without the key, you cannot change the ward. Period.

    "That line that goes around it — you must have the
     KEY to even alter it."
    """
    key_id: str
    holder: str                         # who holds this key
    permissions: Set[str] = field(default_factory=set)  # what operations are allowed
    created_at: float = field(default_factory=time.time)
    expires_at: Optional[float] = None  # None = never expires

    @property
    def is_valid(self) -> bool:
        if self.expires_at is None:
            return True
        return time.time() < self.expires_at

    @property
    def signature(self) -> str:
        raw = f"{self.key_id}:{self.holder}:{sorted(self.permissions)}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    def can(self, operation: str) -> bool:
        """Check if this key permits a specific operation."""
        if not self.is_valid:
            return False
        return operation in self.permissions or "*" in self.permissions

    def __repr__(self):
        return f"WardKey<{self.key_id} holder={self.holder} valid={self.is_valid}>"


# ================================================================
#                    WARD RULE
# ================================================================

@dataclass
class WardRule:
    """
    A single rule within a ward circle.
    Defines what is allowed or denied within the ward's boundary.

    Rules are geometric logic — they describe reality inside the circle.
    """
    ward_type: WardType
    action: str              # "allow", "deny", "siphon", "test", "transform"
    target: str              # what this rule applies to (pattern/identifier)
    conditions: Dict[str, Any] = field(default_factory=dict)
    power: float = 1.0       # rule strength (0.0-10.0)
    active: bool = True

    def matches(self, subject: Dict[str, Any]) -> bool:
        """Check if a subject matches this rule's conditions."""
        if not self.active:
            return False

        # Target matching (supports wildcards)
        if self.target != "*":
            subject_id = subject.get("id", subject.get("name", ""))
            if self.target not in str(subject_id):
                return False

        # Condition matching
        for key, expected in self.conditions.items():
            actual = subject.get(key)
            if actual is None:
                return False
            if callable(expected):
                if not expected(actual):
                    return False
            elif actual != expected:
                return False

        return True

    def __repr__(self):
        return f"WardRule<{self.ward_type.ward_id}:{self.action} '{self.target}' p={self.power}>"


# ================================================================
#                    WARD CIRCLE
# ================================================================

class WardCircle:
    """
    A Ward Circle — the fundamental security/logic boundary.

    A circle of geometric runes that defines what reality is
    permitted inside. Nothing enters or leaves without passing
    through the ward logic.

    Properties:
        - Must be CLOSED (the circle must be complete)
        - Must have a KEY to alter
        - Rules are evaluated in order (first match wins)
        - Touch-perfect: if the circle isn't closed properly,
          the ward doesn't work
        - Power determined by mathematical correctness of the runes

    "Circles are wards. They contain matter. Slowly, steady spin."
    """

    def __init__(self, name: str, ward_type: WardType, key: WardKey):
        self.name = name
        self.ward_type = ward_type
        self.key = key
        self.rules: List[WardRule] = []
        self.closed: bool = False
        self.created_at: float = time.time()
        self._breach_count: int = 0
        self._evaluation_count: int = 0

    @property
    def power(self) -> float:
        """Total power of this ward circle (sum of rule powers)."""
        if not self.closed:
            return 0.0  # open circle has no power
        return sum(r.power for r in self.rules if r.active)

    @property
    def is_intact(self) -> bool:
        """A ward is intact if it's closed and has positive power."""
        return self.closed and self.power > 0

    @property
    def signature(self) -> str:
        raw = f"{self.name}:{self.ward_type.ward_id}:{len(self.rules)}:{self.closed}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    def add_rule(self, rule: WardRule, key: WardKey) -> bool:
        """
        Add a rule to this ward circle. Requires a valid key.
        "You must have the key to even alter it."
        """
        if key.signature != self.key.signature:
            return False
        if not key.can("add_rule"):
            return False
        self.rules.append(rule)
        return True

    def remove_rule(self, index: int, key: WardKey) -> bool:
        """Remove a rule by index. Requires valid key."""
        if key.signature != self.key.signature:
            return False
        if not key.can("remove_rule"):
            return False
        if 0 <= index < len(self.rules):
            self.rules.pop(index)
            return True
        return False

    def close(self, key: WardKey) -> bool:
        """
        Close the ward circle. Makes it active.
        "If they don't touch perfectly, the ward doesn't work."
        Must have at least one rule to close.
        """
        if key.signature != self.key.signature:
            return False
        if not key.can("close"):
            return False
        if not self.rules:
            return False  # empty circle cannot close
        self.closed = True
        return True

    def breach(self):
        """Record a breach attempt. Weakens the ward."""
        self._breach_count += 1

    def evaluate(self, subject: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate a subject against this ward circle.

        Returns the result of the first matching rule.
        If no rules match, default is DENY (nothing enters without permission).

        "Wards determine what is allowed in and what is not allowed in."
        """
        self._evaluation_count += 1

        if not self.is_intact:
            return {
                "allowed": False,
                "reason": "ward_not_intact",
                "ward": self.name,
            }

        for rule in self.rules:
            if rule.matches(subject):
                allowed = rule.action in ("allow", "transform")
                return {
                    "allowed": allowed,
                    "action": rule.action,
                    "rule": repr(rule),
                    "ward": self.name,
                    "ward_type": self.ward_type.ward_id,
                    "power": rule.power,
                }

        # Default: DENY. Nothing enters without explicit permission.
        return {
            "allowed": False,
            "reason": "no_matching_rule",
            "ward": self.name,
            "ward_type": self.ward_type.ward_id,
        }

    def status(self) -> dict:
        return {
            "name": self.name,
            "ward_type": self.ward_type.ward_id,
            "closed": self.closed,
            "intact": self.is_intact,
            "power": round(self.power, 2),
            "rules": len(self.rules),
            "active_rules": sum(1 for r in self.rules if r.active),
            "breaches": self._breach_count,
            "evaluations": self._evaluation_count,
        }

    def __repr__(self):
        state = "INTACT" if self.is_intact else ("CLOSED" if self.closed else "OPEN")
        return f"WardCircle<{self.name} {self.ward_type.ward_id} {state} p={self.power:.1f} rules={len(self.rules)}>"


# ================================================================
#                    WARD NET — Multiple Overlapping Circles
# ================================================================

class WardNet:
    """
    A network of overlapping ward circles.
    Like the Grimoire shows — multiple wards layered for defense in depth.

    Each circle handles a different type of logic.
    A subject must pass ALL circles to be allowed through.
    """

    def __init__(self, name: str):
        self.name = name
        self.circles: List[WardCircle] = []

    def add_circle(self, circle: WardCircle):
        self.circles.append(circle)

    @property
    def total_power(self) -> float:
        return sum(c.power for c in self.circles)

    @property
    def intact_count(self) -> int:
        return sum(1 for c in self.circles if c.is_intact)

    def evaluate(self, subject: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate subject against ALL ward circles in the net.
        Must pass every circle. One failure = denied.
        """
        results = []
        all_allowed = True

        for circle in self.circles:
            result = circle.evaluate(subject)
            results.append(result)
            if not result.get("allowed", False):
                all_allowed = False

        return {
            "allowed": all_allowed,
            "ward_net": self.name,
            "total_power": round(self.total_power, 2),
            "circles_evaluated": len(results),
            "circles_passed": sum(1 for r in results if r.get("allowed")),
            "details": results,
        }

    def status(self) -> dict:
        return {
            "name": self.name,
            "circles": len(self.circles),
            "intact": self.intact_count,
            "total_power": round(self.total_power, 2),
            "circle_status": [c.status() for c in self.circles],
        }

    def __repr__(self):
        return f"WardNet<{self.name} circles={len(self.circles)} p={self.total_power:.1f}>"
