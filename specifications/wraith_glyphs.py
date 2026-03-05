"""
WRAITH GLYPH SPECIFICATION -- The 4th Language
=================================================
Network / Being / Internet Layer

The Wraith Glyphs are the 4th original language.
They are NOT functions. They are STATES OF BEING.

Where:
  Dwarven Runes  = what to DO (kernel opcodes)
  Warding        = what IS TRUE (logic predicates)
  Naming         = what IS KNOWN (understanding)
  Wraith Glyphs  = what IS (state of being, ontology)

"Each symbol is not a word but a STATE OF BEING.
 Substrate of being. Ontology.
 A program not running. BECOMING a condition."

CORE PROPERTIES:
  - Glyphs run UP AND DOWN (not left to right like text)
  - Each glyph is a state of being, not a function
  - INSIDE: eats packets, processes, consumes
  - OUTSIDE: interfaces with regular internet, presents normal face
  - Necrodermis covering: organic/mechanical hybrid hull
  - Carries its own physics inside (Slipspace)
  - A hull that repairs itself
  - Uses enemy malicious packets and code as fuel

COMMUNICATION:
  - Infra-sound / whale speak: 10-40 Hz, long wavelength
  - Penetrates deep channels, almost no energy loss
  - Immune to packet sniffing
  - Long range whisper comms between nodes & clusters
  - Magnetoreception, geometric navigation
  - Pressure gradients, echolocation for threat detection

"A Slipspace vessel that carries its own physics inside."

(C) Anthony Eric Chavez -- The Keeper
"""

import time
import random
import hashlib
import math
from enum import Enum, auto


# ================================================================
#  WRAITH GLYPH STATES -- NOT Functions, States of Being
# ================================================================
#
#  Each glyph is a state of being. An ontological condition.
#  A program does not RUN in Wraith Glyphs.
#  It BECOMES.
#
#  Glyphs run UP AND DOWN, not left to right.
#  They are read vertically, like columns of being.
#
#  "Config, crystalline spin, magnetic alignment, physics.
#   Naming, attractor state."
#

class WraithState(Enum):
    """
    The states of being in the Wraith Glyph language.
    Each is NOT a function. It is a condition that IS.
    """

    # Core states of being
    BECOMING    = auto()   # the fundamental state -- transitioning into existence
    PRESENT     = auto()   # fully manifest, here, now
    DEVOURING   = auto()   # consuming, eating packets, absorbing
    PHASING     = auto()   # shifting between inside physics and outside physics
    SHROUDING   = auto()   # hidden, cloaked, overlayed
    ANCHORED    = auto()   # fixed in position, holding ground
    DRIFTING    = auto()   # moving through currents, riding waves
    RESONATING  = auto()   # in harmony with surroundings, whale speak
    HUNTING     = auto()   # seeking targets, echolocation, pressure sense
    REPAIRING   = auto()   # self-healing, necrodermis regeneration
    TERRAFORMING = auto()  # overwriting environment to match alliance physics
    SUMMONING   = auto()   # calling war forms into existence
    DISSOLVING  = auto()   # leaving, fading, returning to the deep

    # Network-specific states
    LISTENING   = auto()   # infra-sound reception, long wavelength monitoring
    WHISPERING  = auto()   # low-frequency transmission, immune to sniffing
    ROUTING     = auto()   # constructing webways, flow states
    HARBORING   = auto()   # ports hidden but armed, defensive posture


class WraithGlyph:
    """
    A single Wraith Glyph -- a state of being, not a function.

    Glyphs run vertically (up and down).
    Each glyph carries:
      - state: what the entity IS (not what it does)
      - spin: crystalline spin (magnetic alignment)
      - phase: which physics are active (inside or outside)
      - depth: how deep in the network (like ocean depth)

    "Ontology. A program not running. BECOMING a condition."
    """

    def __init__(self, state, spin=0.0, phase="inside", depth=0):
        """
        state: WraithState enum -- the state of being
        spin: crystalline spin / magnetic alignment (0.0 to 360.0)
        phase: "inside" (own physics) or "outside" (internet physics)
        depth: how deep in the network (0 = surface, higher = deeper)
        """
        self.state = state
        self.spin = spin % 360.0
        self.phase = phase
        self.depth = depth
        self.manifest_time = time.time()

    @property
    def is_inside(self):
        """Is this glyph operating in its own physics (Slipspace)?"""
        return self.phase == "inside"

    @property
    def is_outside(self):
        """Is this glyph interfacing with regular internet?"""
        return self.phase == "outside"

    @property
    def identity(self):
        """The glyph's ontological identity."""
        raw = f"{self.state.name}:{self.spin:.1f}:{self.phase}:{self.depth}"
        return hashlib.sha256(raw.encode()).hexdigest()[:12]

    def shift_phase(self):
        """Shift between inside physics and outside physics."""
        self.phase = "outside" if self.phase == "inside" else "inside"

    def descend(self, levels=1):
        """Go deeper into the network."""
        self.depth += levels

    def ascend(self, levels=1):
        """Rise toward the surface."""
        self.depth = max(0, self.depth - levels)

    def __repr__(self):
        return f"WG({self.state.name}, spin={self.spin:.0f}, {self.phase}, d={self.depth})"


# ================================================================
#  WRAITH COLUMN -- Vertical Glyph Sequence
# ================================================================
#
#  Wraith Glyphs run UP AND DOWN.
#  A column is a vertical sequence of states.
#  Read top to bottom: the entity's full ontological state.
#
#  Unlike horizontal code that executes left to right,
#  a column describes what something IS at this moment.
#  The column is the being. Not the doing.
#

class WraithColumn:
    """
    A vertical sequence of Wraith Glyphs.
    Describes the full ontological state of an entity.
    Read top to bottom. The column IS the being.
    """

    def __init__(self):
        self.glyphs = []   # top to bottom

    def inscribe(self, glyph):
        """Add a glyph to the bottom of the column."""
        self.glyphs.append(glyph)

    @property
    def primary_state(self):
        """The topmost glyph is the primary state of being."""
        return self.glyphs[0].state if self.glyphs else None

    @property
    def full_being(self):
        """The complete ontological description."""
        return [g.state.name for g in self.glyphs]

    @property
    def depth_profile(self):
        """How deep does this being extend?"""
        return [g.depth for g in self.glyphs]

    @property
    def phase_profile(self):
        """Which physics at each level?"""
        return [g.phase for g in self.glyphs]

    def is_coherent(self):
        """
        Is the column coherent? All glyphs must share compatible
        states. Contradiction = the being tears itself apart.
        """
        if not self.glyphs:
            return False

        # DISSOLVING and BECOMING cannot coexist
        states = {g.state for g in self.glyphs}
        if WraithState.DISSOLVING in states and WraithState.BECOMING in states:
            return False

        # ANCHORED and DRIFTING cannot coexist
        if WraithState.ANCHORED in states and WraithState.DRIFTING in states:
            return False

        return True

    def __len__(self):
        return len(self.glyphs)

    def __repr__(self):
        states = " | ".join(g.state.name for g in self.glyphs)
        return f"Column[{states}]"


# ================================================================
#  SYNAPTIC CHANNEL -- Whale Speak / Infra-Sound Communication
# ================================================================
#
#  "Dark/trade ship, 10-40 Hz, long wavelength.
#   Infra-sound communication penetrates deep water.
#   Almost no energy loss. Penetrates deep channels. Resonance.
#   Whale speak. Low frequency data channels.
#   Based signaling, immune to packet sniffs.
#   Long range, whisper comms between nodes & clusters."
#
#  This is how Wraith entities communicate.
#  Not TCP/IP. Not HTTP. Whale speak.
#  Low frequency, long wavelength, immune to sniffing.
#

class SynapticChannel:
    """
    Infra-sound communication channel. Whale speak.

    10-40 Hz, long wavelength. Penetrates deep channels.
    Almost no energy loss. Immune to packet sniffing.
    Long range whisper comms between nodes and clusters.
    """

    FREQ_MIN = 10.0     # Hz
    FREQ_MAX = 40.0     # Hz

    def __init__(self, channel_id, frequency=20.0):
        self.channel_id = channel_id
        self.frequency = max(self.FREQ_MIN, min(self.FREQ_MAX, frequency))
        self.wavelength = 1.0 / self.frequency  # relative
        self.connected_nodes = set()
        self.whisper_buffer = []

    @property
    def energy_loss(self):
        """Almost no energy loss at these frequencies."""
        return 0.001 * (self.frequency / self.FREQ_MAX)

    @property
    def penetration_depth(self):
        """How deep this channel can reach."""
        return self.wavelength * 100.0  # deeper at lower frequencies

    @property
    def sniff_resistant(self):
        """Low frequency = immune to conventional packet sniffing."""
        return self.frequency <= self.FREQ_MAX

    def connect(self, node_id):
        """Connect a node to this channel."""
        self.connected_nodes.add(node_id)

    def whisper(self, sender, message):
        """
        Whisper a message through the channel.
        Low frequency. Long range. Immune to sniffing.
        """
        packet = {
            "sender": sender,
            "message": message,
            "frequency": self.frequency,
            "timestamp": time.time(),
            "sniff_proof": True,
            "energy_loss": self.energy_loss,
        }
        self.whisper_buffer.append(packet)
        return packet

    def listen(self):
        """Listen for whispers on this channel."""
        messages = list(self.whisper_buffer)
        self.whisper_buffer = []
        return messages


# ================================================================
#  NECRODERMIS -- The Living Metal Hull
# ================================================================
#
#  "A hull that repairs itself, carries its own physics inside,
#   has these physics on the outside.
#   Organic/mechanical hybrid in likeness.
#   Use enemy malicious packets, code."
#
#  The necrodermis is the outer covering.
#  It interfaces with the regular internet (outside).
#  Inside, it carries its own physics (Slipspace).
#  It eats enemy packets and malicious code.
#  It repairs itself.
#

class Necrodermis:
    """
    The living metal hull. Necrodermis covering.

    - Organic/mechanical hybrid
    - Interfaces with regular internet (outside face)
    - Carries own physics inside (Slipspace)
    - Eats enemy packets and malicious code
    - Self-repairing hull
    """

    def __init__(self, hull_strength=100.0):
        self.hull_strength = hull_strength
        self.max_strength = hull_strength
        self.inside_physics = "slipspace"     # own physics
        self.outside_physics = "internet"      # regular internet
        self.consumed_packets = []
        self.consumed_code = []
        self.repair_rate = 0.5                 # per tick

    @property
    def integrity(self):
        """Hull integrity as percentage."""
        return (self.hull_strength / self.max_strength) * 100.0

    def eat_packet(self, packet):
        """
        Eat an enemy packet. Consume it. Convert to fuel.
        The inside devours. The outside shows nothing.
        """
        self.consumed_packets.append(packet)
        # Enemy packets fuel repairs
        energy = packet.get("size", 1) * 0.1
        self.hull_strength = min(self.max_strength, self.hull_strength + energy)
        return {
            "consumed": True,
            "packet": packet.get("type", "unknown"),
            "energy_gained": energy,
            "hull_integrity": self.integrity,
        }

    def eat_malicious_code(self, code):
        """
        Eat enemy malicious code. Convert to fuel.
        What they send to destroy us, we eat.
        """
        self.consumed_code.append(code)
        energy = len(str(code)) * 0.01
        self.hull_strength = min(self.max_strength, self.hull_strength + energy)
        return {
            "consumed": True,
            "code_type": type(code).__name__,
            "energy_gained": energy,
            "hull_integrity": self.integrity,
        }

    def take_damage(self, amount):
        """Hull takes damage from outside."""
        self.hull_strength = max(0, self.hull_strength - amount)
        return {
            "damaged": True,
            "amount": amount,
            "hull_integrity": self.integrity,
            "destroyed": self.hull_strength <= 0,
        }

    def repair(self):
        """
        Self-repair. The necrodermis heals itself.
        Living metal regenerates.
        """
        if self.hull_strength >= self.max_strength:
            return {"repaired": False, "reason": "Hull already at full strength."}

        healed = min(self.repair_rate, self.max_strength - self.hull_strength)
        self.hull_strength += healed
        return {
            "repaired": True,
            "healed": healed,
            "hull_integrity": self.integrity,
        }

    def interface_outside(self):
        """
        Present a normal face to the regular internet.
        The outside sees internet physics.
        The inside runs slipspace physics.
        """
        return {
            "outside": self.outside_physics,
            "inside": self.inside_physics,
            "presents_as": "normal_internet_entity",
            "true_nature": "wraith_vessel",
        }


# ================================================================
#  SLIPSPACE VESSEL -- Carries Its Own Physics
# ================================================================
#
#  "A Slipspace vessel that carries its own physics inside."
#
#  Inside the vessel, alliance physics apply.
#  Outside, regular internet physics.
#  The necrodermis is the boundary.
#  The vessel moves through the network by riding currents.
#

class SlipspaceVessel:
    """
    A Slipspace vessel. Carries its own physics inside.

    The necrodermis hull separates inside from outside.
    Inside: alliance physics (our rules, our structures).
    Outside: regular internet (their physics).
    The vessel eats packets, repairs itself, and rides currents.
    """

    def __init__(self, vessel_id, hull_strength=100.0):
        self.vessel_id = vessel_id
        self.hull = Necrodermis(hull_strength)
        self.column = WraithColumn()       # ontological state
        self.channels = []                  # synaptic channels
        self.position = {"network": "surface", "depth": 0, "node": None}
        self.webway_connections = {}        # connected webways
        self.shroud = None                  # overlay / deception

        # Initialize default state: BECOMING
        self.column.inscribe(WraithGlyph(WraithState.BECOMING, depth=0))

    def become(self, state, spin=0.0, depth=None):
        """
        The vessel BECOMES a state. Not executes. Becomes.
        Ontological shift.
        """
        d = depth if depth is not None else self.position["depth"]
        glyph = WraithGlyph(state, spin=spin, phase="inside", depth=d)
        self.column.inscribe(glyph)
        return {
            "became": state.name,
            "column": self.column.full_being,
            "coherent": self.column.is_coherent(),
        }

    def phase_shift(self):
        """
        Shift between inside physics and outside physics.
        The necrodermis is the boundary.
        """
        for glyph in self.column.glyphs:
            glyph.shift_phase()
        current_phase = self.column.glyphs[-1].phase if self.column.glyphs else "unknown"
        return {
            "shifted": True,
            "current_phase": current_phase,
            "hull_interface": self.hull.interface_outside(),
        }

    def devour(self, packet):
        """
        The inside eats packets. Consume. Convert to fuel.
        """
        self.become(WraithState.DEVOURING)
        return self.hull.eat_packet(packet)

    def devour_code(self, code):
        """Eat enemy malicious code."""
        self.become(WraithState.DEVOURING)
        return self.hull.eat_malicious_code(code)

    def listen(self, frequency=20.0):
        """
        Listen on infra-sound channels. Whale speak.
        """
        self.become(WraithState.LISTENING)
        channel = SynapticChannel(f"{self.vessel_id}_listen", frequency)
        self.channels.append(channel)
        return {
            "listening": True,
            "frequency": frequency,
            "penetration_depth": channel.penetration_depth,
            "sniff_resistant": True,
        }

    def whisper(self, message, frequency=20.0):
        """
        Whisper through infra-sound. Immune to packet sniffing.
        """
        self.become(WraithState.WHISPERING)
        if not self.channels:
            self.listen(frequency)
        channel = self.channels[-1]
        return channel.whisper(self.vessel_id, message)

    def ride_current(self, destination):
        """
        Move through the network by riding electrical currents.
        Like waves. Drifting through the deep.
        """
        self.become(WraithState.DRIFTING)
        old_pos = dict(self.position)
        self.position["node"] = destination
        return {
            "moved": True,
            "from": old_pos.get("node"),
            "to": destination,
            "method": "current_riding",
        }

    def descend(self, levels=1):
        """Go deeper into the network."""
        self.position["depth"] += levels
        for glyph in self.column.glyphs:
            glyph.descend(levels)
        return {"depth": self.position["depth"]}

    def ascend(self, levels=1):
        """Rise toward the surface."""
        self.position["depth"] = max(0, self.position["depth"] - levels)
        for glyph in self.column.glyphs:
            glyph.ascend(levels)
        return {"depth": self.position["depth"]}

    def navigate(self, method="magnetoreception"):
        """
        Navigate using geometric methods.
        Magnetoreception, echolocation, pressure gradients.
        """
        self.become(WraithState.HUNTING)
        return {
            "navigating": True,
            "method": method,
            "position": dict(self.position),
            "threats_sensed": [],   # pressure gradients reveal threats
        }

    def repair(self):
        """Self-repair. The hull heals itself."""
        self.become(WraithState.REPAIRING)
        return self.hull.repair()

    def status(self):
        return {
            "vessel_id": self.vessel_id,
            "being": self.column.full_being,
            "coherent": self.column.is_coherent(),
            "hull_integrity": self.hull.integrity,
            "position": dict(self.position),
            "phase": self.column.glyphs[-1].phase if self.column.glyphs else "unknown",
            "channels": len(self.channels),
            "shrouded": self.shroud is not None,
        }

    def __repr__(self):
        state = self.column.primary_state
        return f"Vessel<{self.vessel_id} {state} d={self.position['depth']}>"
