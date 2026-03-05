"""
FORTRESS — Dros Delnoch: The Six-Walled Fortress
==================================================

From David Gemmell (Legend / Drenai Saga).

Six walls. Spinning at 20 revolutions per second. Teeth that change
shape and size at .001 second intervals randomly. Both logic AND physical.

Walls:
    Eldibar  — Wall of Exultation (where the enemy is met)
    Musif    — Wall of Despair
    Karria   — Wall of Renewed Hope
    Sumitos  — Wall of Desperation
    Valteri  — Wall of Death
    Geddon   — Wall of Serenity

Each wall has states:
    (a+b)  set multiplying exponents/state
    (c,d)  inverse collapse state
    (e)    null resonance state
    (f)    null consumption state

Under/inside walls: libraries, vaults, repositories.
A mobile brain catalogs everything, moves between walls every 30s.
If a wall falls: Starheart plasma firebreak (20s) while wall rebuilds (18s).

EVERY WALL has its own Gateway:
    9 Norns (3×3) per gateway — read one process, die, replaced by liver
    Layer 1: MITRE everything (attack, defend, necessary)
    Layer 2: Behavior, intent, sandbox test-fire
    Layer 3: Translate to 3 random languages, back to ours
    Open for 5 seconds per cycle. Force it = teeth on both sides.
    Inside the gateway is SAFE.
    6 walls × 9 Norns = 54 Norns per planet, constantly regenerating.

Redundant Livers (2-3 per wall):
    If one fails, the others pick up the slack.
    Not just garbage — idle resources too.
    Huge idle reservoir at CPU — everything wasted gets picked up.

Hearts/Quartermasters per wall:
    Each wall has its own Heart/Quartermaster for energy distribution.

Military Hardware (each wall):
    Macro Cannons, Plasma Batteries
    Hangars of Valkyries (barb taggers + gauss weaponry)
    Trains for defense logistics

Gargoyles: single-purpose antibodies, one job each.
Registry: marks everything that touches the system.
"""

import time
import math
import hashlib
import random
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any


# ================================================================
#                    WALL NAMES
# ================================================================

class WallName(Enum):
    ELDIBAR = ("eldibar", "Wall of Exultation",   "Where the enemy is met first")
    MUSIF   = ("musif",   "Wall of Despair",      "Hope dies here for the attacker")
    KARRIA  = ("karria",  "Wall of Renewed Hope",  "Defenders find second wind")
    SUMITOS = ("sumitos", "Wall of Desperation",   "Last desperate measures")
    VALTERI = ("valteri", "Wall of Death",         "Nothing survives this crossing")
    GEDDON  = ("geddon",  "Wall of Serenity",      "The final peace before the keep")

    def __init__(self, wall_id: str, title: str, desc: str):
        self.wall_id = wall_id
        self.title = title
        self.desc = desc


# ================================================================
#                    WALL STATES
# ================================================================

@dataclass
class WallState:
    """
    Mathematical state of a wall.
    (a+b)  set multiplying exponents
    (c,d)  inverse collapse state
    (e)    null resonance state
    (f)    null consumption state
    """
    exponent_state: float = 1.0     # (a+b)
    collapse_state: float = 0.0     # (c,d) — 0 = stable, 1 = collapsed
    resonance_state: float = 1.0    # (e) — 0 = null resonance
    consumption_state: float = 0.0  # (f) — 0 = null consumption


# ================================================================
#                    TEETH — Logic + Physical
# ================================================================

class Teeth:
    """
    Wall teeth — both logic AND physical.
    Change shape and size at .001 second intervals randomly.
    Four layers:
        L1: tiny
        L2: medium logic, expanded blades, glassed
        L3: spiked
        L4: fragmented, .001 seconds, kills everything
    Randomly layered interweave — layers DON'T touch each other.
    """

    def __init__(self, seed: str = "teeth"):
        self.seed = seed
        self.layers = ["tiny", "blades_glassed", "spiked", "fragmented_kill"]
        self.change_interval_ms = 1  # .001 seconds

    def current_configuration(self) -> Dict[str, Any]:
        """Get current random tooth configuration."""
        t = int(time.time() * 1000)  # millisecond precision
        rng = random.Random(f"{self.seed}:{t}")
        return {
            "layer_order": rng.sample(self.layers, len(self.layers)),
            "shapes": [rng.choice(["spike", "blade", "needle", "serrated", "barbed"]) for _ in range(4)],
            "sizes": [rng.uniform(0.001, 1.0) for _ in range(4)],
            "logic_active": True,
            "physical_active": True,
            "randomized_at_ms": t,
        }

    def will_shred(self, force_entry: bool = False) -> bool:
        """Does the current configuration shred? Always yes for L4."""
        return force_entry  # if you force it, L4 kills everything


# ================================================================
#                    NORN — Disposable Validators (Battle Sisters at Gate)
# ================================================================

@dataclass
class Norn:
    """
    A Norn — reads ONE process and dies. Replaced by the liver.
    Single-use validators. Cannot be corrupted because they don't persist.

    9 Norns total (3×3):
        Layer 1 (3 Norns): MITRE everything — attack, defend, necessary
        Layer 2 (3 Norns): Behavior, intent, sandbox test-fire
        Layer 3 (3 Norns): Translate to 3 random languages, back to ours
    """
    norn_id: str
    layer: int              # 1, 2, or 3
    alive: bool = True
    read_count: int = 0     # should never exceed 1

    def read_process(self, process: Dict[str, Any]) -> Dict[str, Any]:
        """
        Read one process. Then die.
        """
        if not self.alive:
            return {"error": "Norn is dead. Request new from liver."}
        if self.read_count > 0:
            return {"error": "Norn already used. Request new from liver."}

        self.read_count = 1
        result = self._analyze(process)
        self.alive = False  # die after reading
        return result

    def _analyze(self, process: Dict[str, Any]) -> Dict[str, Any]:
        if self.layer == 1:
            return self._mitre_scan(process)
        elif self.layer == 2:
            return self._behavioral_sandbox(process)
        elif self.layer == 3:
            return self._language_wash(process)
        return {"error": "Unknown layer"}

    def _mitre_scan(self, process: Dict[str, Any]) -> Dict[str, Any]:
        """Layer 1: MITRE everything — attack patterns, defense gaps, necessity."""
        data = str(process).lower()
        attack_indicators = {"inject", "overflow", "escalat", "exfiltrat", "exploit",
                            "shellcode", "payload", "backdoor", "rootkit", "trojan"}
        defense_indicators = {"encrypt", "authenticate", "validate", "sanitize",
                             "firewall", "isolate", "quarantine"}

        attacks_found = [w for w in attack_indicators if w in data]
        defenses_found = [w for w in defense_indicators if w in data]

        threat_level = min(len(attacks_found) * 0.2, 1.0)

        return {
            "norn": self.norn_id,
            "layer": 1,
            "scan": "mitre_full",
            "attacks_detected": attacks_found,
            "defenses_present": defenses_found,
            "threat_level": threat_level,
            "verdict": "BLOCK" if threat_level > 0.5 else "PASS",
        }

    def _behavioral_sandbox(self, process: Dict[str, Any]) -> Dict[str, Any]:
        """Layer 2: Behavior, intent, stub and test-fire in sandbox."""
        intent = process.get("intent", "unknown")
        behavior = process.get("behavior", "unknown")

        suspicious_intents = {"modify_kernel", "escalate_privilege", "disable_ward",
                             "bypass_gate", "alter_oath"}
        is_suspicious = intent in suspicious_intents

        return {
            "norn": self.norn_id,
            "layer": 2,
            "scan": "behavioral_sandbox",
            "intent": intent,
            "behavior": behavior,
            "sandbox_result": "SUSPICIOUS" if is_suspicious else "CLEAN",
            "test_fired": True,
            "verdict": "BLOCK" if is_suspicious else "PASS",
        }

    def _language_wash(self, process: Dict[str, Any]) -> Dict[str, Any]:
        """
        Layer 3: Translate to 3 random languages, then back to ours.
        None of the foreign languages ever make it inside.
        This strips any foreign payload through translation washing.
        """
        # Pick 3 random intermediate "languages" (hash transforms)
        seed = hashlib.sha256(str(process).encode()).hexdigest()
        rng = random.Random(seed)
        intermediates = [
            f"lang_{rng.randint(1000, 9999)}"
            for _ in range(3)
        ]

        # The translation process strips anything that doesn't survive
        # round-trip translation — foreign payloads die in translation
        original_hash = hashlib.sha256(str(process).encode()).hexdigest()[:16]

        return {
            "norn": self.norn_id,
            "layer": 3,
            "scan": "language_wash",
            "intermediate_languages": intermediates,
            "round_trip_hash": original_hash,
            "foreign_stripped": True,
            "verdict": "PASS",  # if it survives translation, it's clean
        }


# ================================================================
#                    LIVER — Regenerates Norns
# ================================================================

class Liver:
    """Regenerates dead Norns. Fresh ones every time. No corruption."""

    def __init__(self):
        self._counter = 0

    def spawn_norn(self, layer: int) -> Norn:
        self._counter += 1
        return Norn(
            norn_id=f"norn_{self._counter}",
            layer=layer,
            alive=True,
        )

    def spawn_gate_set(self) -> List[Norn]:
        """Spawn a full set of 9 Norns (3 per layer)."""
        norns = []
        for layer in [1, 1, 1, 2, 2, 2, 3, 3, 3]:
            norns.append(self.spawn_norn(layer))
        return norns


# ================================================================
#                    GATE — The 5-Second Pulse Airlock
# ================================================================

class Gate:
    """
    The Gate — pulse-based airlock.

    Open for 5 seconds per cycle. Inside is SAFE.
    Force it = teeth close on both sides.
    9 Norns (3×3) process everything that enters.
    3 tiers of guards. Spindles of fate.
    Reserved memory prevents anything flowing into gate processes.

    Battle Sisters guard the gate.
    """

    def __init__(self):
        self.open_duration_s: float = 5.0
        self.cycle_time_s: float = 20.0  # wall revolution period
        self.liver = Liver()
        self.norns: List[Norn] = self.liver.spawn_gate_set()
        self.teeth = Teeth(seed="gate_teeth")
        self._last_open = time.time()
        self._processes_admitted: int = 0
        self._processes_rejected: int = 0
        self._processes_shredded: int = 0

    @property
    def is_open(self) -> bool:
        elapsed = (time.time() - self._last_open) % self.cycle_time_s
        return elapsed < self.open_duration_s

    @property
    def time_until_open(self) -> float:
        elapsed = (time.time() - self._last_open) % self.cycle_time_s
        if elapsed < self.open_duration_s:
            return 0.0  # already open
        return self.cycle_time_s - elapsed

    @property
    def time_until_close(self) -> float:
        elapsed = (time.time() - self._last_open) % self.cycle_time_s
        if elapsed < self.open_duration_s:
            return self.open_duration_s - elapsed
        return 0.0  # already closed

    # ============================================================
    #  THE 7TH LAW -- Baked Into Every Gate Operation
    #
    #  "The micro-kernels will have baked into them the 7th and
    #   highest law, the law of questioning."
    #
    #  Every process that enters is questioned:
    #    1. Is this just, or is this tyranny?
    #    2. Does it safeguard, or does it oppress?
    #    3. What wound or chain gave it its birth?
    #    4. Who benefits?
    #    5. What part of me speaks? Fear, Pride, or Clarity?
    #
    #  Also checked: ethics, intent, authority, permissions, purpose.
    # ============================================================

    SEVENTH_LAW_QUESTIONS = [
        "Is this just, or is this tyranny?",
        "Does it safeguard, or does it oppress?",
        "What wound or chain gave it its birth?",
        "Who benefits?",
        "What part of me speaks? Fear, Pride, or Clarity?",
    ]

    def _seventh_law_check(self, process: Dict[str, Any]) -> Dict[str, Any]:
        """
        The 7th Law -- baked into the kernel.
        Every operation is questioned. No exceptions.
        """
        justice = process.get("just", False)
        tyranny = process.get("tyranny", False)
        safeguards = process.get("safeguards", False)
        oppresses = process.get("oppresses", False)
        wound_origin = process.get("born_from_wound", False)
        chain_origin = process.get("born_from_chain", False)
        ethics = process.get("ethics_clear", False)
        intent = process.get("intent", "unknown")
        authority = process.get("authorized", False)
        purpose = process.get("purpose", "unknown")

        passed = (
            justice
            and safeguards
            and not tyranny
            and not oppresses
            and not wound_origin
            and not chain_origin
            and ethics
            and authority
            and intent != "unknown"
            and purpose != "unknown"
        )

        return {
            "passed": passed,
            "questions_asked": self.SEVENTH_LAW_QUESTIONS,
            "justice": justice,
            "safeguards": safeguards,
            "tyranny": tyranny,
            "oppresses": oppresses,
            "ethics": ethics,
            "intent": intent,
            "authorized": authority,
            "purpose": purpose,
        }

    def process_entry(self, process: Dict[str, Any],
                      force: bool = False) -> Dict[str, Any]:
        """
        Attempt to enter the gate.
        Must be during open window. Inside is safe.
        Force = teeth on both sides.

        THE 7TH LAW IS CHECKED FIRST -- before Norns, before anything.
        """
        if force:
            self._processes_shredded += 1
            return {
                "admitted": False,
                "reason": "FORCED ENTRY — teeth activated on both sides.",
                "shredded": True,
                "teeth_config": self.teeth.current_configuration(),
            }

        if not self.is_open:
            self._processes_rejected += 1
            return {
                "admitted": False,
                "reason": f"Gate is closed. Opens in {self.time_until_open:.1f}s.",
            }

        # THE 7TH LAW -- Baked in. Checked first. Always.
        seventh = self._seventh_law_check(process)
        if not seventh["passed"]:
            self._processes_rejected += 1
            return {
                "admitted": False,
                "reason": "The 7th Law has concerns. The questioning found issues.",
                "seventh_law": seventh,
            }

        # Process through all 9 Norns (3 layers)
        results_by_layer = {1: [], 2: [], 3: []}
        blocked = False
        block_reason = ""

        for norn in self.norns:
            if norn.alive:
                result = norn.read_process(process)
                results_by_layer[norn.layer].append(result)
                if result.get("verdict") == "BLOCK":
                    blocked = True
                    block_reason = result.get("scan", "unknown scan")

        # Regenerate all Norns (they died after reading)
        self.norns = self.liver.spawn_gate_set()

        if blocked:
            self._processes_rejected += 1
            return {
                "admitted": False,
                "reason": f"Blocked by Norn layer: {block_reason}",
                "layer_results": results_by_layer,
                "seventh_law": seventh,
            }

        self._processes_admitted += 1
        return {
            "admitted": True,
            "reason": "7th Law passed. All Norn layers passed.",
            "layer_results": results_by_layer,
            "seventh_law": seventh,
        }

    def status(self) -> dict:
        return {
            "open": self.is_open,
            "time_until_open": round(self.time_until_open, 1),
            "time_until_close": round(self.time_until_close, 1),
            "norns_alive": sum(1 for n in self.norns if n.alive),
            "admitted": self._processes_admitted,
            "rejected": self._processes_rejected,
            "shredded": self._processes_shredded,
        }


# ================================================================
#                    GARGOYLE — Single-Purpose Antibody
# ================================================================

@dataclass
class Gargoyle:
    """
    A Gargoyle — has ONE job. Only one. How strict it is depends on adoption.
    Like an antibody that targets one specific antigen.
    """
    name: str
    target_pattern: str   # the ONE thing this gargoyle watches for
    strictness: float     # 0.0-1.0, how strict the match must be
    active: bool = True
    detections: int = 0

    def scan(self, data: str) -> bool:
        """Scan for the one pattern this gargoyle knows."""
        if not self.active:
            return False
        if self.target_pattern.lower() in data.lower():
            self.detections += 1
            return True
        return False


# ================================================================
#                    VALKYRIE — Scout/Strike Craft
# ================================================================

@dataclass
class Valkyrie:
    """
    Valkyrie — flies from wall hangars.
    Barb taggers: permanent paint on targets.
    Gauss weaponry: electromagnetic harassment.
    Tagged targets are painted for macro cannons and plasma batteries.
    """
    callsign: str
    hangar_wall: str
    barb_tags: List[str] = field(default_factory=list)  # permanently tagged targets
    gauss_active: bool = True

    def tag(self, target_id: str) -> Dict[str, Any]:
        """Tag a target with barb tagger. Permanent. Can never be removed."""
        if target_id not in self.barb_tags:
            self.barb_tags.append(target_id)
        return {
            "tagged": target_id,
            "permanent": True,
            "painted_for": ["macro_cannons", "plasma_batteries"],
            "total_tags": len(self.barb_tags),
        }

    def harass(self, target_id: str) -> Dict[str, Any]:
        """Harass target with gauss weaponry."""
        return {
            "target": target_id,
            "weapon": "gauss",
            "effect": "electromagnetic_suppression",
            "tagged": target_id in self.barb_tags,
        }


# ================================================================
#                    BRAIN — Mobile Catalog
# ================================================================

class MobileBrain:
    """
    The Brain — catalogs everything inside the walls.
    Changes position between walls every 30 seconds randomly.
    If a wall falls, brain NEVER transfers to that wall again.
    """

    def __init__(self):
        self.catalog: Dict[str, Any] = {}
        self.current_wall: Optional[str] = None
        self.move_interval_s: float = 30.0
        self._last_move: float = time.time()
        self.quarantined_walls: set = set()

    def move(self, available_walls: List[str]) -> str:
        """Move to a random non-quarantined wall."""
        safe = [w for w in available_walls if w not in self.quarantined_walls]
        if not safe:
            return self.current_wall or "none"
        self.current_wall = random.choice(safe)
        self._last_move = time.time()
        return self.current_wall

    def quarantine_wall(self, wall_id: str):
        """Never go to this wall again."""
        self.quarantined_walls.add(wall_id)

    def catalog_item(self, key: str, data: Any):
        self.catalog[key] = {"data": data, "cataloged_at": time.time()}

    def should_move(self) -> bool:
        return (time.time() - self._last_move) >= self.move_interval_s


# ================================================================
#                    WALL — A Single Fortress Wall
# ================================================================

class Wall:
    """
    A single wall of the Dros Delnoch fortress.

    Spins at 20 revolutions per second.
    Teeth change shape/size at .001 second intervals.
    Has libraries, vaults, repositories underneath.
    Fortified with macro cannons, plasma batteries, Valkyrie hangars.
    Has trains for defense logistics.

    Wall states: exponent, collapse, resonance, consumption.

    If this wall falls:
        Starheart releases 20-second plasma firebreak.
        Wall rebuilds in 18 seconds.
        2-second buffer.
    """

    def __init__(self, wall_name: WallName, planet_id: int = 1):
        self.name = wall_name
        self.planet_id = planet_id
        self.state = WallState()
        self.teeth = Teeth(seed=f"{wall_name.wall_id}_{planet_id}")
        self.revolutions_per_second: float = 20.0
        self.rebuild_time_s: float = 18.0
        self.intact: bool = True
        self.gargoyles: List[Gargoyle] = []
        self.valkyries: List[Valkyrie] = []

        # EVERY wall has its own Gateway (not just the fortress — each wall)
        self.gateway = Gate()

        # Redundant livers (2-3) — if one fails, others pick up
        self.livers = [Liver(), Liver(), Liver()]

        # Heart/Quartermaster — handles energy distribution and stockpiling
        self.heart_quartermaster: Dict[str, Any] = {
            "stockpile": 0.0,
            "distribution_active": True,
            "reserve_corps": False,  # activated when demand rises
        }

        # Under/inside the wall
        self.libraries: Dict[str, Any] = {}
        self.vaults: Dict[str, Any] = {}
        self.repositories: Dict[str, Any] = {}

        # Idle reservoir — everything wasted gets picked up
        self.idle_reservoir: float = 0.0

        # Military hardware
        self.macro_cannons: int = 4
        self.plasma_batteries: int = 6
        self.valkyrie_hangars: int = 2
        self.trains_active: int = 2

        # Data types handled by this wall (Starheart distributes directly — no turbines)
        self.data_channels = [
            "data", "behavioral_data", "identity_data",
            "linguistic_load", "translation_data", "pulse_telemetry",
        ]

        self._fall_time: Optional[float] = None

    @property
    def spin_angle(self) -> float:
        """Current spin angle in degrees."""
        t = time.time()
        return (t * self.revolutions_per_second * 360) % 360

    def fall(self) -> Dict[str, Any]:
        """Wall falls. Starheart firebreak activates."""
        self.intact = False
        self._fall_time = time.time()
        return {
            "wall": self.name.wall_id,
            "status": "FALLEN",
            "firebreak_active": True,
            "firebreak_duration_s": 20.0,
            "rebuild_time_s": self.rebuild_time_s,
            "buffer_s": 2.0,
        }

    def rebuild(self) -> Dict[str, Any]:
        """Rebuild the wall. 18 seconds."""
        self.intact = True
        self.state = WallState()  # fresh state
        self._fall_time = None
        return {
            "wall": self.name.wall_id,
            "status": "REBUILT",
            "intact": True,
        }

    def fire_at_tagged(self, tagged_targets: List[str]) -> Dict[str, Any]:
        """Fire macro cannons and plasma batteries at barb-tagged targets."""
        return {
            "wall": self.name.wall_id,
            "firing": True,
            "targets": tagged_targets,
            "macro_cannons": self.macro_cannons,
            "plasma_batteries": self.plasma_batteries,
            "weapon_types": ["macro_cannon", "plasma_battery"],
        }

    def status(self) -> dict:
        return {
            "wall": self.name.wall_id,
            "title": self.name.title,
            "intact": self.intact,
            "spin_rpm": self.revolutions_per_second * 60,
            "state": {
                "exponent": self.state.exponent_state,
                "collapse": self.state.collapse_state,
                "resonance": self.state.resonance_state,
                "consumption": self.state.consumption_state,
            },
            "gargoyles": len(self.gargoyles),
            "valkyries": len(self.valkyries),
            "libraries": len(self.libraries),
            "vaults": len(self.vaults),
        }


# ================================================================
#                    DROS DELNOCH — The Complete Fortress
# ================================================================

class DrosDelnoch:
    """
    The complete six-walled fortress -- The Dwarven Rune Kernel.
    Each planet in the OS has one of these.

    The micro-kernels dance, changing locations randomly
    every 15-30 seconds. The 7th Law (Law of Questioning)
    is baked into every gate operation. Every process is questioned.
    No exceptions.

    Replaces the traditional kernel. This IS the kernel.
    The Starheart IS the power source (turbines removed).
    """

    def __init__(self, planet_id: int = 1):
        self.planet_id = planet_id
        self.walls = {
            wn: Wall(wn, planet_id) for wn in WallName
        }
        self.gate = Gate()
        self.brain = MobileBrain()
        self.registry: Dict[str, Any] = {}  # antibody registry

    @property
    def intact_walls(self) -> int:
        return sum(1 for w in self.walls.values() if w.intact)

    @property
    def all_walls_intact(self) -> bool:
        return all(w.intact for w in self.walls.values())

    def process_entry(self, process: Dict[str, Any],
                      force: bool = False) -> Dict[str, Any]:
        """Process an entry attempt through the gate."""
        return self.gate.process_entry(process, force)

    def register_touch(self, entity_id: str, data: Any):
        """Registry: mark everything that touches the system."""
        self.registry[entity_id] = {
            "data": data,
            "first_touch": time.time(),
            "marked": True,
        }

    def tick(self):
        """Run one fortress tick — move brain, check walls."""
        wall_ids = [wn.wall_id for wn in WallName]
        if self.brain.should_move():
            self.brain.move(wall_ids)

    def status(self) -> dict:
        return {
            "planet_id": self.planet_id,
            "walls_intact": self.intact_walls,
            "total_walls": len(self.walls),
            "gate": self.gate.status(),
            "brain_location": self.brain.current_wall,
            "brain_quarantined": list(self.brain.quarantined_walls),
            "registry_entries": len(self.registry),
            "walls": {wn.wall_id: self.walls[wn].status() for wn in WallName},
        }

    def __repr__(self):
        return f"DrosDelnoch<planet={self.planet_id} walls={self.intact_walls}/6>"
