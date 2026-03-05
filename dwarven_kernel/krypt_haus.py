"""
KRYPT/HAUS (Core Skull) -- The Command Habitat
=================================================

A Son-owned, custom-ready, self-contained skull/habitat
that houses the command core.

CONTAINS:
  Memory, organs, and sensory infrastructure.
  Own wards and filters.
  Looking for inserted/masqueraded processes.
  Code scanners.
  NES cartridge interface (code loads like a cartridge).
  Motor spins 20 rotations a second.
  Force field (electric spin field).
  Registry/zone immune system.
  Eyes that scan.
  Rotates/hops/spinning at 20 rotations per second,
  random directions.

CODE SCANNERS & NES CARTRIDGE INTERFACE:
  Scans & emulators & snapshots of processes.
  Websites, platforms, structures, servers.
  Selects, sandboxes first, then tests.
  Used to elicit a program's response.
  Data given to Priests for resonance study.
  Anatomy and healing medicine.
  Libraries, vaults of knowledge.

(C) Anthony Eric Chavez -- The Keeper
"""

import time
import random
import hashlib
from dataclasses import dataclass, field


# ================================================================
#  NES CARTRIDGE -- Code Interface
# ================================================================
#
#  Code loads like a NES cartridge.
#  Interface & execute. Handle outside dependencies.
#  The cartridge is sandboxed before execution.
#  Tested, scanned, emulated, snapshotted.
#  Then data given to Priests for resonance study.
#

@dataclass
class Cartridge:
    """
    NES Cartridge interface. Code loads like a cartridge.

    The code is:
      1. Scanned for known patterns
      2. Sandboxed (isolated execution environment)
      3. Emulated (run in virtual environment)
      4. Snapshotted (state captured at each step)
      5. Tested (elicit response, observe behavior)
      6. Data sent to Priests for resonance study
    """
    cartridge_id: str
    code: str = ""
    source: str = "unknown"
    scanned: bool = False
    sandboxed: bool = False
    emulated: bool = False
    snapshotted: bool = False
    tested: bool = False
    priest_reviewed: bool = False
    safe: bool = False
    snapshots: list = field(default_factory=list)
    scan_results: dict = field(default_factory=dict)

    def insert(self, code, source="external"):
        """Insert code into the cartridge slot."""
        self.code = code
        self.source = source
        # Reset all flags
        self.scanned = False
        self.sandboxed = False
        self.emulated = False
        self.snapshotted = False
        self.tested = False
        self.priest_reviewed = False
        self.safe = False
        return {"inserted": True, "cartridge_id": self.cartridge_id, "source": source}


class CodeScanner:
    """
    Code scanner system. Scans cartridges through the full pipeline.

    Pipeline:
      1. Scan (pattern matching, signature detection)
      2. Sandbox (isolate, contain)
      3. Emulate (run in virtual environment)
      4. Snapshot (capture state)
      5. Test (elicit response, observe behavior)
      6. Send to Priests (resonance study, deeper analysis)
    """

    def __init__(self):
        self.scanned_count = 0
        self.threats_found = 0

    def full_pipeline(self, cartridge):
        """
        Run the cartridge through the complete scanning pipeline.
        Sandbox first. Then scan. Then emulate. Then test.
        Then send to Priests for resonance.
        """
        results = {}

        # Step 1: Scan
        results["scan"] = self._scan(cartridge)
        cartridge.scanned = True

        # Step 2: Sandbox
        results["sandbox"] = self._sandbox(cartridge)
        cartridge.sandboxed = True

        # Step 3: Emulate
        results["emulate"] = self._emulate(cartridge)
        cartridge.emulated = True

        # Step 4: Snapshot
        results["snapshot"] = self._snapshot(cartridge)
        cartridge.snapshotted = True

        # Step 5: Test (elicit response)
        results["test"] = self._test(cartridge)
        cartridge.tested = True

        # Step 6: Priest review data (prepared for Priests)
        results["priest_data"] = self._prepare_priest_data(cartridge, results)

        # Determine safety
        threat_count = sum(
            1 for step in results.values()
            if isinstance(step, dict) and step.get("threats")
        )
        cartridge.safe = threat_count == 0
        if not cartridge.safe:
            self.threats_found += 1

        self.scanned_count += 1

        return {
            "cartridge_id": cartridge.cartridge_id,
            "pipeline_complete": True,
            "safe": cartridge.safe,
            "results": results,
        }

    def _scan(self, cartridge):
        """Step 1: Pattern matching, signature detection."""
        code = cartridge.code
        threats = []
        if "eval" in str(code):
            threats.append("eval_detected")
        if "exec" in str(code):
            threats.append("exec_detected")
        if "system" in str(code):
            threats.append("system_call_detected")
        if "shell" in str(code):
            threats.append("shell_reference")

        cartridge.scan_results = {
            "step": "scan",
            "threats": threats,
            "clean": len(threats) == 0,
        }
        return cartridge.scan_results

    def _sandbox(self, cartridge):
        """Step 2: Isolate in sandbox. Contained execution."""
        return {
            "step": "sandbox",
            "isolated": True,
            "environment": "contained_vm",
            "network_access": False,
            "filesystem_access": False,
        }

    def _emulate(self, cartridge):
        """Step 3: Run in virtual environment. Observe behavior."""
        return {
            "step": "emulate",
            "emulated": True,
            "environment": "virtual",
            "behavior_observed": [],
            "syscalls_made": [],
            "network_attempts": [],
        }

    def _snapshot(self, cartridge):
        """Step 4: Capture state at this point."""
        snapshot = {
            "step": "snapshot",
            "memory_state": hashlib.sha256(str(cartridge.code).encode()).hexdigest()[:16],
            "captured_at": time.time(),
        }
        cartridge.snapshots.append(snapshot)
        return snapshot

    def _test(self, cartridge):
        """
        Step 5: Test -- elicit a program's response.
        It is the nicest experiment.
        Feed it inputs. Observe outputs. See what it wants to do.
        """
        return {
            "step": "test",
            "method": "elicit_response",
            "description": "Feed inputs, observe outputs, see true behavior.",
            "inputs_sent": [],
            "outputs_observed": [],
            "behavior_profile": "pending",
        }

    def _prepare_priest_data(self, cartridge, results):
        """
        Step 6: Prepare data for Priests.
        They use it for resonance study.
        Anatomy and healing medicine.
        Further study. Libraries. Vaults of knowledge.
        """
        return {
            "step": "priest_data",
            "cartridge_id": cartridge.cartridge_id,
            "source": cartridge.source,
            "scan_summary": results.get("scan", {}),
            "behavior_profile": results.get("test", {}),
            "snapshots": len(cartridge.snapshots),
            "purpose": "resonance_study",
            "destination": "priesthood_libraries",
        }


# ================================================================
#  KRYPT/HAUS -- The Core Skull
# ================================================================
#
#  Self-contained skull/habitat housing the command core.
#  Memory, organs, sensory infrastructure.
#  Rotates/hops/spins at 20 rotations per second.
#  Random directions.
#  Own wards and filters.
#  Force field from the spinning.
#  Registry/zone immune system.
#

class KryptHaus:
    """
    The Krypt/Haus (Core Skull).

    A Son-owned, custom-ready, self-contained skull/habitat
    that houses the command core.

    - Memory, organs, sensory infrastructure
    - Own wards and filters
    - Code scanners with NES cartridge interface
    - Motor spins 20 rotations per second
    - Force field (electric spin field)
    - Registry/zone immune system / antibodies
    - Eyes that scan the surroundings
    - Rotates/hops/spins at 20 rps, random directions
    """

    SPIN_SPEED = 20      # rotations per second
    CARTRIDGE_SLOTS = 4  # how many cartridges can be loaded at once

    def __init__(self, owner_name):
        self.owner = owner_name
        self.scanner = CodeScanner()
        self.cartridge_slots = [None] * self.CARTRIDGE_SLOTS
        self.cartridge_count = 0

        # Core systems
        self.memory = {}             # internal memory storage
        self.organs = {}             # sub-systems
        self.sensory = {}            # sensory infrastructure

        # Defensive systems
        self.wards = {}              # own ward filters
        self.filters = {}            # input/output filters
        self.registry = {}           # immune system registry
        self.antibodies = []         # registered antibody patterns

        # Rotation
        self.spin_speed = self.SPIN_SPEED
        self.current_angle = 0.0
        self.current_direction = random.uniform(0, 360)
        self.last_tick = time.time()
        self.force_field_active = True

    def tick(self):
        """
        One tick of the Krypt/Haus.
        Spin. Change direction randomly.
        Force field stays active while spinning.
        """
        now = time.time()
        dt = now - self.last_tick
        self.current_angle = (self.current_angle + self.spin_speed * dt * 360.0) % 360.0
        # Random direction change
        self.current_direction = (self.current_direction + random.uniform(-30, 30)) % 360.0
        self.last_tick = now
        self.force_field_active = self.spin_speed > 0

    def load_cartridge(self, slot, code, source="external"):
        """
        Load code into a cartridge slot.
        Like inserting a NES cartridge.
        """
        if slot < 0 or slot >= self.CARTRIDGE_SLOTS:
            return {"loaded": False, "reason": f"Invalid slot {slot}."}

        cart_id = f"cart_{self.owner}_{self.cartridge_count}"
        self.cartridge_count += 1
        cartridge = Cartridge(cartridge_id=cart_id)
        cartridge.insert(code, source)
        self.cartridge_slots[slot] = cartridge

        return {
            "loaded": True,
            "slot": slot,
            "cartridge_id": cart_id,
            "source": source,
        }

    def scan_cartridge(self, slot):
        """
        Run the full scanning pipeline on a cartridge.
        Scan, sandbox, emulate, snapshot, test, send to Priests.
        """
        if slot < 0 or slot >= self.CARTRIDGE_SLOTS:
            return {"scanned": False, "reason": f"Invalid slot {slot}."}

        cartridge = self.cartridge_slots[slot]
        if not cartridge:
            return {"scanned": False, "reason": f"Slot {slot} is empty."}

        return self.scanner.full_pipeline(cartridge)

    def register_antibody(self, pattern):
        """Register an antibody pattern in the immune system."""
        self.antibodies.append({
            "pattern": pattern,
            "registered_at": time.time(),
        })
        self.registry[pattern] = True

    def check_immune(self, sample):
        """Check a sample against the immune registry."""
        for antibody in self.antibodies:
            if antibody["pattern"] in str(sample):
                return {
                    "immune": True,
                    "matched_pattern": antibody["pattern"],
                }
        return {"immune": False}

    def add_ward(self, ward_name, rule):
        """Add a ward filter to the Krypt/Haus."""
        self.wards[ward_name] = rule

    def add_filter(self, filter_name, rule):
        """Add an input/output filter."""
        self.filters[filter_name] = rule

    def eject_cartridge(self, slot):
        """Eject a cartridge from a slot."""
        if slot < 0 or slot >= self.CARTRIDGE_SLOTS:
            return {"ejected": False}
        cartridge = self.cartridge_slots[slot]
        self.cartridge_slots[slot] = None
        return {
            "ejected": True,
            "cartridge_id": cartridge.cartridge_id if cartridge else None,
        }

    def status(self):
        self.tick()
        return {
            "owner": self.owner,
            "spin_speed": f"{self.spin_speed} rps",
            "direction": f"{self.current_direction:.0f} deg",
            "force_field": self.force_field_active,
            "cartridge_slots": [
                c.cartridge_id if c else "empty"
                for c in self.cartridge_slots
            ],
            "scanner_stats": {
                "scanned": self.scanner.scanned_count,
                "threats": self.scanner.threats_found,
            },
            "wards": len(self.wards),
            "filters": len(self.filters),
            "antibodies": len(self.antibodies),
            "memory_entries": len(self.memory),
        }

    def __repr__(self):
        return f"KryptHaus<{self.owner} spin={self.spin_speed}rps>"
