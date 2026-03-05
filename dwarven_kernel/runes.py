"""
DWARVEN RUNES — The Opcode Layer
==================================

The kernel is replaced with repurposed Dwarven Runes —
already fixed with structured meaning through mathematics.
This means it is logical.

15 Core Runes (Opcodes):
    WALL    — boundary, defense perimeter
    GATE    — controlled entry/exit point
    HEART   — power source, life force
    BLADE   — offensive capability, cut/sever
    WARD    — protection, containment definition
    KEY     — authentication, unlocking
    BIND    — connection, linking, relationship
    SHIELD  — passive defense, reflection
    FORGE   — creation, transformation
    RING    — cycle, loop, repetition
    FUNNEL  — directed flow, channeling
    TOUCH   — connection point, interface between runes
    CLOSE   — seal, finalize, complete the circle
    SPREN   — recognition, validation, identity check
    STONE   — storage, persistence, memory (Sipstrassi)

Each rune has:
    - An inner glyph (canonical — used within the fortress, truth)
    - Multiple outer glyphs (shape-shifted by Surges, changes every 15-30s)
    - A geometric construction from primitives
    - Mathematical properties (symmetry, rotation, containment)
    - An opcode function (what it does when executed)

"When activated, its power is determined by how mathematically
 correct it has been parsed. Like mastery."

"It treats all tongues as foreign and is never used by them
 but can wear or use them like a glove — gain their abilities
 but none of their restrictions."
"""

import hashlib
import math
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Callable

from .glyphs import (
    Glyph, Primitive, PlacedPrimitive,
    ward_circle, runic_sigil, nested_containment, key_glyph,
)


# ================================================================
#                    RUNE OPCODES
# ================================================================

class RuneOp(Enum):
    """
    The 15 Dwarven Rune Opcodes.
    Each is a CPU instruction — the bones of execution.
    """
    WALL   = (0x01, "wall",   "boundary, defense perimeter")
    GATE   = (0x02, "gate",   "controlled entry/exit point")
    HEART  = (0x03, "heart",  "power source, life force")
    BLADE  = (0x04, "blade",  "offensive, cut/sever")
    WARD   = (0x05, "ward",   "protection, containment")
    KEY    = (0x06, "key",    "authentication, unlock")
    BIND   = (0x07, "bind",   "connection, link")
    SHIELD = (0x08, "shield", "passive defense, reflect")
    FORGE  = (0x09, "forge",  "creation, transformation")
    RING   = (0x0A, "ring",   "cycle, loop, repeat")
    FUNNEL = (0x0B, "funnel", "directed flow, channel")
    TOUCH  = (0x0C, "touch",  "connection point, interface")
    CLOSE  = (0x0D, "close",  "seal, finalize, complete circle")
    SPREN  = (0x0E, "spren",  "recognition, validate, identity")
    STONE  = (0x0F, "stone",  "storage, persistence, memory")

    def __init__(self, opcode: int, rune_id: str, desc: str):
        self.opcode = opcode
        self.rune_id = rune_id
        self.desc = desc


# ================================================================
#                    RUNE DEFINITIONS — Geometric Construction
# ================================================================

def _build_inner_glyphs() -> Dict[RuneOp, Glyph]:
    """
    Build the canonical (inner) glyph for each rune.
    These are the TRUE forms — only seen inside the fortress.
    They never change. They are truth.
    """
    glyphs = {}

    # WALL — outer circle with four lines (the four walls)
    g = Glyph("wall")
    g.add(Primitive.CIRCLE, 0, 0, scale=2.0)
    g.add(Primitive.LINE_H, -2, 0)
    g.add(Primitive.LINE_H, 2, 0)
    g.add(Primitive.LINE_V, 0, -2)
    g.add(Primitive.LINE_V, 0, 2)
    glyphs[RuneOp.WALL] = g

    # GATE — circle with a gap (the opening) and a diamond (the passage)
    g = Glyph("gate")
    g.add(Primitive.ARC_TOP, 0, -1)
    g.add(Primitive.ARC_BOT, 0, 1)
    g.add(Primitive.DIAMOND, 0, 0)
    g.add(Primitive.LINE_V, -1, 0)
    g.add(Primitive.LINE_V, 1, 0)
    glyphs[RuneOp.GATE] = g

    # HEART — nested circles with a star center (the starheart)
    g = Glyph("heart")
    g.add(Primitive.CIRCLE, 0, 0, scale=2.0)
    g.add(Primitive.CIRCLE, 0, 0, scale=1.0)
    g.add(Primitive.STAR, 0, 0)
    g.add(Primitive.WAVE, -1, 0)
    g.add(Primitive.WAVE, 1, 0)
    glyphs[RuneOp.HEART] = g

    # BLADE — triangle (cutting edge) with lines (reach)
    g = Glyph("blade")
    g.add(Primitive.TRIANGLE, 0, -1)
    g.add(Primitive.LINE_V, 0, 0)
    g.add(Primitive.LINE_V, 0, 1)
    g.add(Primitive.CROSS, 0, 2)
    glyphs[RuneOp.BLADE] = g

    # WARD — circle with hexagon inside (containment + structure)
    g = Glyph("ward")
    g.add(Primitive.CIRCLE, 0, 0, scale=2.0)
    g.add(Primitive.HEXAGON, 0, 0)
    g.add(Primitive.DOT, 0, 0)
    g.add(Primitive.LINE_DR, -1, -1)
    g.add(Primitive.LINE_DL, 1, -1)
    g.add(Primitive.LINE_H, 0, 1)
    glyphs[RuneOp.WARD] = g

    # KEY — diamond (the key shape) inside a circle (the lock)
    g = key_glyph("key", Primitive.DIAMOND, Primitive.CIRCLE)
    glyphs[RuneOp.KEY] = g

    # BIND — two circles connected by a line (linked entities)
    g = Glyph("bind")
    g.add(Primitive.CIRCLE, -1.5, 0)
    g.add(Primitive.CIRCLE, 1.5, 0)
    g.add(Primitive.LINE_H, 0, 0)
    g.add(Primitive.DOT, -1.5, 0)
    g.add(Primitive.DOT, 1.5, 0)
    glyphs[RuneOp.BIND] = g

    # SHIELD — hexagon (strength) with arcs (deflection)
    g = Glyph("shield")
    g.add(Primitive.HEXAGON, 0, 0, scale=1.5)
    g.add(Primitive.ARC_TOP, 0, -2)
    g.add(Primitive.ARC_BOT, 0, 2)
    g.add(Primitive.DOT, 0, 0)
    glyphs[RuneOp.SHIELD] = g

    # FORGE — square (anvil) with triangle (flame) and star (spark)
    g = Glyph("forge")
    g.add(Primitive.SQUARE, 0, 1)
    g.add(Primitive.TRIANGLE, 0, -1)
    g.add(Primitive.STAR, 0, -2)
    g.add(Primitive.LINE_V, -1, 0)
    g.add(Primitive.LINE_V, 1, 0)
    glyphs[RuneOp.FORGE] = g

    # RING — circle with spiral inside (cycles within cycles)
    g = Glyph("ring")
    g.add(Primitive.RING, 0, 0, scale=2.0)
    g.add(Primitive.SPIRAL, 0, 0)
    g.add(Primitive.ARROW_RT, 1, -1)
    g.add(Primitive.ARROW_DN, 1, 1)
    g.add(Primitive.ARROW_LF, -1, 1)
    g.add(Primitive.ARROW_UP, -1, -1)
    glyphs[RuneOp.RING] = g

    # FUNNEL — inverted triangle (narrowing) with lines (directed flow)
    g = Glyph("funnel")
    g.add(Primitive.INV_TRI, 0, 0, scale=1.5)
    g.add(Primitive.LINE_V, 0, 2)
    g.add(Primitive.ARROW_DN, 0, 3)
    g.add(Primitive.LINE_H, -1, -1)
    g.add(Primitive.LINE_H, 1, -1)
    glyphs[RuneOp.FUNNEL] = g

    # TOUCH — two dots with a small line between (the interface point)
    g = Glyph("touch")
    g.add(Primitive.DOT, -1, 0)
    g.add(Primitive.DOT, 1, 0)
    g.add(Primitive.LINE_H, 0, 0)
    g.add(Primitive.WAVE, 0, -0.5)
    g.add(Primitive.WAVE, 0, 0.5)
    glyphs[RuneOp.TOUCH] = g

    # CLOSE — complete circle with omega (finality)
    g = Glyph("close")
    g.add(Primitive.CIRCLE, 0, 0, scale=2.0)
    g.add(Primitive.OMEGA, 0, 0)
    g.add(Primitive.DOT, 0, -1)
    g.add(Primitive.DOT, 0, 1)
    glyphs[RuneOp.CLOSE] = g

    # SPREN — star (identity) inside hexagon (recognition structure)
    g = Glyph("spren")
    g.add(Primitive.HEXAGON, 0, 0, scale=1.5)
    g.add(Primitive.STAR, 0, 0)
    g.add(Primitive.WAVE, -1, 0)
    g.add(Primitive.WAVE, 1, 0)
    g.add(Primitive.DOT, 0, -1.5)
    g.add(Primitive.DOT, 0, 1.5)
    glyphs[RuneOp.SPREN] = g

    # STONE — square (solidity) nested in circle (permanence) with spiral (deep memory)
    g = Glyph("stone")
    g.add(Primitive.CIRCLE, 0, 0, scale=2.0)
    g.add(Primitive.SQUARE, 0, 0)
    g.add(Primitive.SPIRAL, 0, 0)
    glyphs[RuneOp.STONE] = g

    return glyphs


# Module-level canonical glyphs
INNER_GLYPHS: Dict[RuneOp, Glyph] = _build_inner_glyphs()


# ================================================================
#                    RUNE INSTANCE
# ================================================================

@dataclass
class Rune:
    """
    A single rune instance — an opcode ready for execution.

    The rune carries its glyph, its mathematical power,
    and optional arguments for its operation.
    """
    op: RuneOp
    args: Dict[str, Any] = field(default_factory=dict)
    power: float = 0.0     # set during parsing based on glyph correctness

    @property
    def glyph(self) -> Glyph:
        """The canonical (inner) glyph for this rune."""
        return INNER_GLYPHS[self.op]

    @property
    def opcode(self) -> int:
        return self.op.opcode

    def __repr__(self):
        args_str = f" {self.args}" if self.args else ""
        return f"Rune<{self.op.rune_id} 0x{self.opcode:02X} p={self.power:.1f}{args_str}>"


# ================================================================
#                    RUNE SEQUENCE — A Program
# ================================================================

class RuneSequence:
    """
    A sequence of runes — the equivalent of a program.

    Rules:
        - Must start with a containment rune (WALL, WARD, or SHIELD)
        - Must end with CLOSE (seal the circle)
        - TOUCH must sit between two runes to connect them
        - CLOSE only after a valid rune list
        - If they don't touch perfectly, the ward doesn't work

    "Patterns form like avalanche of rock and stone.
     None like the other at anything."
    """

    def __init__(self, name: str = "unnamed"):
        self.name = name
        self.runes: List[Rune] = []
        self.sealed: bool = False

    def inscribe(self, op: RuneOp, **args) -> 'RuneSequence':
        """Add a rune to the sequence. Returns self for chaining."""
        if self.sealed:
            return self  # cannot modify a sealed sequence
        self.runes.append(Rune(op=op, args=args))
        return self

    def seal(self) -> bool:
        """
        Seal the sequence. Validates structure.
        A sealed sequence cannot be modified.
        """
        if not self.runes:
            return False

        # Must end with CLOSE
        if self.runes[-1].op != RuneOp.CLOSE:
            return False

        # Must start with a containment rune
        if self.runes[0].op not in (RuneOp.WALL, RuneOp.WARD, RuneOp.SHIELD):
            return False

        # TOUCH must be between two other runes
        for i, rune in enumerate(self.runes):
            if rune.op == RuneOp.TOUCH:
                if i == 0 or i == len(self.runes) - 1:
                    return False
                if self.runes[i - 1].op == RuneOp.TOUCH:
                    return False
                if self.runes[i + 1].op == RuneOp.TOUCH:
                    return False

        self.sealed = True
        return True

    @property
    def total_power(self) -> float:
        """Total power of the sequence (sum of rune powers)."""
        if not self.sealed:
            return 0.0
        return sum(r.power for r in self.runes)

    @property
    def signature(self) -> str:
        """Unique hash of this rune sequence."""
        parts = [f"{r.op.rune_id}:{r.opcode}" for r in self.runes]
        raw = "|".join(parts)
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    def render(self) -> str:
        """Render the sequence as a flat glyph string."""
        return " ".join(r.glyph.render_flat() for r in self.runes)

    def __len__(self):
        return len(self.runes)

    def __iter__(self):
        return iter(self.runes)

    def __repr__(self):
        state = "SEALED" if self.sealed else "OPEN"
        ops = " → ".join(r.op.rune_id for r in self.runes)
        return f"RuneSequence<{self.name} {state} [{ops}] p={self.total_power:.1f}>"
