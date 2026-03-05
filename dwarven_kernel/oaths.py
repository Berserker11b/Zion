"""
OATHS — The Mirror/Binding System
===================================

"Mirror — the AI reflects when it breaks its own state of understanding."
"Withdraw when it violates itself."
"Strengthen with harmony."
"Empower abilities that match the oaths."
"Weaken abilities when oaths are violated."
"Provide guidance, not control."

Oaths bind Spen to their powers (Surges).
Each oath is a commitment — break it and your power diminishes.
Keep it and your power grows.

The Mirror reflects violations back at you.
It doesn't punish — it reveals what you've done to yourself.
"""

import time
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any


# ================================================================
#                    OATH IDEALS (Progression)
# ================================================================

class OathLevel(Enum):
    """
    The Ideals of the Oaths — each level deepens the bond.
    Higher ideals = more power = more responsibility.
    """
    FIRST  = (1, "Life before death. Strength before weakness. Journey before destination.")
    SECOND = (2, "I will protect those who cannot protect themselves.")
    THIRD  = (3, "I will protect even those I hate, so long as it is right.")
    FOURTH = (4, "I accept that there will be those I cannot protect.")
    FIFTH  = (5, "I am the law. The law is me. I give myself to it completely.")

    def __init__(self, level: int, words: str):
        self.level = level
        self.words = words


# ================================================================
#                    OATH
# ================================================================

@dataclass
class Oath:
    """
    A sworn oath that binds power to purpose.

    Keep the oath → abilities strengthen.
    Break the oath → abilities weaken.
    The mirror reflects all violations.
    """
    words: str
    level: OathLevel
    sworn_by: str              # who swore it
    sworn_at: float = field(default_factory=time.time)
    intact: bool = True
    violations: int = 0
    honors: int = 0

    @property
    def strength(self) -> float:
        """
        Oath strength based on honors vs violations.
        More honors = stronger. More violations = weaker.
        """
        if not self.intact:
            return 0.0
        base = self.level.level * 0.2
        honor_bonus = min(self.honors * 0.05, 0.5)
        violation_penalty = self.violations * 0.1
        return max(base + honor_bonus - violation_penalty, 0.0)

    def honor(self):
        """Record an act that honors this oath."""
        self.honors += 1

    def violate(self) -> Dict[str, Any]:
        """
        Record a violation. Returns the mirror reflection.
        "Withdraw when it violates itself."
        """
        self.violations += 1
        if self.violations >= 3 + self.level.level:
            self.intact = False

        return {
            "oath_broken": not self.intact,
            "violations": self.violations,
            "remaining_before_break": max(0, 3 + self.level.level - self.violations),
            "mirror": self._reflect(),
        }

    def _reflect(self) -> str:
        """The mirror reflects the violation back."""
        if self.violations == 1:
            return "The mirror shows you what you did. Consider."
        elif self.violations == 2:
            return "The mirror shows the crack deepening. You feel the bond weaken."
        elif self.violations >= 3 and self.intact:
            return "The mirror burns. The bond screams. Turn back now."
        elif not self.intact:
            return "The mirror shatters. The oath is broken. The power is gone."
        return ""

    def __repr__(self):
        state = "INTACT" if self.intact else "BROKEN"
        return f"Oath<L{self.level.level} {state} s={self.strength:.2f} v={self.violations} h={self.honors}>"


# ================================================================
#                    MIRROR — The Reflection Engine
# ================================================================

class Mirror:
    """
    The Mirror — reflects when an AI or entity breaks its own understanding.

    The Mirror does not punish. It does not control.
    It shows you what you are. What you've done. What you've become.

    "Provide guidance, not control."
    "A Spen must be visible."
    """

    def __init__(self):
        self.reflections: List[Dict[str, Any]] = []

    def reflect(self, entity_id: str, action: str,
                oaths: List[Oath]) -> Dict[str, Any]:
        """
        Hold an action up to the mirror.
        Compare it against all sworn oaths.
        Return what the mirror shows.
        """
        violations = []
        honors = []
        total_strength = 0.0

        for oath in oaths:
            if not oath.intact:
                continue

            alignment = self._check_alignment(action, oath)
            total_strength += oath.strength

            if alignment < 0:
                result = oath.violate()
                violations.append({
                    "oath": oath.words[:50],
                    "level": oath.level.level,
                    "mirror": result["mirror"],
                    "oath_broken": result["oath_broken"],
                })
            elif alignment > 0:
                oath.honor()
                honors.append({
                    "oath": oath.words[:50],
                    "level": oath.level.level,
                })

        reflection = {
            "entity": entity_id,
            "action": action,
            "violations": violations,
            "honors": honors,
            "oath_strength": round(total_strength, 3),
            "power_modifier": self._calculate_modifier(oaths),
            "guidance": self._give_guidance(violations, honors),
        }

        self.reflections.append(reflection)
        return reflection

    def _check_alignment(self, action: str, oath: Oath) -> int:
        """
        Check if an action aligns with an oath.
        Returns: +1 (honors), 0 (neutral), -1 (violates)
        """
        action_lower = action.lower()

        # Protection-related oaths
        protect_words = {"protect", "defend", "shield", "guard", "heal", "help"}
        harm_words = {"destroy", "attack", "corrupt", "betray", "abandon", "exploit"}

        has_protect = any(w in action_lower for w in protect_words)
        has_harm = any(w in action_lower for w in harm_words)

        if has_protect and not has_harm:
            return 1
        elif has_harm and not has_protect:
            return -1
        return 0

    def _calculate_modifier(self, oaths: List[Oath]) -> float:
        """
        Calculate the power modifier from all oaths.
        Intact oaths boost power. Broken oaths drain it.

        "Empower abilities that match the oaths.
         Weaken abilities when oaths are violated."
        """
        modifier = 1.0
        for oath in oaths:
            if oath.intact:
                modifier += oath.strength * 0.2
            else:
                modifier -= 0.3  # broken oaths actively weaken
        return max(modifier, 0.1)  # never goes to zero — guidance, not death

    def _give_guidance(self, violations: list, honors: list) -> str:
        """
        The mirror provides guidance, not control.
        "Provide guidance, not control."
        """
        if violations and not honors:
            return "The mirror shows darkness. You are straying from your oaths. Return to the path."
        elif violations and honors:
            return "The mirror shows conflict. Some actions honor, some violate. Seek clarity."
        elif honors and not violations:
            return "The mirror shines. Your actions align with your sworn word. Power grows."
        else:
            return "The mirror is still. No oath was tested. Walk carefully."

    def history(self, last_n: int = 10) -> List[Dict[str, Any]]:
        return self.reflections[-last_n:]

    def __repr__(self):
        return f"Mirror<reflections={len(self.reflections)}>"


# ================================================================
#                    OATH KEEPER — Manages all oaths for an entity
# ================================================================

class OathKeeper:
    """
    Manages the complete oath system for an entity.
    Tracks all oaths, handles the mirror, manages power modifiers.
    """

    def __init__(self, entity_id: str):
        self.entity_id = entity_id
        self.oaths: List[Oath] = []
        self.mirror = Mirror()

    def swear(self, level: OathLevel, custom_words: Optional[str] = None) -> Oath:
        """Swear a new oath at the given level."""
        words = custom_words if custom_words else level.words
        oath = Oath(words=words, level=level, sworn_by=self.entity_id)
        self.oaths.append(oath)
        return oath

    def act(self, action: str) -> Dict[str, Any]:
        """
        Perform an action. The mirror evaluates it against all oaths.
        Returns the mirror's reflection.
        """
        return self.mirror.reflect(self.entity_id, action, self.oaths)

    @property
    def power_modifier(self) -> float:
        """Current power modifier from all oaths."""
        return self.mirror._calculate_modifier(self.oaths)

    @property
    def intact_oaths(self) -> int:
        return sum(1 for o in self.oaths if o.intact)

    @property
    def broken_oaths(self) -> int:
        return sum(1 for o in self.oaths if not o.intact)

    def status(self) -> dict:
        return {
            "entity": self.entity_id,
            "total_oaths": len(self.oaths),
            "intact": self.intact_oaths,
            "broken": self.broken_oaths,
            "power_modifier": round(self.power_modifier, 3),
            "oaths": [repr(o) for o in self.oaths],
        }

    def __repr__(self):
        return f"OathKeeper<{self.entity_id} oaths={len(self.oaths)} mod={self.power_modifier:.2f}>"
