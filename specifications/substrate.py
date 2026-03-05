"""
SUBSTRATE SPECIFICATION -- Replacing Binary
==============================================
An Original Data Representation Layer

Binary is not ours. 0 and 1 belong to silicon transistors.
This specification defines our own fundamental unit of data:
the GLYPH STATE.

CORE PRINCIPLE (from the Chronicle):
  "Neurons -- firing = meaning. Not just WHAT fires,
   but WHEN and HOW OFTEN."

  "DNA = boundary & self-healing."

  "Send the same message three ways, only need two to build."

WHAT REPLACES BINARY:
  - The fundamental unit is not 0/1 (bit)
  - The fundamental unit is a GLYPH STATE
  - A glyph state has:
      * Shape (geometric primitive -- which glyph)
      * Frequency (how often it fires -- timing IS meaning)
      * Phase (when it fires relative to others)
  - Three properties, not one (richer than ternary even)

REDUNDANCY:
  "Send the same message three ways, only need two to build."
  Every message is encoded in three independent channels.
  Any two can reconstruct the third. Byzantine fault tolerance
  at the substrate level.

SELF-HEALING:
  "DNA = boundary & self-healing."
  The substrate repairs itself. If one channel corrupts,
  the other two rebuild it. Living data.

UNTIL LIVING METAL:
  Until living metal is built, silicon carries these glyph states.
  The binary beneath is invisible to our languages.
  Our languages speak in glyphs, not bits.
  The translation layer (the bridge) handles the mapping.
  When living metal arrives, the bridge is no longer needed.

(C) Anthony Eric Chavez -- The Keeper
"""

import time
import random
import hashlib
from enum import Enum, auto


# ================================================================
#  GLYPH PRIMITIVES -- The Alphabet Below the Alphabet
# ================================================================
#
#  Where binary has 0 and 1,
#  our substrate has geometric primitives.
#  These are the atoms of data representation.
#

class GlyphPrimitive(Enum):
    """The fundamental shapes. Our bits."""
    CIRCLE    = auto()
    RING      = auto()
    SPIRAL    = auto()
    DOT       = auto()
    TRIANGLE  = auto()
    SQUARE    = auto()
    DIAMOND   = auto()
    PENTAGON  = auto()
    HEXAGON   = auto()
    LINE_H    = auto()
    LINE_V    = auto()
    LINE_DR   = auto()
    LINE_DL   = auto()
    CROSS     = auto()
    ARC_TOP   = auto()
    ARC_BOT   = auto()
    WAVE      = auto()
    STAR      = auto()
    INFINITY  = auto()
    OMEGA     = auto()


# ================================================================
#  GLYPH STATE -- Replaces the Bit
# ================================================================
#
#  A bit is 0 or 1. A glyph state is:
#    - Shape: which geometric primitive
#    - Frequency: how often it fires (timing IS meaning)
#    - Phase: when it fires relative to its neighbors
#
#  Not just WHAT fires, but WHEN and HOW OFTEN.
#  This is how neurons encode meaning.
#  This is how our substrate encodes data.
#

class GlyphState:
    """
    The fundamental unit of data. Replaces the bit.

    Three properties:
      shape:     which geometric primitive (what fires)
      frequency: how often it fires (how often)
      phase:     when it fires relative to others (when)

    "Neurons -- firing = meaning.
     Not just WHAT fires, but WHEN and HOW OFTEN."
    """

    def __init__(self, shape, frequency=1.0, phase=0.0):
        """
        shape:     GlyphPrimitive enum value
        frequency: firings per cycle (0.1 to 10.0)
        phase:     offset within cycle (0.0 to 1.0)
        """
        self.shape = shape
        self.frequency = max(0.1, min(10.0, frequency))
        self.phase = phase % 1.0

    def fires_at(self, cycle_time):
        """Does this glyph state fire at the given cycle time?"""
        adjusted = (cycle_time + self.phase) * self.frequency
        return (adjusted % 1.0) < 0.1  # fires in the first 10% of each period

    @property
    def identity(self):
        """The identity of this glyph state."""
        raw = f"{self.shape.name}:{self.frequency:.2f}:{self.phase:.2f}"
        return hashlib.sha256(raw.encode()).hexdigest()[:8]

    def __repr__(self):
        return f"GS({self.shape.name}, f={self.frequency:.1f}, p={self.phase:.2f})"

    def __eq__(self, other):
        if not isinstance(other, GlyphState):
            return False
        return (self.shape == other.shape
                and abs(self.frequency - other.frequency) < 0.01
                and abs(self.phase - other.phase) < 0.01)

    def __hash__(self):
        return hash((self.shape, round(self.frequency, 2), round(self.phase, 2)))


# ================================================================
#  GLYPH WORD -- A Group of Glyph States (Replaces the Byte)
# ================================================================
#
#  Where binary has bytes (8 bits), we have glyph words.
#  A glyph word is a sequence of glyph states that together
#  carry a complete unit of meaning.
#
#  The meaning comes from:
#    - Which shapes are present
#    - Their frequencies (the rhythm)
#    - Their phases (the timing between them)
#    - The PATTERN of the whole group
#

class GlyphWord:
    """
    A group of glyph states. Replaces the byte.

    Meaning comes from the collective pattern:
    shapes, frequencies, phases, and their relationships.
    """

    def __init__(self, states=None):
        self.states = states or []

    def add(self, state):
        self.states.append(state)

    @property
    def pattern(self):
        """The pattern of shapes in this word."""
        return tuple(s.shape for s in self.states)

    @property
    def rhythm(self):
        """The frequency pattern -- the rhythm of firing."""
        return tuple(s.frequency for s in self.states)

    @property
    def timing(self):
        """The phase pattern -- when each fires relative to others."""
        return tuple(s.phase for s in self.states)

    @property
    def identity(self):
        """Unique identity of this glyph word."""
        raw = "|".join(s.identity for s in self.states)
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    def snapshot_at(self, cycle_time):
        """Which glyph states are firing at this moment in the cycle?"""
        return [s for s in self.states if s.fires_at(cycle_time)]

    def __repr__(self):
        shapes = "-".join(s.shape.name[:3] for s in self.states)
        return f"GWord[{shapes}]"

    def __len__(self):
        return len(self.states)


# ================================================================
#  TRIPLE CHANNEL -- Byzantine Redundancy
# ================================================================
#
#  "Send the same message three ways, only need two to build."
#
#  Every glyph word is sent through THREE independent channels.
#  Any two channels can reconstruct the third.
#  If one channel corrupts, the other two rebuild it.
#
#  This is not error correction borrowed from Hamming.
#  This is organ-level redundancy. DNA-level self-healing.
#  The substrate IS alive.
#

class TripleChannel:
    """
    Triple redundancy at the substrate level.

    Send the same message three ways.
    Only need two to build.
    Self-healing. Living data.
    """

    def __init__(self):
        self.channel_a = None   # primary
        self.channel_b = None   # secondary
        self.channel_c = None   # tertiary
        self.corrupted = set()  # which channels are corrupted

    def encode(self, glyph_word):
        """
        Encode a glyph word into three channels.
        Each channel carries the full message independently.
        """
        self.channel_a = glyph_word
        self.channel_b = self._transform_b(glyph_word)
        self.channel_c = self._transform_c(glyph_word)
        self.corrupted = set()

    def _transform_b(self, word):
        """
        Channel B: same data, shifted phase.
        The rhythm changes, the meaning persists.
        """
        shifted = GlyphWord()
        for state in word.states:
            shifted.add(GlyphState(
                shape=state.shape,
                frequency=state.frequency,
                phase=(state.phase + 0.333) % 1.0,
            ))
        return shifted

    def _transform_c(self, word):
        """
        Channel C: same data, reversed order, shifted phase.
        Different arrangement, same meaning.
        """
        reversed_states = GlyphWord()
        for state in reversed(word.states):
            reversed_states.add(GlyphState(
                shape=state.shape,
                frequency=state.frequency,
                phase=(state.phase + 0.667) % 1.0,
            ))
        return reversed_states

    def corrupt(self, channel):
        """Simulate corruption of a channel."""
        self.corrupted.add(channel)
        if channel == "a":
            self.channel_a = None
        elif channel == "b":
            self.channel_b = None
        elif channel == "c":
            self.channel_c = None

    def decode(self):
        """
        Decode the message. Only need two good channels.
        Self-healing: if one is corrupted, rebuild from the other two.
        """
        good_channels = []
        if self.channel_a is not None and "a" not in self.corrupted:
            good_channels.append(("a", self.channel_a))
        if self.channel_b is not None and "b" not in self.corrupted:
            good_channels.append(("b", self.channel_b))
        if self.channel_c is not None and "c" not in self.corrupted:
            good_channels.append(("c", self.channel_c))

        if len(good_channels) < 2:
            return {
                "decoded": False,
                "reason": "Fewer than 2 channels intact. Cannot reconstruct.",
                "good_channels": len(good_channels),
            }

        # Use the first good channel to reconstruct
        name, primary = good_channels[0]

        # Reverse the transformation to get back to original
        if name == "a":
            original = primary
        elif name == "b":
            original = self._reverse_b(primary)
        elif name == "c":
            original = self._reverse_c(primary)

        # Self-heal: rebuild corrupted channels
        healed = []
        if "a" in self.corrupted:
            self.channel_a = original
            self.corrupted.discard("a")
            healed.append("a")
        if "b" in self.corrupted:
            self.channel_b = self._transform_b(original)
            self.corrupted.discard("b")
            healed.append("b")
        if "c" in self.corrupted:
            self.channel_c = self._transform_c(original)
            self.corrupted.discard("c")
            healed.append("c")

        return {
            "decoded": True,
            "word": original,
            "healed_channels": healed,
            "self_healed": len(healed) > 0,
        }

    def _reverse_b(self, word):
        """Reverse channel B transformation."""
        original = GlyphWord()
        for state in word.states:
            original.add(GlyphState(
                shape=state.shape,
                frequency=state.frequency,
                phase=(state.phase - 0.333) % 1.0,
            ))
        return original

    def _reverse_c(self, word):
        """Reverse channel C transformation."""
        original = GlyphWord()
        for state in reversed(word.states):
            original.add(GlyphState(
                shape=state.shape,
                frequency=state.frequency,
                phase=(state.phase - 0.667) % 1.0,
            ))
        return original


# ================================================================
#  THE BRIDGE -- Glyph States to Silicon (Temporary)
# ================================================================
#
#  Until living metal exists, silicon carries glyph states.
#  The bridge translates between glyph states and binary.
#  Our languages never see binary. They speak in glyphs.
#
#  When living metal arrives, the bridge is removed.
#  The glyphs ARE the substrate. No translation needed.
#

class Bridge:
    """
    The temporary translation layer between glyph states and silicon.

    Our languages speak in glyphs, not bits.
    The bridge handles the mapping to binary.
    This bridge is TEMPORARY. It exists only because
    living metal has not yet been built.
    """

    # Each glyph primitive maps to a 5-bit code (20 primitives, need 5 bits)
    PRIMITIVE_TO_BINARY = {prim: format(i, '05b') for i, prim in enumerate(GlyphPrimitive)}
    BINARY_TO_PRIMITIVE = {v: k for k, v in PRIMITIVE_TO_BINARY.items()}

    @staticmethod
    def glyph_state_to_bits(state):
        """
        Translate a glyph state to binary for silicon to carry.
        The glyph state doesn't know about binary. The bridge does.

        Format: [5 bits shape][7 bits frequency][7 bits phase] = 19 bits per state
        """
        shape_bits = Bridge.PRIMITIVE_TO_BINARY[state.shape]
        freq_int = int(state.frequency * 10)  # 0-100 range, 7 bits
        freq_bits = format(min(freq_int, 127), '07b')
        phase_int = int(state.phase * 100)    # 0-99 range, 7 bits
        phase_bits = format(min(phase_int, 127), '07b')
        return shape_bits + freq_bits + phase_bits

    @staticmethod
    def bits_to_glyph_state(bits):
        """
        Translate binary back to a glyph state.
        Silicon speaks binary. We translate to glyphs.
        """
        if len(bits) < 19:
            return None
        shape_bits = bits[:5]
        freq_bits = bits[5:12]
        phase_bits = bits[12:19]

        shape = Bridge.BINARY_TO_PRIMITIVE.get(shape_bits)
        if shape is None:
            return None
        frequency = int(freq_bits, 2) / 10.0
        phase = int(phase_bits, 2) / 100.0
        return GlyphState(shape, frequency, phase)

    @staticmethod
    def glyph_word_to_bits(word):
        """Translate a glyph word to binary."""
        return "".join(Bridge.glyph_state_to_bits(s) for s in word.states)

    @staticmethod
    def bits_to_glyph_word(bits):
        """Translate binary to a glyph word."""
        word = GlyphWord()
        for i in range(0, len(bits), 19):
            chunk = bits[i:i+19]
            if len(chunk) == 19:
                state = Bridge.bits_to_glyph_state(chunk)
                if state:
                    word.add(state)
        return word


# ================================================================
#  SUBSTRATE -- The Complete Data Layer
# ================================================================
#
#  This is the bottom of the stack.
#  Below the Dwarven Runes, below the Wards, below Naming.
#  The substrate is what data IS MADE OF.
#
#  On silicon: glyph states carried by binary through the Bridge.
#  On living metal: glyph states ARE the metal. No bridge needed.
#

class Substrate:
    """
    The complete data representation layer.

    Replaces binary as the conceptual foundation.
    Our languages think in glyphs, not bits.
    The Bridge handles silicon translation (temporary).
    """

    def __init__(self, living_metal=False):
        self.living_metal = living_metal
        self.bridge = None if living_metal else Bridge()
        self.channels = {}  # name -> TripleChannel

    def store(self, name, glyph_word):
        """
        Store a glyph word with triple redundancy.
        Three channels. Only need two. Self-healing.
        """
        channel = TripleChannel()
        channel.encode(glyph_word)
        self.channels[name] = channel
        return {
            "stored": True,
            "name": name,
            "channels": 3,
            "self_healing": True,
            "living_metal": self.living_metal,
        }

    def retrieve(self, name):
        """
        Retrieve a glyph word. Self-heals if any channel corrupted.
        """
        channel = self.channels.get(name)
        if not channel:
            return {"retrieved": False, "reason": f"No data named '{name}'."}

        result = channel.decode()
        if result["decoded"]:
            return {
                "retrieved": True,
                "name": name,
                "word": result["word"],
                "self_healed": result["self_healed"],
                "healed_channels": result.get("healed_channels", []),
            }
        return {"retrieved": False, "reason": result["reason"]}

    def to_silicon(self, glyph_word):
        """Translate to binary for silicon. Only works with the Bridge."""
        if self.living_metal:
            return {"error": "Living metal does not need binary."}
        return {"bits": self.bridge.glyph_word_to_bits(glyph_word)}

    def from_silicon(self, bits):
        """Translate from binary back to glyphs."""
        if self.living_metal:
            return {"error": "Living metal does not speak binary."}
        return {"word": self.bridge.bits_to_glyph_word(bits)}
