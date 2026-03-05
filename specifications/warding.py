"""
WARDING LOGIC SPECIFICATION
=============================
An Original Language -- Binding Reality Logic

This is NOT Go. This is an original logic language defined from scratch.
Wards define what is real and what is allowed inside any region.

CORE PROPERTIES:
  - Wards slightly SPIN, changing locations
  - Must TOUCH PERFECTLY to activate -- geometry must be exact
  - Permanent shape once set -- cannot be removed without the key
  - Define reality boundaries: what IS and what IS NOT allowed
  - Binding wards shape reality logic

DESIGN:
  Warding is the logic layer. Where Dwarven Runes are opcodes
  (what to DO), Wards are predicates (what IS TRUE).
  A ward circle defines a region of reality.
  Inside that circle, the ward's rules are absolute.

  But the wards SPIN. They change position.
  And they must TOUCH PERFECTLY -- every edge, every vertex,
  every line must connect with exact geometric precision.
  A gap, even microscopic, and the ward fails.

(C) Anthony Eric Chavez -- The Keeper
"""

import time
import math
import random
import hashlib
from enum import Enum, auto

# ================================================================
#  THE 21 WARD TYPES -- Original Logic Operators
# ================================================================
#
#  Each ward is a PREDICATE that defines reality inside its circle.
#  Not boolean logic borrowed from Boole.
#  Not SQL WHERE clauses borrowed from Codd.
#  Geometric predicates: a shape that IS the rule.
#

class WardType(Enum):
    """The 21 original ward types -- logic operators of the Warding language."""

    # Core 8 -- fundamental operations
    IMPACT      = auto()   # force, collision, direct effect
    SIPHON      = auto()   # drain, extract, redirect energy
    TEST        = auto()   # evaluate, examine, question
    CONTAINMENT = auto()   # hold, restrict, define boundary
    COLD        = auto()   # freeze, pause, suspend
    ENERGY      = auto()   # power, fuel, activation
    SEALING     = auto()   # lock, finalize, make permanent
    BINDING     = auto()   # link, connect, make inseparable

    # Extended 13 -- advanced operations
    PROTECTION  = auto()   # shield, guard, prevent harm
    LIGHT       = auto()   # reveal, illuminate, expose
    PROPHECY    = auto()   # predict, anticipate, pre-compute
    RESONANCE   = auto()   # harmonize, match frequency, sync
    UNSIGHT     = auto()   # hide, conceal, make invisible
    WARDSIGHT   = auto()   # see wards, meta-inspection
    MAGNETIC    = auto()   # attract, repel, orient
    MOISTURE    = auto()   # flow, adapt, fill gaps
    PIERCING    = auto()   # penetrate, bypass, cut through
    PRESSURE    = auto()   # compress, force inward, concentrate
    PERCEPTION  = auto()   # sense, detect, awareness
    BLENDING    = auto()   # merge, combine, unify
    CONFUSION   = auto()   # obfuscate, misdirect, scramble


# ================================================================
#  WARD -- A Single Logic Predicate
# ================================================================
#
#  A ward is a geometric shape that spins.
#  It changes position as it spins.
#  But it must TOUCH PERFECTLY with adjacent wards
#  to form a complete ward circle.
#

class Ward:
    """
    A single ward in the Warding language.

    The ward spins, changing its angular position.
    It must touch perfectly with adjacent wards.
    A gap and the ward circle breaks.
    """

    def __init__(self, ward_type, vertices, center=(0.0, 0.0), radius=1.0):
        """
        ward_type: which of the 21 ward types
        vertices: list of (x, y) points defining the ward's geometry
        center: the center point of the ward
        radius: the radius of the ward's circle
        """
        self.ward_type = ward_type
        self.original_vertices = list(vertices)
        self.vertices = list(vertices)
        self.center = center
        self.radius = radius
        self.angle = 0.0                # current rotation angle (radians)
        self.spin_rate = random.uniform(0.01, 0.05)  # radians per tick
        self.last_spin = time.time()
        self.key = None                 # ward key -- required to alter
        self.permanent = False          # once sealed, cannot be removed without key
        self.active = False

    def spin(self):
        """
        The ward slightly spins, changing its location.
        The vertices rotate around the center.
        """
        self.angle += self.spin_rate

        # Rotate all vertices around center
        cos_a = math.cos(self.spin_rate)
        sin_a = math.sin(self.spin_rate)
        cx, cy = self.center

        new_vertices = []
        for (x, y) in self.vertices:
            # Translate to origin
            dx = x - cx
            dy = y - cy
            # Rotate
            nx = dx * cos_a - dy * sin_a
            ny = dx * sin_a + dy * cos_a
            # Translate back
            new_vertices.append((nx + cx, ny + cy))

        self.vertices = new_vertices
        self.last_spin = time.time()

    def touches(self, other, tolerance=0.001):
        """
        Check if this ward TOUCHES PERFECTLY with another ward.

        Must touch perfectly -- every connection point must be exact.
        Tolerance is microscopic. A gap and it fails.
        """
        for v1 in self.vertices:
            for v2 in other.vertices:
                dist = math.sqrt(
                    (v1[0] - v2[0]) ** 2 + (v1[1] - v2[1]) ** 2
                )
                if dist <= tolerance:
                    return True
        return False

    def seal(self, key):
        """
        Seal the ward permanently.
        Once sealed, the ward cannot be altered or removed without the key.
        """
        self.key = key
        self.permanent = True
        self.active = True
        return {
            "sealed": True,
            "ward_type": self.ward_type.name,
            "permanent": True,
        }

    def unseal(self, key):
        """Attempt to unseal the ward. Requires the correct key."""
        if not self.permanent:
            return {"unsealed": True, "reason": "Ward was not sealed."}
        if key == self.key:
            self.permanent = False
            self.active = False
            return {"unsealed": True}
        return {"unsealed": False, "reason": "Wrong key."}

    @property
    def identity(self):
        """The ward's identity hash based on its type and original geometry."""
        raw = f"{self.ward_type.name}:{self.original_vertices}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]


# ================================================================
#  WARD CIRCLE -- A Complete Logic Statement
# ================================================================
#
#  A ward circle is a group of wards arranged in a circle.
#  ALL wards must TOUCH PERFECTLY with their neighbors.
#  If any gap exists, the circle is broken and inactive.
#
#  This is the fundamental "statement" of the Warding language:
#  a closed circle of predicates that define reality inside.
#

class WardCircle:
    """
    A complete ward circle -- a statement in the Warding language.

    All wards must touch perfectly with their neighbors.
    A single gap breaks the entire circle.
    Inside the circle, the wards' rules define reality.
    """

    def __init__(self, name="unnamed"):
        self.name = name
        self.wards = []
        self.sealed = False
        self.key = None
        self.active = False

    def add_ward(self, ward):
        """Add a ward to the circle. Order matters -- adjacency is sequential."""
        self.wards.append(ward)
        self.active = False  # must re-verify

    def verify_touch(self, tolerance=0.001):
        """
        Verify that ALL adjacent wards touch perfectly.

        Every ward must touch its neighbor.
        The last ward must touch the first (closed circle).
        A single gap and the entire circle fails.
        """
        if len(self.wards) < 2:
            return {
                "perfect": False,
                "reason": "Need at least 2 wards to form a circle.",
                "gaps": [],
            }

        gaps = []
        for i in range(len(self.wards)):
            current = self.wards[i]
            neighbor = self.wards[(i + 1) % len(self.wards)]

            if not current.touches(neighbor, tolerance):
                gaps.append({
                    "between": (i, (i + 1) % len(self.wards)),
                    "ward_a": current.ward_type.name,
                    "ward_b": neighbor.ward_type.name,
                })

        perfect = len(gaps) == 0
        if perfect:
            self.active = True

        return {
            "perfect": perfect,
            "gaps": gaps,
            "reason": "Touch-perfect." if perfect
                      else f"{len(gaps)} gap(s) found. Circle broken.",
        }

    def spin_all(self):
        """
        All wards in the circle spin slightly.
        After spinning, touch must be re-verified.
        """
        for ward in self.wards:
            ward.spin()
        self.active = False  # must re-verify after spin

    def seal_circle(self, key):
        """Seal the entire circle. All wards become permanent."""
        # Must be touch-perfect first
        result = self.verify_touch()
        if not result["perfect"]:
            return {
                "sealed": False,
                "reason": "Cannot seal a broken circle.",
                "gaps": result["gaps"],
            }

        self.key = key
        self.sealed = True
        for ward in self.wards:
            ward.seal(key)

        return {
            "sealed": True,
            "name": self.name,
            "ward_count": len(self.wards),
        }

    @property
    def rules(self):
        """What reality rules does this circle enforce?"""
        return [ward.ward_type.name for ward in self.wards if ward.active]


# ================================================================
#  WARDING ENGINE -- The Logic Evaluator
# ================================================================
#
#  The Warding Engine evaluates ward circles.
#  It spins the wards, checks touch-perfection,
#  and determines what reality is defined inside each circle.
#
#  This is the "runtime" of the Warding language.
#

class WardingEngine:
    """
    The Warding language runtime.

    Manages ward circles. Spins wards. Verifies touch.
    Evaluates what reality is defined inside each circle.
    """

    def __init__(self):
        self.circles = {}   # name -> WardCircle

    def create_circle(self, name):
        """Create a new ward circle."""
        circle = WardCircle(name)
        self.circles[name] = circle
        return circle

    def evaluate(self, circle_name):
        """
        Evaluate a ward circle.

        1. Spin all wards (they drift)
        2. Check touch-perfection (must be exact)
        3. If perfect, the circle's rules define reality
        4. If broken, the circle is inactive
        """
        circle = self.circles.get(circle_name)
        if not circle:
            return {"evaluated": False, "reason": f"No circle named '{circle_name}'."}

        # 1. Spin
        circle.spin_all()

        # 2. Verify touch
        touch_result = circle.verify_touch()

        if not touch_result["perfect"]:
            return {
                "evaluated": True,
                "active": False,
                "reason": "Touch broken after spin. Gaps exist.",
                "gaps": touch_result["gaps"],
                "rules": [],
            }

        # 3. Active -- rules define reality
        return {
            "evaluated": True,
            "active": True,
            "rules": circle.rules,
            "ward_count": len(circle.wards),
            "name": circle_name,
        }

    def evaluate_all(self):
        """Evaluate all ward circles. Return which are active."""
        results = {}
        for name in self.circles:
            results[name] = self.evaluate(name)
        return results
