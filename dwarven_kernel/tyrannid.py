"""
TYRANNID — Packet Channeling into Solid Structure
===================================================

The Tyrannid makes packets/processes go through certain channels.
These channels form STRUCTURES — constant data flow creates persistence.
You can build entire buildings inside the walls — real buildings that are solid.

They're solid because data has to go through these channels CONSTANTLY.
Overlays are thrown over them so the world becomes 3D and solid.

"Solid structures real and everything — cities, walls, and wonder."

Data flow through channels = structure.
Constant flow = solidity.
Overlays = 3D visualization.
Code becomes architecture. Architecture becomes world.
"""

import time
import hashlib
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum


# ================================================================
#                    CHANNEL TYPES
# ================================================================

class ChannelType(Enum):
    """Types of data channels that form structures."""
    BACKBONE  = ("backbone",  "primary structural support — load-bearing")
    CONDUIT   = ("conduit",   "secondary channel — utility routing")
    ARTERIAL  = ("arterial",  "high-flow main channel — major throughput")
    CAPILLARY = ("capillary", "fine detail channel — precision structures")
    NEURAL    = ("neural",    "signal channel — control and communication")

    def __init__(self, channel_id: str, desc: str):
        self.channel_id = channel_id
        self.desc = desc


# ================================================================
#                    CHANNEL — A Single Data Path
# ================================================================

@dataclass
class Channel:
    """
    A single data channel. Data flows through it constantly.
    The constant flow makes it persistent — a physical structure.
    """
    channel_id: str
    channel_type: ChannelType
    origin: str
    destination: str
    flow_rate: float = 0.0       # current data flow rate
    coherence: float = 0.0       # how solid this channel is (0.0-1.0)
    created_at: float = field(default_factory=time.time)

    @property
    def age(self) -> float:
        return time.time() - self.created_at

    @property
    def is_solid(self) -> bool:
        """A channel becomes solid when coherence exceeds threshold."""
        return self.coherence >= 0.7

    def flow(self, data_mass: float):
        """Push data through this channel. Increases coherence."""
        self.flow_rate = data_mass
        # Coherence grows with constant flow, decays without it
        self.coherence = min(self.coherence + data_mass * 0.01, 1.0)

    def decay(self, amount: float = 0.001):
        """Without flow, coherence decays — structure weakens."""
        self.coherence = max(self.coherence - amount, 0.0)

    def receive_radiance(self, radiance: float):
        """
        Receive Radiance from an Everstorm.
        Makes the structure more coherent.
        """
        self.coherence = min(self.coherence + radiance * 0.05, 1.0)


# ================================================================
#                    STRUCTURE — A 3D Building
# ================================================================

@dataclass
class Structure:
    """
    A 3D structure built from interconnected channels.
    Real buildings that are solid because data constantly flows through them.

    "Cities, walls, and wonder."
    """
    name: str
    structure_type: str       # "building", "wall", "tower", "bridge", etc.
    channels: List[Channel] = field(default_factory=list)
    position: Dict[str, float] = field(default_factory=lambda: {"x": 0, "y": 0, "z": 0})
    overlay_applied: bool = False

    @property
    def coherence(self) -> float:
        """Average coherence of all channels in this structure."""
        if not self.channels:
            return 0.0
        return sum(c.coherence for c in self.channels) / len(self.channels)

    @property
    def is_solid(self) -> bool:
        """Structure is solid when average coherence is high."""
        return self.coherence >= 0.6

    @property
    def is_3d(self) -> bool:
        """Structure appears in 3D when overlay is applied and it's solid."""
        return self.overlay_applied and self.is_solid

    def apply_overlay(self):
        """Throw an overlay over the channels — world becomes 3D."""
        self.overlay_applied = True

    def tick(self, data_mass: float):
        """One tick — push data through all channels."""
        per_channel = data_mass / len(self.channels) if self.channels else 0
        for channel in self.channels:
            channel.flow(per_channel)

    def receive_everstorm(self, radiance: float):
        """Everstorm rains energy — makes this structure more coherent."""
        for channel in self.channels:
            channel.receive_radiance(radiance)

    def __repr__(self):
        state = "3D_SOLID" if self.is_3d else ("SOLID" if self.is_solid else "FORMING")
        return f"Structure<{self.name} {self.structure_type} {state} c={self.coherence:.0%}>"


# ================================================================
#                    TYRANNID — The Structure Engine
# ================================================================

class Tyrannid:
    """
    The Tyrannid — routes packets/processes through fixed channels.
    These channels become persistent structures.
    Overlays make them 3D.

    Constant flow = solidity.
    The world IS the running code.
    The code IS the buildings.

    "The end of code. The beginning of structure."
    """

    def __init__(self):
        self.channels: Dict[str, Channel] = {}
        self.structures: Dict[str, Structure] = {}
        self._channel_counter: int = 0

    def create_channel(self, channel_type: ChannelType,
                       origin: str, destination: str) -> Channel:
        """Create a new data channel."""
        self._channel_counter += 1
        ch = Channel(
            channel_id=f"ch_{self._channel_counter}",
            channel_type=channel_type,
            origin=origin,
            destination=destination,
        )
        self.channels[ch.channel_id] = ch
        return ch

    def build_structure(self, name: str, structure_type: str,
                        channel_types: List[ChannelType],
                        position: Optional[Dict[str, float]] = None) -> Structure:
        """
        Build a new structure from channels.
        The more channels, the more complex the structure.
        """
        channels = []
        for ct in channel_types:
            ch = self.create_channel(ct, f"{name}_in", f"{name}_out")
            channels.append(ch)

        structure = Structure(
            name=name,
            structure_type=structure_type,
            channels=channels,
            position=position or {"x": 0, "y": 0, "z": 0},
        )
        structure.apply_overlay()
        self.structures[name] = structure
        return structure

    def route_packet(self, packet: Dict[str, Any], channel_id: str) -> bool:
        """Route a packet through a specific channel."""
        ch = self.channels.get(channel_id)
        if ch is None:
            return False
        ch.flow(packet.get("mass", 1.0))
        return True

    def tick(self, global_data_flow: float = 1.0):
        """
        Global tick — push data through all channels.
        Structures maintain solidity. Without flow, they decay.
        """
        for structure in self.structures.values():
            structure.tick(global_data_flow)

        # Decay unused standalone channels
        for ch in self.channels.values():
            if ch.flow_rate <= 0:
                ch.decay()

    def everstorm(self, radiance: float):
        """An Everstorm hits — all structures receive Radiance."""
        for structure in self.structures.values():
            structure.receive_everstorm(radiance)

    def status(self) -> dict:
        return {
            "channels": len(self.channels),
            "structures": len(self.structures),
            "solid_structures": sum(1 for s in self.structures.values() if s.is_solid),
            "3d_structures": sum(1 for s in self.structures.values() if s.is_3d),
            "structure_details": {
                name: {
                    "type": s.structure_type,
                    "coherence": round(s.coherence, 3),
                    "solid": s.is_solid,
                    "3d": s.is_3d,
                    "channels": len(s.channels),
                }
                for name, s in self.structures.items()
            },
        }

    def __repr__(self):
        solid = sum(1 for s in self.structures.values() if s.is_solid)
        return f"Tyrannid<channels={len(self.channels)} structures={len(self.structures)} solid={solid}>"
