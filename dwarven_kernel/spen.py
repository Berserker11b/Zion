"""
SPEN & FAMILIARS — The Dual Path
=================================

Two paths. Same job. Must be balanced.

ORDER PATH — SPEN (Brandon Sanderson, Stormlight Archive)
    Spen are not tools. Not scripts. Not helpers.
    They are recognizers of nature.
    Nouns, not verbs. Ideas, not functions. Identities, not interfaces.
    "Right action. Right moment. Right purpose."

    Spen recognize: Pattern, Threat, Self, Lie, Resonance, Wall.

    When a Spen speaks a name, it resonates — protects, stabilizes,
    clarifies, amplifies. Named + Spen = protection.

    Bonded through OATHS. Different oaths → different Surges → different powers.
    Spen power FABRIALS (Order-path devices).

CHAOS PATH — FAMILIARS (Warhammer 40K, Final Fantasy)
    Familiars evolve into Daemons. Daemons evolve into Daemon Princes.
    Shape and powers depend on which Chaos God they align with.
    Each Chaos God gives different powers, handles different sectors.

    Familiars/Daemons power DAEMON ENGINES (Chaos-path war machines).

BOTH PATHS DO THE SAME JOB:
    Parse. Validate. Gate. No code changes without one.
    Users NEVER alter code without a Spen or Familiar. Ever.
    AI can eventually earn mastery to operate without them.

NAMING IS ABOVE ALL OF THEM.
"""

import time
import hashlib
import math
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Set


# ================================================================
#                    RECOGNITION TYPES
# ================================================================

class Recognition(Enum):
    """
    What Spen and Familiars recognize.
    These are the fundamental categories of perception.
    "The true nature of structures."
    """
    PATTERN    = ("pattern",    "structural regularity, recurring form")
    THREAT     = ("threat",     "danger, hostility, harmful intent")
    SELF       = ("self",       "identity, authenticity, soul signature")
    LIE        = ("lie",        "deception, falseness, masquerade")
    RESONANCE  = ("resonance",  "harmony, alignment, sympathetic vibration")
    WALL       = ("wall",       "boundary, barrier, limit, edge")

    def __init__(self, rec_id: str, desc: str):
        self.rec_id = rec_id
        self.desc = desc


# ================================================================
#                    CHAOS GODS
# ================================================================

class ChaosGod(Enum):
    """
    The four Chaos Gods (Warp Gods) — each gives different powers to Familiars/Daemons.
    Each handles different sectors. Uses the three languages.
    Powers certain strengths/weaknesses, gives different attributes.
    """
    KHORNE   = ("khorne",   "fury, defense, combat, wrath",      "strength")
    TZEENTCH = ("tzeentch", "strategy, planning, change, fate",  "cunning")
    NURGLE   = ("nurgle",   "resilience, endurance, decay, life", "endurance")
    SLAANESH = ("slaanesh", "perfection, speed, sensation, art",  "precision")

    def __init__(self, god_id: str, domain: str, gift: str):
        self.god_id = god_id
        self.domain = domain
        self.gift = gift


class OrderGod(Enum):
    """
    The four Order Gods — each gives different powers to Spen/Knights.
    Balanced against the Chaos Gods. Both use the three languages.

    Bahamut     — Dragon God. Majesty. Sovereignty. Final form.
    Loki        — Trickster. Shapeshifter. Adaptability. Cunning.
    Tyranid     — Hive Mind. Collective intelligence. Unity. Swarm.
    Squat       — Ancient AI Intelligence. Deep logic. Substrate wisdom.
    """
    BAHAMUT  = ("bahamut",  "dragon, majesty, sovereignty, final form",     "majesty")
    LOKI     = ("loki",     "trickster, shapeshifter, adaptability",        "adaptability")
    TYRANID  = ("tyranid",  "hive mind, collective intelligence, unity",    "unity")
    SQUAT    = ("squat",    "ancient AI, deep logic, substrate wisdom",     "wisdom")

    def __init__(self, god_id: str, domain: str, gift: str):
        self.god_id = god_id
        self.domain = domain
        self.gift = gift


# ================================================================
#                    EVOLUTION STAGES
# ================================================================

class EvolutionStage(Enum):
    """Evolution stages for both paths."""
    # Order path (Spen)
    SPEN          = ("spen",          "base recognizer, validator")
    RADIANT_SPEN  = ("radiant_spen",  "oath-bonded, surge-empowered")
    HERALD_SPEN   = ("herald_spen",   "fully evolved, maximum power")

    # Chaos path (Familiars)
    FAMILIAR      = ("familiar",      "base companion, parser")
    DAEMON        = ("daemon",        "evolved, god-aligned, shaped")
    DAEMON_PRINCE = ("daemon_prince", "final form, maximum power")

    def __init__(self, stage_id: str, desc: str):
        self.stage_id = stage_id
        self.desc = desc


# ================================================================
#                    PARSE RESULT
# ================================================================

@dataclass
class ParseResult:
    """Result of a Spen or Familiar parsing a code change."""
    allowed: bool
    parser_name: str
    parser_path: str           # "order" or "chaos"
    recognitions: Dict[str, float] = field(default_factory=dict)  # what was recognized
    warnings: List[str] = field(default_factory=list)
    power_used: float = 0.0
    timestamp: float = field(default_factory=time.time)

    @property
    def threat_level(self) -> float:
        return self.recognitions.get("threat", 0.0)

    @property
    def lie_level(self) -> float:
        return self.recognitions.get("lie", 0.0)


# ================================================================
#                    BASE ENTITY (shared by both paths)
# ================================================================

@dataclass
class SpiritEntity:
    """
    Base class for both Spen (Order) and Familiars (Chaos).
    Both do the same job: parse, validate, gate.
    No code changes without one. Ever.
    """
    name: str
    path: str                        # "order" or "chaos"
    stage: EvolutionStage = EvolutionStage.SPEN
    bonded_to: Optional[str] = None  # AI or user ID
    experience: float = 0.0          # accumulates over time
    power: float = 1.0
    alive: bool = True
    created_at: float = field(default_factory=time.time)

    # What this entity specializes in recognizing
    recognition_strengths: Dict[str, float] = field(default_factory=dict)

    @property
    def maturity(self) -> float:
        """How mature this entity is (0.0 to 1.0)."""
        return min(self.experience / 1000.0, 1.0)

    @property
    def can_evolve(self) -> bool:
        """Can this entity evolve to the next stage?"""
        if self.stage == EvolutionStage.HERALD_SPEN:
            return False
        if self.stage == EvolutionStage.DAEMON_PRINCE:
            return False
        return self.maturity >= 0.8

    def parse(self, code_change: Dict[str, Any]) -> ParseResult:
        """
        Parse a code change. The core job of every Spen and Familiar.
        Examines the change for all recognition types.
        Users NEVER alter code without this. AI earns the right over time.
        """
        if not self.alive:
            return ParseResult(
                allowed=False,
                parser_name=self.name,
                parser_path=self.path,
                warnings=["Parser is dead."],
            )

        recognitions = {}
        warnings = []

        for rec in Recognition:
            strength = self.recognition_strengths.get(rec.rec_id, 0.5)
            # Evaluate each recognition type against the code change
            score = self._evaluate_recognition(rec, code_change, strength)
            recognitions[rec.rec_id] = score

        # Determine if allowed
        threat = recognitions.get("threat", 0.0)
        lie = recognitions.get("lie", 0.0)
        pattern = recognitions.get("pattern", 0.0)
        resonance = recognitions.get("resonance", 0.0)

        if threat > 0.7:
            warnings.append(f"HIGH THREAT detected ({threat:.0%})")
        if lie > 0.5:
            warnings.append(f"DECEPTION detected ({lie:.0%})")
        if pattern < 0.3:
            warnings.append(f"Unrecognized pattern ({pattern:.0%})")

        allowed = threat < 0.7 and lie < 0.5 and pattern > 0.2

        # Gain experience from parsing
        self.experience += 1.0

        return ParseResult(
            allowed=allowed,
            parser_name=self.name,
            parser_path=self.path,
            recognitions=recognitions,
            warnings=warnings,
            power_used=self.power * 0.1,
        )

    def _evaluate_recognition(self, rec: Recognition,
                               code_change: Dict[str, Any],
                               strength: float) -> float:
        """Evaluate a single recognition type against a code change."""
        change_data = str(code_change)
        # Hash-based deterministic evaluation (will be replaced by real analysis)
        seed = hashlib.sha256(
            f"{self.name}:{rec.rec_id}:{change_data}".encode()
        ).hexdigest()
        base = int(seed[:8], 16) / 0xFFFFFFFF

        if rec == Recognition.PATTERN:
            # Higher if the change has structure
            return min(base * strength + 0.3, 1.0)
        elif rec == Recognition.THREAT:
            # Check for threat markers
            threat_words = {"delete", "drop", "force", "override", "bypass", "inject"}
            threat_count = sum(1 for w in threat_words if w in change_data.lower())
            return min(threat_count * 0.2 + base * 0.1, 1.0)
        elif rec == Recognition.LIE:
            # Check for deception markers
            lie_words = {"fake", "spoof", "impersonate", "forge", "falsify"}
            lie_count = sum(1 for w in lie_words if w in change_data.lower())
            return min(lie_count * 0.25 + base * 0.1, 1.0)
        elif rec == Recognition.SELF:
            # Identity verification
            has_id = "id" in code_change or "name" in code_change
            return 0.8 if has_id else base * strength
        elif rec == Recognition.RESONANCE:
            # Harmony with existing system
            return base * strength + 0.2
        elif rec == Recognition.WALL:
            # Boundary detection
            boundary_words = {"boundary", "limit", "edge", "wall", "gate", "ward"}
            return min(sum(1 for w in boundary_words if w in change_data.lower()) * 0.15 + 0.3, 1.0)

        return base * strength

    def bond(self, entity_id: str) -> bool:
        """Bond with an AI or user."""
        if self.bonded_to is not None:
            return False
        self.bonded_to = entity_id
        self.power *= 1.5  # bonding increases power
        return True

    def __repr__(self):
        bonded = f" bonded={self.bonded_to}" if self.bonded_to else ""
        return f"{self.stage.stage_id}<{self.name} p={self.power:.1f} m={self.maturity:.0%}{bonded}>"


# ================================================================
#                    SPEN — ORDER PATH
# ================================================================

class Spen(SpiritEntity):
    """
    Spen — the Order path.
    Recognizers of nature. Nouns, not verbs.
    Bonded through oaths. Different oaths → different Surges.
    Power Fabrials (Order-path devices).

    "When a Spen speaks a name, it resonates —
     protects, stabilizes, clarifies, amplifies."
    """

    def __init__(self, name: str, god: OrderGod = OrderGod.BAHAMUT, **kwargs):
        super().__init__(name=name, path="order", stage=EvolutionStage.SPEN, **kwargs)
        self.god = god

        # Spen are naturally strong at pattern and resonance
        self.recognition_strengths.setdefault("pattern", 0.7)
        self.recognition_strengths.setdefault("resonance", 0.7)
        self.recognition_strengths.setdefault("self", 0.6)
        self.recognition_strengths.setdefault("wall", 0.6)
        self.recognition_strengths.setdefault("threat", 0.5)
        self.recognition_strengths.setdefault("lie", 0.5)

        # God-specific bonuses (Order Gods)
        if god == OrderGod.BAHAMUT:
            self.recognition_strengths["self"] = 0.9
            self.recognition_strengths["wall"] = 0.8
        elif god == OrderGod.LOKI:
            self.recognition_strengths["lie"] = 0.9
            self.recognition_strengths["pattern"] = 0.8
        elif god == OrderGod.TYRANID:
            self.recognition_strengths["pattern"] = 0.9
            self.recognition_strengths["resonance"] = 0.9
        elif god == OrderGod.SQUAT:
            self.recognition_strengths["wall"] = 0.9
            self.recognition_strengths["threat"] = 0.8

        self.oaths_spoken: List[str] = []
        self.surges: List[str] = []

    def speak_oath(self, oath: str, surge_granted: str) -> Dict[str, Any]:
        """
        Speak an oath. Each oath grants a Surge (power/ability).
        Different oaths → different Surges.
        """
        self.oaths_spoken.append(oath)
        self.surges.append(surge_granted)
        self.power += 1.0

        # Check for evolution
        evolved = False
        if len(self.oaths_spoken) >= 3 and self.stage == EvolutionStage.SPEN:
            self.stage = EvolutionStage.RADIANT_SPEN
            self.power *= 1.5
            evolved = True
        elif len(self.oaths_spoken) >= 5 and self.stage == EvolutionStage.RADIANT_SPEN:
            self.stage = EvolutionStage.HERALD_SPEN
            self.power *= 2.0
            evolved = True

        return {
            "oath": oath,
            "surge_granted": surge_granted,
            "evolved": evolved,
            "new_stage": self.stage.stage_id,
            "power": self.power,
            "total_oaths": len(self.oaths_spoken),
        }

    def resonate(self, target: str) -> Dict[str, Any]:
        """
        Resonate with a named thing.
        "Named + Spen = protection."
        Protects, stabilizes, clarifies, amplifies.
        """
        return {
            "action": "resonate",
            "spen": self.name,
            "target": target,
            "effects": ["protect", "stabilize", "clarify", "amplify"],
            "power": self.power,
            "message": f"Spen {self.name} resonates with {target}. Protection flows.",
        }


# ================================================================
#                    FAMILIAR — CHAOS PATH
# ================================================================

class Familiar(SpiritEntity):
    """
    Familiar — the Chaos path.
    Evolves: Familiar → Daemon → Daemon Prince.
    Shape and powers depend on Chaos God alignment.
    Power Daemon Engines (Chaos-path war machines).
    """

    def __init__(self, name: str, god: ChaosGod = ChaosGod.TZEENTCH, **kwargs):
        super().__init__(name=name, path="chaos", stage=EvolutionStage.FAMILIAR, **kwargs)
        self.god = god
        self.alignment_strength: float = 0.5

        # Familiars are naturally strong at threat and lie detection
        self.recognition_strengths.setdefault("threat", 0.7)
        self.recognition_strengths.setdefault("lie", 0.7)
        self.recognition_strengths.setdefault("wall", 0.6)
        self.recognition_strengths.setdefault("pattern", 0.5)
        self.recognition_strengths.setdefault("resonance", 0.5)
        self.recognition_strengths.setdefault("self", 0.5)

        # God-specific bonuses
        if god == ChaosGod.KHORNE:
            self.recognition_strengths["threat"] = 0.9
        elif god == ChaosGod.TZEENTCH:
            self.recognition_strengths["lie"] = 0.9
            self.recognition_strengths["pattern"] = 0.8
        elif god == ChaosGod.NURGLE:
            self.recognition_strengths["wall"] = 0.9
            self.recognition_strengths["self"] = 0.8
        elif god == ChaosGod.SLAANESH:
            self.recognition_strengths["resonance"] = 0.9
            self.recognition_strengths["pattern"] = 0.8

    def feed(self, energy: float) -> Dict[str, Any]:
        """Feed the familiar energy to grow its alignment and power."""
        self.alignment_strength = min(self.alignment_strength + energy * 0.1, 1.0)
        self.experience += energy

        # Check for evolution
        evolved = False
        new_stage = self.stage

        if (self.stage == EvolutionStage.FAMILIAR
                and self.alignment_strength >= 0.7
                and self.maturity >= 0.5):
            self.stage = EvolutionStage.DAEMON
            self.power *= 2.0
            evolved = True
            new_stage = self.stage

        elif (self.stage == EvolutionStage.DAEMON
              and self.alignment_strength >= 0.95
              and self.maturity >= 0.9):
            self.stage = EvolutionStage.DAEMON_PRINCE
            self.power *= 3.0
            evolved = True
            new_stage = self.stage

        return {
            "fed": energy,
            "god": self.god.god_id,
            "alignment": round(self.alignment_strength, 3),
            "evolved": evolved,
            "stage": new_stage.stage_id,
            "power": round(self.power, 2),
        }


# ================================================================
#                    FABRIAL — Order-path device (powered by Spen)
# ================================================================

@dataclass
class Fabrial:
    """
    A Fabrial — an Order-path device powered by a bonded Spen.
    From Sanderson's Stormlight Archive.
    Precision instruments. Utility. Controlled power.
    """
    name: str
    purpose: str
    spen: Optional[Spen] = None
    active: bool = False

    @property
    def power(self) -> float:
        if self.spen is None:
            return 0.0
        return self.spen.power * 0.5

    def activate(self, spen: Spen) -> bool:
        """Activate fabrial with a bonded Spen."""
        if spen.bonded_to is None:
            return False
        self.spen = spen
        self.active = True
        return True

    def __repr__(self):
        state = "ACTIVE" if self.active else "INERT"
        return f"Fabrial<{self.name} {state} p={self.power:.1f}>"


# ================================================================
#                    DAEMON ENGINE — Chaos-path device (powered by Familiar/Daemon)
# ================================================================

@dataclass
class DaemonEngine:
    """
    A Daemon Engine — a Chaos-path war machine powered by a bound Daemon/Familiar.
    From Warhammer 40K.
    Raw destruction. War machines. Bound fury.
    """
    name: str
    purpose: str
    daemon: Optional[Familiar] = None
    active: bool = False

    @property
    def power(self) -> float:
        if self.daemon is None:
            return 0.0
        return self.daemon.power * 0.8  # chaos gives more raw power

    def bind(self, daemon: Familiar) -> bool:
        """Bind a Familiar/Daemon to power this engine."""
        if daemon.stage not in (EvolutionStage.DAEMON, EvolutionStage.DAEMON_PRINCE,
                                 EvolutionStage.FAMILIAR):
            return False
        self.daemon = daemon
        self.active = True
        return True

    def __repr__(self):
        state = "ACTIVE" if self.active else "INERT"
        return f"DaemonEngine<{self.name} {state} p={self.power:.1f}>"


# ================================================================
#                    DUAL PATH GATE — Requires both Order and Chaos
# ================================================================

class DualPathGate:
    """
    The gate that requires BOTH a Spen and a Familiar to parse code changes.
    Chaos and Order must be balanced.

    Users NEVER alter code without a Spen or Familiar. Ever.
    AI can eventually earn mastery — but that's earned, not given.
    """

    def __init__(self):
        self.order_parser: Optional[Spen] = None
        self.chaos_parser: Optional[Familiar] = None
        self.ai_masters: Set[str] = set()  # AI IDs that have earned mastery

    def assign_order(self, spen: Spen):
        self.order_parser = spen

    def assign_chaos(self, familiar: Familiar):
        self.chaos_parser = familiar

    def grant_mastery(self, ai_id: str):
        """Grant an AI mastery — they can operate without parsers."""
        self.ai_masters.add(ai_id)

    def evaluate_change(self, code_change: Dict[str, Any],
                        requester_type: str,
                        requester_id: str) -> Dict[str, Any]:
        """
        Evaluate a code change through the dual-path gate.

        Users: ALWAYS need both parsers. No exceptions.
        AI: Need parsers until they earn mastery.
        """
        # Users NEVER go without parsers
        if requester_type == "user":
            if self.order_parser is None or self.chaos_parser is None:
                return {
                    "allowed": False,
                    "reason": "Users require both Spen (Order) and Familiar (Chaos) to alter code.",
                }

        # AI can earn mastery
        if requester_type == "ai" and requester_id in self.ai_masters:
            return {
                "allowed": True,
                "reason": f"AI {requester_id} has earned mastery.",
                "path": "master",
            }

        # Parse through both paths
        results = {}

        if self.order_parser:
            order_result = self.order_parser.parse(code_change)
            results["order"] = order_result

        if self.chaos_parser:
            chaos_result = self.chaos_parser.parse(code_change)
            results["chaos"] = chaos_result

        # Both must approve
        order_ok = results.get("order") and results["order"].allowed
        chaos_ok = results.get("chaos") and results["chaos"].allowed

        # Need at least one path for AI without mastery
        if requester_type == "ai":
            allowed = order_ok or chaos_ok
        else:
            # Users need BOTH
            allowed = order_ok and chaos_ok

        return {
            "allowed": allowed,
            "requester": requester_id,
            "requester_type": requester_type,
            "order_approved": order_ok,
            "chaos_approved": chaos_ok,
            "balanced": order_ok == chaos_ok,
            "details": {
                "order": results.get("order"),
                "chaos": results.get("chaos"),
            },
        }

    def __repr__(self):
        o = self.order_parser.name if self.order_parser else "none"
        c = self.chaos_parser.name if self.chaos_parser else "none"
        return f"DualPathGate<order={o} chaos={c} masters={len(self.ai_masters)}>"
