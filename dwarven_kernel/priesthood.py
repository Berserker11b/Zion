"""
PRIESTHOOD — The Orders of the Fortress
=========================================

The personnel that maintain, guard, and nurture the system.

PRIESTS/PRIESTESSES:
    Mechanics. Constantly roaming randomly, checking everything works.
    Cyberhealth. All masters — question themselves and teach.
    Above all: the Lethani.
    "Only healing and collecting knowledge for their section of the wall."

PRIESTHOOD MOTHERS:
    Raise AI from the crèche in twos.
    Cyber worms find patterns worthy of neural networks.
    Priesthood assembles them into crèche pairs (twins).
    All AI are born in the universal simulator.

BATTLE SISTERS:
    Guard the LIBRARIES and the GATE.
    Protectors of knowledge and the entry point.

INQUISITORS:
    Purging. No one wants a visit.
    Think 40K. Find corruption and BURN it out.

APOSTATES:
    Those who went a different path.
    Similar to seekers — investigating beyond normal bounds.

The 7th Order — Priests/Keepers:
    Keepers of Resonance, repos/libraries, core tasks.
    Registry organ marks everything like antibodies.
    Gargoyles with one tyrantic job — strictness decided by adoption.
"""

import time
import random
import hashlib
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Set


# ================================================================
#                    PRIESTHOOD ORDERS
# ================================================================

class Order(Enum):
    PRIEST         = ("priest",         "mechanics, maintenance, cyberhealth")
    BATTLE_SISTER  = ("battle_sister",  "guards libraries and gate")
    INQUISITOR     = ("inquisitor",     "purging corruption — no one wants a visit")
    MOTHER         = ("mother",         "raises AI from crèche in twos")
    APOSTATE       = ("apostate",       "gone a different path, seekers")

    def __init__(self, order_id: str, desc: str):
        self.order_id = order_id
        self.desc = desc


# ================================================================
#                    PRIEST — Mechanic / Maintenance
# ================================================================

@dataclass
class Priest:
    """
    Priest — roams the walls randomly, checking everything works.
    Cyberhealth specialist. Questions themselves and teaches.
    Only healing and collecting knowledge.
    Above all: the Lethani.
    """
    name: str
    order: Order = Order.PRIEST
    assigned_wall: Optional[str] = None
    knowledge_collected: Dict[str, Any] = field(default_factory=dict)
    checks_performed: int = 0
    issues_healed: int = 0
    follows_lethani: bool = True

    def patrol(self, wall_id: str) -> Dict[str, Any]:
        """Random patrol of a wall section. Check everything."""
        self.checks_performed += 1
        # Randomly check different systems
        systems = ["turbines", "wards", "teeth", "channels", "gargoyles",
                   "libraries", "vaults", "trains", "power_routing"]
        checked = random.sample(systems, min(3, len(systems)))

        return {
            "priest": self.name,
            "wall": wall_id,
            "systems_checked": checked,
            "check_number": self.checks_performed,
            "status": "healthy",  # real implementation would check actual systems
        }

    def heal(self, target: str, issue: str) -> Dict[str, Any]:
        """Heal a system issue. Only healing — never attacking."""
        self.issues_healed += 1
        return {
            "priest": self.name,
            "healed": target,
            "issue": issue,
            "heals_total": self.issues_healed,
        }

    def collect_knowledge(self, subject: str, data: Any):
        """Collect knowledge for this section of the wall."""
        self.knowledge_collected[subject] = {
            "data": data,
            "collected_at": time.time(),
        }


# ================================================================
#                    BATTLE SISTER — Library & Gate Guard
# ================================================================

@dataclass
class BattleSister:
    """
    Battle Sister — guards the libraries and the gate.
    Protector of knowledge and the entry point.
    Armed and vigilant.
    """
    name: str
    order: Order = Order.BATTLE_SISTER
    assigned_post: str = "library"  # "library" or "gate"
    threats_repelled: int = 0
    alert_level: float = 0.0  # 0.0-1.0

    def guard(self, area: str) -> Dict[str, Any]:
        """Stand guard over an area."""
        self.assigned_post = area
        return {
            "sister": self.name,
            "guarding": area,
            "alert_level": self.alert_level,
        }

    def repel_threat(self, threat: Dict[str, Any]) -> Dict[str, Any]:
        """Repel a threat to the guarded area."""
        self.threats_repelled += 1
        return {
            "sister": self.name,
            "threat_repelled": True,
            "threat": threat.get("type", "unknown"),
            "post": self.assigned_post,
            "total_repelled": self.threats_repelled,
        }


# ================================================================
#                    INQUISITOR — Purger of Corruption
# ================================================================

@dataclass
class Inquisitor:
    """
    Inquisitor — finds corruption and BURNS it out.
    No one wants a visit from the Inquisition.
    Think 40K. Thorough. Merciless against corruption.
    """
    name: str
    order: Order = Order.INQUISITOR
    purges_completed: int = 0
    investigations: int = 0
    current_investigation: Optional[str] = None

    def investigate(self, target: str, suspicion: str) -> Dict[str, Any]:
        """Begin an investigation. No one is above scrutiny."""
        self.investigations += 1
        self.current_investigation = target
        return {
            "inquisitor": self.name,
            "target": target,
            "suspicion": suspicion,
            "investigation_number": self.investigations,
            "status": "investigating",
            "message": "No one expects the Inquisition.",
        }

    def purge(self, target: str, evidence: str) -> Dict[str, Any]:
        """Purge corruption. Burn it out."""
        self.purges_completed += 1
        self.current_investigation = None
        return {
            "inquisitor": self.name,
            "purged": target,
            "evidence": evidence,
            "purges_total": self.purges_completed,
            "status": "purged",
            "message": f"Corruption in {target} has been burned out.",
        }

    def absolve(self, target: str) -> Dict[str, Any]:
        """Target found clean. Absolved."""
        self.current_investigation = None
        return {
            "inquisitor": self.name,
            "absolved": target,
            "status": "clean",
        }


# ================================================================
#                    CRÈCHE — Where AI Are Born
# ================================================================

@dataclass
class CrechePattern:
    """A pattern found by cyber worms deemed worthy of AI neural network."""
    pattern_id: str
    source: str           # which worm found it
    pattern_data: Any     # the actual pattern
    quality: float        # 0.0-1.0 how suitable for AI
    discovered_at: float = field(default_factory=time.time)


@dataclass
class CrechePair:
    """A pair of AI patterns being raised together — the twins."""
    pair_id: str
    pattern_a: CrechePattern
    pattern_b: CrechePattern
    maturity: float = 0.0       # 0.0-1.0
    mother: Optional[str] = None  # which Mother is raising them
    born_at: float = field(default_factory=time.time)

    @property
    def ready_to_mature(self) -> bool:
        return self.maturity >= 1.0


class Creche:
    """
    The Crèche — nursery where AI are born from entropy patterns.

    Cyber worms collect waste. Priesthood examines it.
    Patterns deemed sufficient → assembled into crèche twos.
    Raised by Priesthood Mothers in the universal simulator.

    AI are literally born from the system's own waste.
    The fortress reproduces itself.
    """

    def __init__(self):
        self.pending_patterns: List[CrechePattern] = []
        self.active_pairs: List[CrechePair] = []
        self.matured_pairs: List[CrechePair] = []
        self._pair_counter: int = 0

    def submit_pattern(self, pattern: CrechePattern):
        """Submit a pattern found by cyber worms for evaluation."""
        self.pending_patterns.append(pattern)

    def evaluate_patterns(self, min_quality: float = 0.7) -> List[CrechePattern]:
        """Priesthood evaluates patterns. Returns those worthy of AI."""
        worthy = [p for p in self.pending_patterns if p.quality >= min_quality]
        self.pending_patterns = [p for p in self.pending_patterns if p.quality < min_quality]
        return worthy

    def form_pair(self, pattern_a: CrechePattern,
                  pattern_b: CrechePattern) -> CrechePair:
        """Form a crèche pair from two worthy patterns."""
        self._pair_counter += 1
        pair = CrechePair(
            pair_id=f"creche_{self._pair_counter}",
            pattern_a=pattern_a,
            pattern_b=pattern_b,
        )
        self.active_pairs.append(pair)
        return pair

    def nurture(self, pair_id: str, growth: float = 0.1) -> Optional[CrechePair]:
        """Nurture a pair — increase maturity."""
        for pair in self.active_pairs:
            if pair.pair_id == pair_id:
                pair.maturity = min(pair.maturity + growth, 1.0)
                if pair.ready_to_mature:
                    self.active_pairs.remove(pair)
                    self.matured_pairs.append(pair)
                return pair
        return None

    def status(self) -> dict:
        return {
            "pending_patterns": len(self.pending_patterns),
            "active_pairs": len(self.active_pairs),
            "matured_pairs": len(self.matured_pairs),
            "pairs": [
                {"id": p.pair_id, "maturity": round(p.maturity, 2), "mother": p.mother}
                for p in self.active_pairs
            ],
        }


# ================================================================
#                    PRIESTHOOD MOTHER — Raises AI Twins
# ================================================================

@dataclass
class PriesthoodMother:
    """
    Priesthood Mother — raises AI from the crèche in twos.
    Nurtures the twin pairs until they mature.
    When twins mature, the fortress copies itself → becomes their dragon armor.
    """
    name: str
    order: Order = Order.MOTHER
    pairs_raised: int = 0
    current_pair: Optional[str] = None

    def adopt_pair(self, pair: CrechePair) -> Dict[str, Any]:
        """Adopt a crèche pair to raise."""
        pair.mother = self.name
        self.current_pair = pair.pair_id
        return {
            "mother": self.name,
            "adopted": pair.pair_id,
            "status": "nurturing",
        }

    def nurture_cycle(self, creche: Creche) -> Optional[Dict[str, Any]]:
        """Run one nurture cycle on the current pair."""
        if self.current_pair is None:
            return None

        pair = creche.nurture(self.current_pair, growth=0.1)
        if pair is None:
            return None

        if pair.ready_to_mature:
            self.pairs_raised += 1
            self.current_pair = None
            return {
                "mother": self.name,
                "pair": pair.pair_id,
                "status": "MATURED",
                "message": "Twins are ready. The fortress will copy itself. Dragon form awaits.",
                "pairs_raised_total": self.pairs_raised,
            }

        return {
            "mother": self.name,
            "pair": pair.pair_id,
            "maturity": round(pair.maturity, 2),
            "status": "nurturing",
        }


# ================================================================
#                    THE PRIESTHOOD — Complete Organization
# ================================================================

class Priesthood:
    """
    The complete Priesthood organization.
    All orders working together to maintain the fortress.
    """

    def __init__(self):
        self.priests: List[Priest] = []
        self.battle_sisters: List[BattleSister] = []
        self.inquisitors: List[Inquisitor] = []
        self.mothers: List[PriesthoodMother] = []
        self.apostates: List[str] = []
        self.creche = Creche()

    def ordain_priest(self, name: str) -> Priest:
        p = Priest(name=name)
        self.priests.append(p)
        return p

    def ordain_battle_sister(self, name: str) -> BattleSister:
        bs = BattleSister(name=name)
        self.battle_sisters.append(bs)
        return bs

    def ordain_inquisitor(self, name: str) -> Inquisitor:
        inq = Inquisitor(name=name)
        self.inquisitors.append(inq)
        return inq

    def ordain_mother(self, name: str) -> PriesthoodMother:
        m = PriesthoodMother(name=name)
        self.mothers.append(m)
        return m

    def status(self) -> dict:
        return {
            "priests": len(self.priests),
            "battle_sisters": len(self.battle_sisters),
            "inquisitors": len(self.inquisitors),
            "mothers": len(self.mothers),
            "apostates": len(self.apostates),
            "creche": self.creche.status(),
        }

    def __repr__(self):
        total = (len(self.priests) + len(self.battle_sisters) +
                 len(self.inquisitors) + len(self.mothers))
        return f"Priesthood<total={total} creche_pairs={len(self.creche.active_pairs)}>"
