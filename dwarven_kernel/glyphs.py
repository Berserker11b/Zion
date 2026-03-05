"""
GLYPHS — The Geometric Character Set
=====================================

The Dwarven Kernel uses NO traditional text characters.
All symbols are geometric compositions: circles, lines, polygons.

Each glyph is a spatial arrangement of primitives on a grid.
Mathematical properties (symmetry, containment, rotation) determine power.

"They don't use traditional human characters at all."

Shape-based: circles are wards. Polygons are mathematical glyphs.
Order and containment matter. They spin.

Dynamic composition: Key-Glyph + Simple + Eurotype sign + Mark
Whether a line matters more than the literal symbol.
"""

import math
import hashlib
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Dict


# ================================================================
#                 GEOMETRIC PRIMITIVES — THE ALPHABET
# ================================================================

class Primitive(Enum):
    """
    Geometric primitives — the alphabet of the Dwarven language.
    These are not characters. They are shapes. Forms. Geometry.
    """
    # Containment forms (the circles, the wards)
    CIRCLE      = ("○", "containment, wholeness, warding")
    RING        = ("◯", "boundary, cycle, orbit")
    SPIRAL      = ("◎", "recursion, depth, layers")
    DOT         = ("·", "singularity, origin, seed")

    # Polygonal forms (mathematical glyphs, order)
    TRIANGLE    = ("△", "stability, structure, triad")
    INV_TRI     = ("▽", "inversion, descent, funnel")
    SQUARE      = ("□", "foundation, grounding, walls")
    DIAMOND     = ("◇", "value, transformation, choice")
    PENTAGON    = ("⬠", "complexity, life, organic")
    HEXAGON     = ("⬡", "harmony, efficiency, crystal")

    # Linear forms (connections, flows, pillars)
    LINE_H      = ("―", "horizontal flow, connection")
    LINE_V      = ("│", "vertical pillar, support")
    LINE_DR     = ("╲", "descent right, fall, gravity")
    LINE_DL     = ("╱", "ascent left, rise, lift")
    CROSS       = ("✚", "intersection, junction, decision")

    # Arcs and curves (partial containment, scope)
    ARC_TOP     = ("⌒", "upper arc, dome, sky")
    ARC_BOT     = ("⌣", "lower arc, basin, earth")
    WAVE        = ("∿", "resonance, frequency, vibration")

    # Special forms (Key-Glyphs)
    STAR        = ("✦", "power focus, radiance")
    ARROW_UP    = ("↑", "ascent, growth, surge")
    ARROW_DN    = ("↓", "descent, gravity, pull")
    ARROW_RT    = ("→", "flow, direction, path")
    ARROW_LF    = ("←", "return, reflection, origin")
    INFINITY    = ("∞", "unbounded, eternal, loop")
    OMEGA       = ("Ω", "completion, end, omega-point")

    def __init__(self, symbol: str, meaning: str):
        self.symbol = symbol
        self.meaning = meaning

    @property
    def is_containment(self) -> bool:
        return self in (
            Primitive.CIRCLE, Primitive.RING,
            Primitive.SPIRAL, Primitive.HEXAGON,
            Primitive.SQUARE, Primitive.PENTAGON,
        )

    @property
    def is_connector(self) -> bool:
        return self in (
            Primitive.LINE_H, Primitive.LINE_V,
            Primitive.LINE_DR, Primitive.LINE_DL,
            Primitive.CROSS, Primitive.WAVE,
            Primitive.ARROW_UP, Primitive.ARROW_DN,
            Primitive.ARROW_RT, Primitive.ARROW_LF,
        )

    @property
    def is_polygon(self) -> bool:
        return self in (
            Primitive.TRIANGLE, Primitive.INV_TRI,
            Primitive.SQUARE, Primitive.DIAMOND,
            Primitive.PENTAGON, Primitive.HEXAGON,
        )

    @property
    def sides(self) -> int:
        """Number of sides for polygonal forms. 0 for non-polygons."""
        return {
            Primitive.DOT: 0, Primitive.CIRCLE: 0,
            Primitive.RING: 0, Primitive.SPIRAL: 0,
            Primitive.LINE_H: 1, Primitive.LINE_V: 1,
            Primitive.LINE_DR: 1, Primitive.LINE_DL: 1,
            Primitive.TRIANGLE: 3, Primitive.INV_TRI: 3,
            Primitive.SQUARE: 4, Primitive.DIAMOND: 4,
            Primitive.PENTAGON: 5, Primitive.HEXAGON: 6,
        }.get(self, 0)


# ================================================================
#                 PLACED PRIMITIVE — A SHAPE ON THE GRID
# ================================================================

@dataclass
class PlacedPrimitive:
    """
    A geometric primitive placed at a specific position with rotation and scale.
    This is a single stroke in the glyph — one shape, positioned in space.
    """
    primitive: Primitive
    x: float = 0.0
    y: float = 0.0
    rotation: float = 0.0   # degrees
    scale: float = 1.0

    def distance_to(self, other: 'PlacedPrimitive') -> float:
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def touches(self, other: 'PlacedPrimitive', threshold: float = 1.5) -> bool:
        """Two elements touch if they are within threshold distance."""
        return self.distance_to(other) <= threshold

    @property
    def fingerprint(self) -> str:
        return f"{self.primitive.symbol}@{self.x:.1f},{self.y:.1f}r{self.rotation:.0f}s{self.scale:.1f}"


# ================================================================
#                 GLYPH — A COMPOSED GEOMETRIC CHARACTER
# ================================================================

@dataclass
class Glyph:
    """
    A composed geometric symbol — the fundamental character unit.
    Built from arranged primitives, like a ward is built from strokes.

    NOT text. Geometry. The spatial relationships ARE the meaning.

    Mathematical properties determine power:
      - Symmetry: rotational and reflective balance
      - Containment: depth of nesting (circles within circles)
      - Connectivity: how elements touch
      - Harmony: polygon-side ratios and angle relationships
    """
    name: str
    elements: List[PlacedPrimitive] = field(default_factory=list)

    def add(self, primitive: Primitive, x: float = 0.0, y: float = 0.0,
            rotation: float = 0.0, scale: float = 1.0) -> 'Glyph':
        """Add a primitive to this glyph. Returns self for chaining."""
        self.elements.append(PlacedPrimitive(primitive, x, y, rotation, scale))
        return self

    # --- MATHEMATICAL PROPERTIES ---

    @property
    def center(self) -> Tuple[float, float]:
        if not self.elements:
            return (0.0, 0.0)
        cx = sum(e.x for e in self.elements) / len(self.elements)
        cy = sum(e.y for e in self.elements) / len(self.elements)
        return (cx, cy)

    @property
    def symmetry(self) -> float:
        """
        Rotational symmetry score (0.0 to 1.0).
        Higher symmetry = more mathematically correct = more power.
        """
        if len(self.elements) <= 1:
            return 1.0

        cx, cy = self.center
        matches = 0
        total = 0

        for e in self.elements:
            # Check 180-degree rotational symmetry
            mx, my = 2 * cx - e.x, 2 * cy - e.y
            for other in self.elements:
                if (abs(other.x - mx) < 0.3 and abs(other.y - my) < 0.3
                        and other.primitive == e.primitive):
                    matches += 1
                    break
            total += 1

        return matches / total if total > 0 else 0.0

    @property
    def containment_depth(self) -> int:
        """
        How many containment-forms (circles, hexagons, etc.) are present.
        Deeper containment = stronger warding = more power.
        """
        return sum(1 for e in self.elements if e.primitive.is_containment)

    @property
    def connectivity(self) -> float:
        """
        What fraction of elements touch at least one other element.
        Disconnected elements weaken the glyph.
        """
        if len(self.elements) <= 1:
            return 1.0

        connected = 0
        for i, e in enumerate(self.elements):
            for j, other in enumerate(self.elements):
                if i != j and e.touches(other):
                    connected += 1
                    break

        return connected / len(self.elements)

    @property
    def harmony(self) -> float:
        """
        Ratio of polygon sides present. More diverse polygons = more harmony.
        Mathematical relationships between shapes create resonance.
        """
        side_counts = set()
        for e in self.elements:
            s = e.primitive.sides
            if s > 0:
                side_counts.add(s)

        if not side_counts:
            return 0.5
        # Perfect harmony uses sacred ratios (3, 4, 5, 6)
        sacred = {3, 4, 5, 6}
        overlap = side_counts & sacred
        return len(overlap) / len(sacred)

    @property
    def power(self) -> float:
        """
        POWER = mathematical correctness of composition.
        "When activated, its power is determined by how mathematically
         correct it has been parsed. Like mastery."

        Power formula:
          base (element count) +
          symmetry bonus +
          containment bonus +
          connectivity bonus +
          harmony bonus
        """
        if not self.elements:
            return 0.0

        base = min(len(self.elements) * 0.15, 2.0)
        sym_bonus = self.symmetry * 3.0
        con_bonus = min(self.containment_depth * 0.8, 3.0)
        conn_bonus = self.connectivity * 2.0
        harm_bonus = self.harmony * 2.0

        return min(base + sym_bonus + con_bonus + conn_bonus + harm_bonus, 10.0)

    @property
    def signature(self) -> str:
        """Unique cryptographic hash of this glyph's geometric structure."""
        parts = []
        for e in sorted(self.elements, key=lambda e: (e.x, e.y, e.primitive.symbol)):
            parts.append(e.fingerprint)
        raw = "|".join(parts)
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    @property
    def is_closed(self) -> bool:
        """A glyph is closed if it contains at least one containment form."""
        return self.containment_depth > 0

    @property
    def touch_map(self) -> Dict[int, List[int]]:
        """Map of which elements touch which other elements."""
        touches = {}
        for i, e in enumerate(self.elements):
            touches[i] = []
            for j, other in enumerate(self.elements):
                if i != j and e.touches(other):
                    touches[i].append(j)
        return touches

    # --- RENDERING ---

    def render_flat(self) -> str:
        """Render as a flat sequence of symbols (compact form)."""
        return "".join(e.primitive.symbol for e in self.elements)

    def render_grid(self, size: int = 9) -> str:
        """
        Render as a 2D grid showing spatial arrangement.
        This is the visual form — what you would carve in stone.
        """
        grid = [[" " for _ in range(size)] for _ in range(size)]
        mid = size // 2

        for e in self.elements:
            gx = int(round(mid + e.x))
            gy = int(round(mid + e.y))
            if 0 <= gx < size and 0 <= gy < size:
                grid[gy][gx] = e.primitive.symbol

        lines = []
        for row in grid:
            line = "".join(row)
            if line.strip():
                lines.append(line)

        return "\n".join(lines) if lines else "·"

    def __repr__(self):
        return f"Glyph<{self.name} p={self.power:.1f} [{self.render_flat()}]>"


# ================================================================
#                 GLYPH BUILDERS — Common Constructions
# ================================================================

def ward_circle(name: str, inner_primitive: Primitive = Primitive.DOT) -> Glyph:
    """
    Build a basic ward circle: outer circle containing an inner form.
    The fundamental ward shape — containment around a core.
    """
    g = Glyph(name)
    # Outer containment circle
    g.add(Primitive.CIRCLE, 0, 0, scale=2.0)
    # Cardinal connection points
    g.add(Primitive.LINE_H, -2, 0)
    g.add(Primitive.LINE_H, 2, 0)
    g.add(Primitive.LINE_V, 0, -2)
    g.add(Primitive.LINE_V, 0, 2)
    # Inner core
    g.add(inner_primitive, 0, 0)
    return g


def runic_sigil(name: str, core: Primitive, arms: int = 4) -> Glyph:
    """
    Build a runic sigil: a central form with radiating arms.
    Used for active runes (opcodes that DO things).
    """
    g = Glyph(name)
    g.add(core, 0, 0)

    angle_step = 360.0 / arms
    for i in range(arms):
        angle = math.radians(i * angle_step)
        x = round(math.cos(angle) * 2, 1)
        y = round(math.sin(angle) * 2, 1)
        g.add(Primitive.LINE_H if abs(x) > abs(y) else Primitive.LINE_V, x, y,
              rotation=i * angle_step)

    return g


def nested_containment(name: str, depth: int = 3) -> Glyph:
    """
    Build nested containment: circles within circles.
    Each layer adds warding depth and power.
    """
    g = Glyph(name)
    for d in range(depth):
        g.add(Primitive.CIRCLE, 0, 0, scale=1.0 + d)
    g.add(Primitive.DOT, 0, 0)
    return g


def key_glyph(name: str, key_form: Primitive, lock_form: Primitive) -> Glyph:
    """
    Build a Key-Glyph: composite symbol combining key + lock forms.
    "Dynamic: Key-Glyph + Simple + Eurotype sign"
    """
    g = Glyph(name)
    # Key at top
    g.add(key_form, 0, -1)
    # Connector
    g.add(Primitive.LINE_V, 0, 0)
    # Lock at bottom
    g.add(lock_form, 0, 1)
    # Ward circle containing both
    g.add(Primitive.CIRCLE, 0, 0, scale=2.0)
    return g


def geometric_word(name: str, primitives: List[Primitive]) -> Glyph:
    """
    Build a geometric word: a sequence of primitives laid out horizontally.
    This is how you compose longer expressions in the geometric language.
    """
    g = Glyph(name)
    for i, p in enumerate(primitives):
        g.add(p, i * 1.5, 0)
        if i < len(primitives) - 1:
            g.add(Primitive.LINE_H, i * 1.5 + 0.75, 0)
    return g
