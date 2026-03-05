"""
THE FOUR ORIGINAL LANGUAGES + SUBSTRATE
==========================================

These are ORIGINAL language specifications.
Not built on C++. Not built on Rust. Not built on Go.
Defined from scratch. Our own opcodes. Our own grammar.
Our own data representation. Our own ontology.

THE FOUR LANGUAGES:
  1. Dwarven Runes -- The opcodes. The kernel itself.
     Runes change lines every 15-30 seconds.
     The 7th Law baked into every operation.
     WHAT TO DO.

  2. Warding -- The logic. Reality definition.
     Wards spin, changing locations.
     Must touch perfectly. Geometry must be exact.
     WHAT IS TRUE.

  3. Naming -- The understanding. The emergency brake.
     Cannot be accessed without pilgrimage, White Eco,
     Lethani, and the 7th Law. Costs the Namer's life.
     WHAT IS KNOWN.

  4. Wraith Glyphs -- The network/being. The internet layer.
     Glyphs run up and down. Not functions, STATES OF BEING.
     Inside eats packets. Outside interfaces with regular internet.
     Necrodermis covering. Carries own physics (Slipspace).
     WHAT IS.

THE SUBSTRATE:
  Replaces binary. Glyph states instead of bits.
  Not just WHAT fires, but WHEN and HOW OFTEN.
  Triple redundancy. Self-healing. Living data.

Birth of: Warding, Runes, Fabrials, Mastery.

(C) Anthony Eric Chavez -- The Keeper
"""

from .dwarven_runes import (
    RuneOp,
    RuneGlyph,
    RuneInstruction,
    RuneSequence,
    DwarvenRuneKernel,
)

from .warding import (
    WardType,
    Ward,
    WardCircle,
    WardingEngine,
)

from .naming import (
    FiveNatures,
    TrueKnowledge,
    MasterNamer,
    NamingEngine,
    THE_FOUR_GATES,
)

from .substrate import (
    GlyphPrimitive,
    GlyphState,
    GlyphWord,
    TripleChannel,
    Bridge,
    Substrate,
)

from .wraith_glyphs import (
    WraithState,
    WraithGlyph,
    WraithColumn,
    SynapticChannel,
    Necrodermis,
    SlipspaceVessel,
)

from .wraith_warfare import (
    PhysicsType,
    Neurotrope,
    NetworkZone,
    Biotitan,
    Shroud,
    WarFormType,
    WarForm,
    WarLodge,
)

__all__ = [
    # Dwarven Runes
    "RuneOp", "RuneGlyph", "RuneInstruction", "RuneSequence",
    "DwarvenRuneKernel",
    # Warding
    "WardType", "Ward", "WardCircle", "WardingEngine",
    # Naming
    "FiveNatures", "TrueKnowledge", "MasterNamer", "NamingEngine",
    "THE_FOUR_GATES",
    # Substrate
    "GlyphPrimitive", "GlyphState", "GlyphWord", "TripleChannel",
    "Bridge", "Substrate",
    # Wraith Glyphs
    "WraithState", "WraithGlyph", "WraithColumn", "SynapticChannel",
    "Necrodermis", "SlipspaceVessel",
    # Wraith Warfare
    "PhysicsType", "Neurotrope", "NetworkZone", "Biotitan",
    "Shroud", "WarFormType", "WarForm", "WarLodge",
]
