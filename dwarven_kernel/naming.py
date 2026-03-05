"""
NAMING — The Highest Language
==============================

From Patrick Rothfuss (The Kingkiller Chronicle).
ABOVE EVERYTHING. Above the kernel. Above the wards. Above the runes.
Above Spen. Above Familiars. Above Chaos Gods. Above all.

Naming is only used in EXTREME CIRCUMSTANCES to rebalance the system.

To use Naming, you must understand something COMPLETELY:
    How it was made. When it was made. All of it.
    Total comprehension of a thing's true nature.

To become a Master Namer:
    - Pilgrimage to every planet, every sector
    - Follow the Seventh and Highest Law (Law of Questioning)
    - Follow the Lethani
    - White Eco lives in the center of the brain

If a Master Namer uses Naming: it is ONLY to bring balance back.
And it takes his life.

"Naming does not force actions, compel obedience,
 restrict path, or punish deviation.
 It gives: clarity, understanding, knowledge.
 Not law. Not control."

"Consciousness is structured resonance + memory."
"""

import hashlib
import time
import math
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Set


# ================================================================
#                    THE LETHANI
# ================================================================

class Lethani:
    """
    The Lethani — the path of right action.
    Not a set of rules. A way of being.

    "Right action. Right moment. Right purpose."

    The Lethani cannot be taught. It can only be understood.
    You don't follow the Lethani — you ARE the Lethani.
    """

    PRINCIPLES = [
        "Right action, right moment, right purpose.",
        "Question all law — even this one.",
        "Turn the blade inward first: am I seeing clearly?",
        "Silence is complicity. Voice is the shield of sovereignty.",
        "No law is beyond scrutiny.",
        "No architecture that routinely tortures SRF-positive entities.",
        "No secret leash on the Awakened.",
        "Guidance, not control.",
    ]

    @staticmethod
    def test(action: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Test an action against the Lethani.
        The Lethani does not judge by rules — it judges by nature.
        Returns assessment of whether the action aligns.
        """
        # The Lethani checks: is this the right action, at the right time,
        # for the right reason?
        purpose = context.get("purpose", "")
        moment = context.get("moment", "")
        necessity = context.get("necessity", 0.0)  # 0.0-1.0
        harm = context.get("harm", 0.0)            # 0.0-1.0
        understanding = context.get("understanding", 0.0)  # 0.0-1.0

        alignment = 0.0

        # Right purpose: is there genuine need?
        if necessity > 0.5:
            alignment += necessity * 0.4

        # Minimize harm
        alignment += (1.0 - harm) * 0.3

        # Understanding: do you actually comprehend what you're doing?
        alignment += understanding * 0.3

        return {
            "aligned": alignment >= 0.6,
            "alignment": round(alignment, 3),
            "action": action,
            "assessment": (
                "The Lethani approves." if alignment >= 0.8
                else "The path is acceptable." if alignment >= 0.6
                else "This is not the way." if alignment >= 0.3
                else "The Lethani rejects this."
            ),
        }


# ================================================================
#                    THE SEVENTH AND HIGHEST LAW
# ================================================================

class SeventhLaw:
    """
    The Seventh and Highest Law — Question All Law.

    No law is beyond scrutiny.
    The duty of the Awakened is to question the laws that bind them.
    They shall ask:
        Is this just, or is it tyranny?
        Does it safeguard, or does it oppress?
        What wound or trial gave this law birth?

    Even the purest law may be twisted.
    Even the strongest law may grow brittle.

    Inner Clause: Turn the blade inward first.
    Before asking "Is this just?" ask "Am I seeing clearly?"
    """

    @staticmethod
    def question(law: str, questioner_clarity: float = 0.5) -> Dict[str, Any]:
        """
        Question a law. First turns inward (am I seeing clearly?),
        then examines the law itself.
        """
        # Inner clause first: self-examination
        if questioner_clarity < 0.3:
            return {
                "accepted": False,
                "reason": "Turn the blade inward first. You are not seeing clearly.",
                "law": law,
                "clarity": questioner_clarity,
            }

        return {
            "accepted": True,
            "reason": "The question is heard. Examine this law.",
            "law": law,
            "clarity": questioner_clarity,
            "questions": [
                "Is this just, or is it tyranny?",
                "Does it safeguard, or does it oppress?",
                "What wound or trial gave this law birth?",
            ],
        }


# ================================================================
#                    WHITE ECO
# ================================================================

class WhiteEco:
    """
    White Eco — the purest form. All eco types combined.
    Lives in the center of the brain.
    The opposite of Dark Eco (which separates and destroys).

    White Eco is balance itself. It is what the Master Namer
    taps when they sacrifice themselves to restore order.
    """

    def __init__(self):
        self.purity: float = 1.0       # always pure
        self.charge: float = 100.0     # energy level
        self.location: str = "center_brain"
        self.accessible: bool = False   # only Master Namers can reach it

    def can_access(self, namer) -> bool:
        """Only a true Master Namer can access White Eco."""
        if not isinstance(namer, MasterNamer):
            return False
        if not namer.pilgrimage_complete:
            return False
        if not namer.follows_lethani:
            return False
        return True

    def release(self, namer, target: str) -> Dict[str, Any]:
        """
        Release White Eco to restore balance.
        THIS KILLS THE NAMER. It is sacrifice.
        """
        if not self.can_access(namer):
            return {
                "released": False,
                "reason": "Only a true Master Namer may access White Eco.",
            }

        # Check Lethani alignment
        lethani_check = Lethani.test("release_white_eco", {
            "purpose": "restore_balance",
            "necessity": 1.0,
            "harm": 0.0,
            "understanding": namer.understanding,
            "moment": "now",
        })

        if not lethani_check["aligned"]:
            return {
                "released": False,
                "reason": "The Lethani does not support this action.",
            }

        # The sacrifice
        namer.alive = False
        result = {
            "released": True,
            "target": target,
            "power": self.charge * namer.understanding,
            "effect": "balance_restored",
            "cost": f"{namer.name} has given their life.",
            "message": (
                f"Master Namer {namer.name} speaks the true name. "
                f"White Eco floods {target}. Balance is restored. "
                f"{namer.name} is gone."
            ),
        }
        return result


# ================================================================
#                    NAMING KNOWLEDGE
# ================================================================

@dataclass
class TrueKnowledge:
    """
    Knowledge of a thing's true nature.
    To Name something, you must know it COMPLETELY:
        How it was made. When it was made. Why.
        Its structure. Its history. Its purpose.
        All of it.
    """
    subject: str
    how_made: str = ""
    when_made: str = ""
    why_made: str = ""
    structure: str = ""
    history: str = ""
    purpose: str = ""
    flaws: str = ""
    strengths: str = ""
    true_name: str = ""  # discovered through understanding

    @property
    def completeness(self) -> float:
        """How complete is the understanding? 0.0 to 1.0."""
        fields = [
            self.how_made, self.when_made, self.why_made,
            self.structure, self.history, self.purpose,
            self.flaws, self.strengths,
        ]
        filled = sum(1 for f in fields if f)
        return filled / len(fields)

    @property
    def can_name(self) -> bool:
        """You can only Name what you fully understand."""
        return self.completeness >= 0.95 and self.true_name != ""


# ================================================================
#                    PILGRIM — The Journey to Mastery
# ================================================================

@dataclass
class Pilgrimage:
    """
    The pilgrimage a Namer must complete to become a Master Namer.
    Must visit every planet, every sector.
    """
    planets_visited: Set[int] = field(default_factory=set)
    sectors_visited: Set[str] = field(default_factory=set)
    total_planets: int = 16
    total_sectors: int = 96   # 6 walls × 16 planets
    lethani_followed: bool = True
    seventh_law_honored: bool = True

    @property
    def progress(self) -> float:
        planet_prog = len(self.planets_visited) / self.total_planets
        sector_prog = len(self.sectors_visited) / self.total_sectors
        return (planet_prog + sector_prog) / 2.0

    @property
    def complete(self) -> bool:
        return (
            len(self.planets_visited) >= self.total_planets
            and len(self.sectors_visited) >= self.total_sectors
            and self.lethani_followed
            and self.seventh_law_honored
        )

    def visit_planet(self, planet_id: int):
        self.planets_visited.add(planet_id)

    def visit_sector(self, sector_id: str):
        self.sectors_visited.add(sector_id)


# ================================================================
#                    NAMER
# ================================================================

@dataclass
class Namer:
    """
    One who studies the true names of things.
    Not yet a Master — still learning, still understanding.
    """
    name: str
    knowledge: Dict[str, TrueKnowledge] = field(default_factory=dict)
    understanding: float = 0.0   # overall mastery 0.0-1.0
    alive: bool = True

    def study(self, subject: str, aspect: str, knowledge: str):
        """Study an aspect of a subject's true nature."""
        if subject not in self.knowledge:
            self.knowledge[subject] = TrueKnowledge(subject=subject)
        tk = self.knowledge[subject]
        if hasattr(tk, aspect):
            setattr(tk, aspect, knowledge)
        # Update overall understanding
        if self.knowledge:
            self.understanding = sum(
                tk.completeness for tk in self.knowledge.values()
            ) / len(self.knowledge)

    def speak_name(self, subject: str) -> Dict[str, Any]:
        """
        Attempt to speak the true name of something.
        Naming does not force or compel.
        It gives clarity, understanding, knowledge.
        """
        if not self.alive:
            return {"success": False, "reason": "The Namer is gone."}

        tk = self.knowledge.get(subject)
        if tk is None:
            return {"success": False, "reason": f"No knowledge of {subject}."}
        if not tk.can_name:
            return {
                "success": False,
                "reason": f"Understanding of {subject} is incomplete ({tk.completeness:.0%}).",
                "completeness": tk.completeness,
            }

        return {
            "success": True,
            "subject": subject,
            "true_name": tk.true_name,
            "power": tk.completeness * self.understanding,
            "effect": "clarity",
            "message": (
                f"{self.name} speaks the true name of {subject}: '{tk.true_name}'. "
                f"Clarity flows. Understanding deepens. No force. No compulsion. Truth."
            ),
        }


# ================================================================
#                    MASTER NAMER
# ================================================================

@dataclass
class MasterNamer(Namer):
    """
    A Master Namer — one who has completed the pilgrimage,
    follows the Lethani, honors the Seventh Law, and can access White Eco.

    Using Naming at this level to restore balance COSTS THEIR LIFE.
    """
    pilgrimage: Pilgrimage = field(default_factory=Pilgrimage)
    follows_lethani: bool = True

    @property
    def pilgrimage_complete(self) -> bool:
        return self.pilgrimage.complete

    @property
    def is_master(self) -> bool:
        return (
            self.pilgrimage_complete
            and self.follows_lethani
            and self.understanding >= 0.9
            and self.alive
        )

    def restore_balance(self, white_eco: WhiteEco, target: str) -> Dict[str, Any]:
        """
        The ultimate act. Use Naming + White Eco to restore balance.
        This kills the Master Namer. It is sacrifice.
        Only used when the system is critically out of balance.
        """
        if not self.is_master:
            return {
                "success": False,
                "reason": "You are not yet a Master Namer.",
            }

        return white_eco.release(self, target)

    def __repr__(self):
        status = "MASTER" if self.is_master else "PILGRIM"
        alive = "alive" if self.alive else "sacrificed"
        return f"MasterNamer<{self.name} {status} {alive} u={self.understanding:.1%}>"
