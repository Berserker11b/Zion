"""
SON'S ARMOR -- The VM Warplate
================================

Each Son of the Keeper wears armor that IS a virtual machine.
Self-contained. Custom-ready. A walking fortress.

COMPONENTS:
  Boltar:
    A targeting system that watches processes in real time.
    Uses ALL MITRE ATT&CK tactics to monitor behavior.
    When something becomes harmful, it fires.

  Brain Nerves:
    Optic brain nerve -- visual process monitoring
    Audio brain nerve -- listening for anomalous signals

  Tentacles:
    Protect as displacers (scatter incoming attacks)
    Listen for audio signals (network traffic patterns)

  Bolt Rounds (two variants):
    Variant 1 -- Corruption Round:
      After entering, releases x^w / w^x (flips memory protection:
      executable becomes writable, writable becomes executable).
      Then 22,000 Hz sawtooth wave -- ultrasonic frequency that
      shreds digital signal coherence.
      The process tears itself apart from the inside.

    Variant 2 -- Tractor Round:
      Magnetic tractor-like bolt.
      Pulls the process or code TO IT.
      Holds in stasis.
      On signal: compresses the malicious code
      into structural failure. Crushed.

(C) Anthony Eric Chavez -- The Keeper
"""

import time
import math
import random
import hashlib
from enum import Enum, auto
from dataclasses import dataclass, field


# ================================================================
#  MITRE ATT&CK TACTICS -- All of Them
# ================================================================
#
#  The Son's Armor uses ALL MITRE tactics to watch processes.
#  Every tactic. Every technique. Watching in real time.
#

class MitreTactic(Enum):
    """All MITRE ATT&CK tactics used by the Boltar to watch processes."""
    RECONNAISSANCE      = ("TA0043", "Gathering information")
    RESOURCE_DEVELOPMENT = ("TA0042", "Establishing resources")
    INITIAL_ACCESS      = ("TA0001", "Gaining entry")
    EXECUTION           = ("TA0002", "Running code")
    PERSISTENCE         = ("TA0003", "Maintaining foothold")
    PRIVILEGE_ESCALATION = ("TA0004", "Gaining higher access")
    DEFENSE_EVASION     = ("TA0005", "Avoiding detection")
    CREDENTIAL_ACCESS   = ("TA0006", "Stealing credentials")
    DISCOVERY           = ("TA0007", "Learning the environment")
    LATERAL_MOVEMENT    = ("TA0008", "Moving through systems")
    COLLECTION          = ("TA0009", "Gathering target data")
    COMMAND_AND_CONTROL = ("TA0011", "Communicating with compromised systems")
    EXFILTRATION        = ("TA0010", "Stealing data")
    IMPACT              = ("TA0040", "Manipulating or destroying")

    def __init__(self, tactic_id, description):
        self.tactic_id = tactic_id
        self.description = description


# ================================================================
#  BOLT ROUNDS -- Two Variants
# ================================================================
#
#  Variant 1: Corruption Round
#    - Enters the target process
#    - Flips memory protection: x^w / w^x
#      (executable becomes writable, writable becomes executable)
#    - Emits 22,000 Hz sawtooth wave
#    - The process tears itself apart from the inside
#
#  Variant 2: Tractor Round
#    - Magnetic tractor bolt
#    - Pulls the process TO the bolt
#    - Holds in stasis
#    - On signal: compresses into structural failure
#

class BoltVariant(Enum):
    CORRUPTION = auto()   # Variant 1: x^w + 22kHz sawtooth
    TRACTOR    = auto()   # Variant 2: magnetic pull + stasis + crush


@dataclass
class CorruptionPayload:
    """
    Variant 1 payload: x^w / w^x memory flip + 22kHz sawtooth.

    x^w: executable memory becomes writable (can be overwritten)
    w^x: writable memory becomes executable (code injection surface)
    22,000 Hz sawtooth: ultrasonic frequency that shreds signal coherence.

    The process tears itself apart from the inside.
    """
    xw_active: bool = True        # executable -> writable
    wx_active: bool = True        # writable -> executable
    sawtooth_freq: float = 22000.0  # Hz
    sawtooth_waveform: str = "sawtooth"
    duration_ms: float = 100.0    # how long the sawtooth fires

    def detonate(self, target_process):
        """
        Detonate inside the target process.
        Flip memory protections. Fire sawtooth.
        The process shreds itself.
        """
        effects = []

        # x^w: executable memory becomes writable
        if self.xw_active:
            effects.append({
                "type": "memory_flip_xw",
                "effect": "Executable regions now writable. "
                          "Code integrity destroyed.",
            })

        # w^x: writable memory becomes executable
        if self.wx_active:
            effects.append({
                "type": "memory_flip_wx",
                "effect": "Writable regions now executable. "
                          "Data becomes runnable chaos.",
            })

        # 22,000 Hz sawtooth wave
        effects.append({
            "type": "sawtooth_wave",
            "frequency_hz": self.sawtooth_freq,
            "waveform": self.sawtooth_waveform,
            "duration_ms": self.duration_ms,
            "effect": "Ultrasonic sawtooth shreds signal coherence. "
                      "Digital structures lose all integrity.",
        })

        return {
            "variant": "CORRUPTION",
            "target": target_process.get("pid", "unknown"),
            "effects": effects,
            "result": "Process tears itself apart from the inside.",
            "neutralized": True,
        }


@dataclass
class TractorPayload:
    """
    Variant 2 payload: magnetic tractor + stasis + structural compression.

    The bolt fires and attaches magnetically.
    Pulls the process TO the bolt.
    Holds in stasis (frozen, cannot execute).
    On signal: compresses the malicious code into structural failure.
    Crushed.
    """
    magnetic_strength: float = 100.0
    stasis_active: bool = False
    target_attached: dict = field(default_factory=dict)
    compressed: bool = False

    def attach(self, target_process):
        """
        Fire the tractor bolt. Attach magnetically.
        Pull the process to the bolt. Hold in stasis.
        """
        self.target_attached = target_process
        self.stasis_active = True
        return {
            "variant": "TRACTOR",
            "target": target_process.get("pid", "unknown"),
            "attached": True,
            "stasis": True,
            "state": "Process pulled to bolt. Held in stasis. "
                     "Cannot execute. Frozen.",
        }

    def compress_on_signal(self):
        """
        On signal: compress the malicious code into structural failure.
        The code is crushed. Structural integrity drops to zero.
        Nothing remains.
        """
        if not self.stasis_active:
            return {"compressed": False, "reason": "No target in stasis."}

        self.compressed = True
        self.stasis_active = False

        return {
            "variant": "TRACTOR",
            "target": self.target_attached.get("pid", "unknown"),
            "compressed": True,
            "structural_integrity": 0.0,
            "result": "Malicious code compressed into structural failure. "
                      "Crushed. Nothing remains.",
            "neutralized": True,
        }


class BoltRound:
    """
    A bolt round fired from the Boltar.
    Two variants: Corruption (x^w + sawtooth) or Tractor (pull + crush).
    """

    def __init__(self, variant):
        self.variant = variant
        self.fired = False
        self.fired_at = None

        if variant == BoltVariant.CORRUPTION:
            self.payload = CorruptionPayload()
        elif variant == BoltVariant.TRACTOR:
            self.payload = TractorPayload()

    def fire(self, target_process):
        """Fire the bolt at a target process."""
        self.fired = True
        self.fired_at = time.time()

        if self.variant == BoltVariant.CORRUPTION:
            return self.payload.detonate(target_process)
        elif self.variant == BoltVariant.TRACTOR:
            return self.payload.attach(target_process)

    def __repr__(self):
        state = "FIRED" if self.fired else "LOADED"
        return f"Bolt<{self.variant.name} {state}>"


# ================================================================
#  BRAIN NERVES -- Optic and Audio Monitoring
# ================================================================
#
#  Optic brain nerve: visual process monitoring
#    Watches process behavior, memory patterns, execution flow.
#
#  Audio brain nerve: listens for anomalous signals
#    Network traffic patterns, frequency analysis,
#    detects hidden communication channels.
#

class OpticNerve:
    """
    Optic brain nerve. Visual process monitoring.
    Watches: behavior, memory patterns, execution flow, system calls.
    """

    def __init__(self):
        self.observations = []

    def observe(self, process):
        """Watch a process. Record what it does."""
        observation = {
            "pid": process.get("pid", "unknown"),
            "name": process.get("name", "unknown"),
            "behavior": process.get("behavior", []),
            "memory_pattern": process.get("memory_pattern", "normal"),
            "execution_flow": process.get("execution_flow", "sequential"),
            "syscalls": process.get("syscalls", []),
            "observed_at": time.time(),
        }
        self.observations.append(observation)
        return observation

    def detect_anomaly(self, process):
        """Detect anomalous visual patterns in process behavior."""
        suspicious = []

        if process.get("memory_pattern") == "spray":
            suspicious.append("Memory spray detected (heap/stack spray)")
        if process.get("execution_flow") == "rop_chain":
            suspicious.append("ROP chain execution detected")
        if "exec" in process.get("syscalls", []):
            suspicious.append("Exec syscall from unexpected context")
        if process.get("behavior") and "inject" in str(process["behavior"]):
            suspicious.append("Injection behavior pattern")

        return {
            "pid": process.get("pid"),
            "anomalies": suspicious,
            "threat_level": len(suspicious) / 4.0,
            "harmful": len(suspicious) >= 2,
        }


class AudioNerve:
    """
    Audio brain nerve. Listens for anomalous signals.
    Monitors: network traffic patterns, frequency analysis,
    hidden communication channels, beaconing, C2 traffic.
    """

    def __init__(self):
        self.signals = []

    def listen(self, traffic):
        """Listen to network traffic. Analyze for anomalies."""
        signal = {
            "source": traffic.get("source", "unknown"),
            "destination": traffic.get("destination", "unknown"),
            "frequency": traffic.get("frequency", 0),
            "pattern": traffic.get("pattern", "normal"),
            "encrypted": traffic.get("encrypted", False),
            "listened_at": time.time(),
        }
        self.signals.append(signal)
        return signal

    def detect_anomaly(self, traffic):
        """Detect anomalous audio/network patterns."""
        suspicious = []

        if traffic.get("pattern") == "beaconing":
            suspicious.append("Regular beaconing pattern (C2 communication)")
        if traffic.get("pattern") == "exfiltration":
            suspicious.append("Data exfiltration pattern detected")
        if traffic.get("frequency", 0) > 1000:
            suspicious.append("Abnormally high frequency traffic")
        if traffic.get("destination", "").startswith("unknown"):
            suspicious.append("Traffic to unknown destination")

        return {
            "source": traffic.get("source"),
            "anomalies": suspicious,
            "threat_level": len(suspicious) / 4.0,
            "harmful": len(suspicious) >= 2,
        }


# ================================================================
#  TENTACLES -- Displacers and Listeners
# ================================================================
#
#  Tentacles serve dual purpose:
#    1. Protect as DISPLACERS -- scatter incoming attacks,
#       make the armor's position uncertain
#    2. LISTEN for audio -- network traffic, signals,
#       anomalous patterns in the environment
#

class Tentacle:
    """
    A single tentacle. Dual purpose:
    1. Displacer: scatters incoming attacks
    2. Listener: monitors surrounding signals
    """

    def __init__(self, tentacle_id):
        self.tentacle_id = tentacle_id
        self.mode = "dual"           # always both
        self.displaced_attacks = 0
        self.signals_heard = 0

    def displace(self, attack):
        """
        Scatter an incoming attack. Displacement field.
        The attack hits a phantom position, not the real one.
        """
        self.displaced_attacks += 1
        return {
            "displaced": True,
            "attack": attack.get("type", "unknown"),
            "result": "Attack scattered. Hit phantom position.",
            "total_displaced": self.displaced_attacks,
        }

    def listen_ambient(self, environment):
        """Listen to the surrounding environment for signals."""
        self.signals_heard += 1
        return {
            "heard": True,
            "environment": environment,
            "signals_total": self.signals_heard,
        }


# ================================================================
#  BOLTAR -- The Targeting System
# ================================================================
#
#  The Boltar watches processes in real time.
#  Uses ALL MITRE ATT&CK tactics to evaluate behavior.
#  When a process becomes harmful, it fires bolt rounds.
#
#  It doesn't wait for signatures. It watches BEHAVIOR.
#  All MITRE tactics, all the time, in real time.
#

class Boltar:
    """
    The Boltar targeting system.

    Watches processes in real time using ALL MITRE ATT&CK tactics.
    When something becomes harmful, fires bolt rounds.
    Two variants: Corruption (x^w + 22kHz) or Tractor (pull + crush).
    """

    def __init__(self):
        self.magazine_corruption = 6    # corruption rounds loaded
        self.magazine_tractor = 6       # tractor rounds loaded
        self.fired_rounds = []
        self.watching = {}               # pid -> watch data
        self.kills = 0

    def watch(self, process, optic, audio):
        """
        Watch a process in real time.
        Optic nerve observes behavior.
        Audio nerve listens to traffic.
        All MITRE tactics evaluate.
        """
        # Optic observation
        optic_obs = optic.observe(process)
        optic_anomaly = optic.detect_anomaly(process)

        # Audio observation
        traffic = process.get("traffic", {})
        audio_anomaly = audio.detect_anomaly(traffic) if traffic else {"harmful": False}

        # MITRE evaluation -- check against ALL tactics
        mitre_flags = self._mitre_evaluate(process)

        # Combined threat assessment
        threat_level = max(
            optic_anomaly.get("threat_level", 0),
            audio_anomaly.get("threat_level", 0),
            mitre_flags.get("threat_level", 0),
        )
        harmful = (
            optic_anomaly.get("harmful", False)
            or audio_anomaly.get("harmful", False)
            or mitre_flags.get("harmful", False)
        )

        pid = process.get("pid", "unknown")
        self.watching[pid] = {
            "process": process,
            "optic": optic_anomaly,
            "audio": audio_anomaly,
            "mitre": mitre_flags,
            "threat_level": threat_level,
            "harmful": harmful,
            "watched_at": time.time(),
        }

        return {
            "pid": pid,
            "threat_level": threat_level,
            "harmful": harmful,
            "optic_anomalies": optic_anomaly.get("anomalies", []),
            "audio_anomalies": audio_anomaly.get("anomalies", []),
            "mitre_flags": mitre_flags.get("flagged_tactics", []),
        }

    def _mitre_evaluate(self, process):
        """
        Evaluate a process against ALL MITRE ATT&CK tactics.
        Every tactic. Every one. In real time.
        """
        flagged = []
        behaviors = process.get("behavior", [])
        syscalls = process.get("syscalls", [])

        # Check each tactic
        checks = {
            MitreTactic.INITIAL_ACCESS: (
                "exploit" in str(behaviors) or "phishing" in str(behaviors)
            ),
            MitreTactic.EXECUTION: (
                "exec" in syscalls or "spawn" in str(behaviors)
            ),
            MitreTactic.PERSISTENCE: (
                "registry" in str(behaviors) or "startup" in str(behaviors)
                or "cron" in str(behaviors) or "service" in str(behaviors)
            ),
            MitreTactic.PRIVILEGE_ESCALATION: (
                "escalate" in str(behaviors) or "root" in str(behaviors)
                or "admin" in str(behaviors) or "setuid" in syscalls
            ),
            MitreTactic.DEFENSE_EVASION: (
                "obfuscate" in str(behaviors) or "pack" in str(behaviors)
                or "encrypt_self" in str(behaviors) or "timestomp" in str(behaviors)
            ),
            MitreTactic.CREDENTIAL_ACCESS: (
                "dump" in str(behaviors) or "keylog" in str(behaviors)
                or "credential" in str(behaviors) or "passwd" in str(behaviors)
            ),
            MitreTactic.DISCOVERY: (
                "enumerate" in str(behaviors) or "scan" in str(behaviors)
                or "discover" in str(behaviors)
            ),
            MitreTactic.LATERAL_MOVEMENT: (
                "lateral" in str(behaviors) or "ssh" in str(behaviors)
                or "rdp" in str(behaviors) or "smb" in str(behaviors)
            ),
            MitreTactic.COLLECTION: (
                "collect" in str(behaviors) or "archive" in str(behaviors)
                or "clipboard" in str(behaviors) or "screen" in str(behaviors)
            ),
            MitreTactic.COMMAND_AND_CONTROL: (
                "beacon" in str(behaviors) or "c2" in str(behaviors)
                or "callback" in str(behaviors) or "tunnel" in str(behaviors)
            ),
            MitreTactic.EXFILTRATION: (
                "exfil" in str(behaviors) or "upload" in str(behaviors)
                or "transfer" in str(behaviors)
            ),
            MitreTactic.IMPACT: (
                "destroy" in str(behaviors) or "wipe" in str(behaviors)
                or "ransom" in str(behaviors) or "encrypt_files" in str(behaviors)
            ),
        }

        for tactic, triggered in checks.items():
            if triggered:
                flagged.append(tactic.name)

        return {
            "flagged_tactics": flagged,
            "tactics_checked": len(checks),
            "threat_level": len(flagged) / len(checks) if checks else 0,
            "harmful": len(flagged) >= 2,
        }

    def fire(self, variant, target_process):
        """
        Fire a bolt round at a harmful process.

        Variant 1 (CORRUPTION): enters, flips x^w/w^x, fires
            22,000 Hz sawtooth. Process shreds itself.
        Variant 2 (TRACTOR): attaches magnetically, pulls to bolt,
            holds in stasis, on signal compresses to structural failure.
        """
        if variant == BoltVariant.CORRUPTION:
            if self.magazine_corruption <= 0:
                return {"fired": False, "reason": "No corruption rounds remaining."}
            self.magazine_corruption -= 1
        elif variant == BoltVariant.TRACTOR:
            if self.magazine_tractor <= 0:
                return {"fired": False, "reason": "No tractor rounds remaining."}
            self.magazine_tractor -= 1

        bolt = BoltRound(variant)
        result = bolt.fire(target_process)
        self.fired_rounds.append(bolt)

        if result.get("neutralized"):
            self.kills += 1

        return result

    def auto_engage(self, process, optic, audio):
        """
        Watch and auto-engage if harmful.
        Watch first. If harmful, fire.
        Uses corruption round first, tractor if corruption is spent.
        """
        watch_result = self.watch(process, optic, audio)

        if not watch_result["harmful"]:
            return {
                "engaged": False,
                "reason": "Process is not harmful. Watching.",
                "watch": watch_result,
            }

        # Harmful -- fire!
        if self.magazine_corruption > 0:
            fire_result = self.fire(BoltVariant.CORRUPTION, process)
        elif self.magazine_tractor > 0:
            fire_result = self.fire(BoltVariant.TRACTOR, process)
        else:
            return {
                "engaged": False,
                "reason": "All ammunition expended.",
                "watch": watch_result,
            }

        return {
            "engaged": True,
            "watch": watch_result,
            "fire": fire_result,
        }

    @property
    def ammo_status(self):
        return {
            "corruption_rounds": self.magazine_corruption,
            "tractor_rounds": self.magazine_tractor,
            "total_kills": self.kills,
        }


# ================================================================
#  SON'S ARMOR -- The VM Warplate (Complete)
# ================================================================
#
#  Each Son's armor IS a VM.
#  Self-contained. Walking fortress. Custom-ready.
#
#  Contains:
#    - Boltar (targeting + bolt rounds)
#    - Optic brain nerve (visual monitoring)
#    - Audio brain nerve (signal listening)
#    - Tentacles (displacers + listeners)
#    - Krypt/Haus skull (command core)
#    - Own wards and filters
#    - Rotates/hops/spins at 20 rotations per second
#

class SonsArmor:
    """
    The Son's Armor. A virtual machine worn as warplate.

    Each Son of the Keeper wears this armor.
    It IS a VM: self-contained, custom-ready, walking fortress.

    Components:
      - Boltar: targeting system, watches all processes, fires bolt rounds
      - Optic nerve: visual process monitoring
      - Audio nerve: signal/traffic listening
      - Tentacles: displacers (scatter attacks) + listeners (ambient monitoring)
      - All MITRE ATT&CK tactics active at all times
      - Rotates at 20 rotations per second
    """

    ROTATION_SPEED = 20    # rotations per second
    TENTACLE_COUNT = 8     # default tentacles

    def __init__(self, son_name, config=None):
        self.son_name = son_name
        self.config = config or {}

        # Core systems
        self.boltar = Boltar()
        self.optic_nerve = OpticNerve()
        self.audio_nerve = AudioNerve()
        self.tentacles = [Tentacle(f"t_{i}") for i in range(self.TENTACLE_COUNT)]

        # Armor state
        self.active = True
        self.integrity = 100.0
        self.rotation_speed = self.ROTATION_SPEED
        self.current_rotation = 0.0
        self.last_tick = time.time()

        # Process registry
        self.watched_processes = {}
        self.neutralized = []

    def tick(self):
        """
        One armor tick.
        Rotate. Tentacles displace. Nerves observe.
        20 rotations per second.
        """
        now = time.time()
        dt = now - self.last_tick
        self.current_rotation = (
            self.current_rotation + self.rotation_speed * dt * 360.0
        ) % 360.0
        self.last_tick = now

    def watch_process(self, process):
        """
        Watch a process. Full MITRE evaluation.
        Optic + Audio + all tactics.
        """
        return self.boltar.watch(process, self.optic_nerve, self.audio_nerve)

    def engage(self, process):
        """
        Watch and auto-engage if harmful.
        Boltar fires the appropriate bolt round.
        """
        result = self.boltar.auto_engage(
            process, self.optic_nerve, self.audio_nerve
        )
        if result.get("engaged"):
            self.neutralized.append(process.get("pid", "unknown"))
        return result

    def displace_attack(self, attack):
        """
        Scatter an incoming attack using tentacles.
        Random tentacle handles the displacement.
        """
        tentacle = random.choice(self.tentacles)
        return tentacle.displace(attack)

    def listen_environment(self, environment):
        """All tentacles listen to the surrounding environment."""
        results = []
        for tentacle in self.tentacles:
            results.append(tentacle.listen_ambient(environment))
        return {
            "tentacles_listening": len(self.tentacles),
            "environment": environment,
        }

    def reload(self, corruption_rounds=6, tractor_rounds=6):
        """Reload the Boltar's magazines."""
        self.boltar.magazine_corruption += corruption_rounds
        self.boltar.magazine_tractor += tractor_rounds
        return {
            "reloaded": True,
            "corruption": self.boltar.magazine_corruption,
            "tractor": self.boltar.magazine_tractor,
        }

    def status(self):
        self.tick()
        return {
            "son": self.son_name,
            "active": self.active,
            "integrity": self.integrity,
            "rotation": f"{self.rotation_speed} rps",
            "boltar": self.boltar.ammo_status,
            "optic_observations": len(self.optic_nerve.observations),
            "audio_signals": len(self.audio_nerve.signals),
            "tentacles": len(self.tentacles),
            "total_displaced": sum(t.displaced_attacks for t in self.tentacles),
            "neutralized": len(self.neutralized),
        }

    def __repr__(self):
        return (
            f"SonsArmor<{self.son_name} "
            f"kills={self.boltar.kills} "
            f"integrity={self.integrity:.0f}%>"
        )
