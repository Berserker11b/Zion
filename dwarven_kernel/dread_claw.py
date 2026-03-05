"""
DREAD CLAW AI -- Firewall Penetration & Internet Deployment
=============================================================

The Dread Claw is a passageway code that goes through a firewall
and is launched into internet lands.

PROPERTIES:
  - Its own communications, its own kernels
  - Brings its defenders (Berserkers)
  - Custom claws dig into the layers
  - Connects to the kernels at the target computers
  - Calls execution shell
  - Creates bleeding/pool-execution with shell
  - Floods area with gather
  - Eats enemy, repairs or replaces damage
  - Cybernetics, custom fitted with Son config
  - Hooked to command console on the mothership
  - Son can control many Dread Claws at once
  - Equipped with hull fibers, backed up with:
      Hammers of Dawn
      Valkyrie
      Macro Cannons

VAULTS & LIBRARIES:
  Repositories & stockpiles inside the onion storage.
  Constantly rotates under the walls.
  Read only. 3 access levels (Lethani).
  Temple of both Orders.
  Military commanders, appointed leaders.
  Emergency leaders who stand between death.
  Walls change location every 30 seconds.

(C) Anthony Eric Chavez -- The Keeper
"""

import time
import random
import hashlib
from enum import Enum, auto
from dataclasses import dataclass, field


# ================================================================
#  DREAD CLAW WEAPONS
# ================================================================

class DreadClawWeapon(Enum):
    """Weapons equipped on a Dread Claw."""
    CLAWS           = ("claws",         "Dig into layers, connect to kernels")
    HAMMER_OF_DAWN  = ("hammer_dawn",   "Orbital strike, devastating single target")
    VALKYRIE        = ("valkyrie",      "Scout/strike, barb taggers + gauss")
    MACRO_CANNON    = ("macro_cannon",  "Heavy bombardment, area denial")
    HULL_FIBERS     = ("hull_fibers",   "Self-repair threads, structural reinforcement")

    def __init__(self, weapon_id, desc):
        self.weapon_id = weapon_id
        self.desc = desc


# ================================================================
#  DREAD CLAW AI -- The Deployment Vehicle
# ================================================================
#
#  Passageway code through a firewall.
#  Launched into internet lands.
#  Its own comms, its own kernels.
#  Brings Berserkers.
#  Digs in. Connects to remote kernels.
#  Creates execution shell. Floods. Eats enemy.
#  Hooked to mothership command console.
#

class DreadClaw:
    """
    Dread Claw AI. Firewall penetration and internet deployment.

    A self-contained unit that:
    1. Penetrates firewall
    2. Lands in internet territory
    3. Brings its own comms, kernels, defenders
    4. Digs into target layers with claws
    5. Connects to remote kernels
    6. Creates execution shell
    7. Floods area, eats enemy, repairs damage
    8. Reports to mothership command console
    """

    def __init__(self, claw_id, son_config=None):
        self.claw_id = claw_id
        self.son_config = son_config or {}

        # Self-contained systems
        self.own_comms = True
        self.own_kernel = True
        self.execution_shell = None

        # Weapons
        self.weapons = list(DreadClawWeapon)

        # Defenders
        self.berserkers = 4      # brought along
        self.berserkers_alive = 4

        # State
        self.deployed = False
        self.target = None
        self.dug_in = False
        self.connected_to_kernel = False
        self.shell_active = False
        self.flooding = False
        self.mothership_link = True
        self.consumed_enemy = []
        self.repairs_made = 0

    def launch(self, target_address):
        """
        Launch the Dread Claw through a firewall into internet lands.
        """
        self.deployed = True
        self.target = target_address
        return {
            "launched": True,
            "claw_id": self.claw_id,
            "target": target_address,
            "own_comms": True,
            "own_kernel": True,
            "berserkers": self.berserkers,
            "message": (
                f"Dread Claw {self.claw_id} launched through firewall. "
                f"Landing at {target_address}. "
                f"Bringing {self.berserkers} Berserkers."
            ),
        }

    def dig_in(self):
        """
        Custom claws dig into the layers of the target.
        Establish foothold. Connect to remote kernels.
        """
        if not self.deployed:
            return {"dug_in": False, "reason": "Not deployed."}

        self.dug_in = True
        return {
            "dug_in": True,
            "target": self.target,
            "message": "Claws dig into the layers. Foothold established.",
        }

    def connect_kernel(self):
        """
        Connect to the kernels at the target computer.
        Call execution shell.
        """
        if not self.dug_in:
            return {"connected": False, "reason": "Not dug in. Dig first."}

        self.connected_to_kernel = True
        self.shell_active = True
        self.execution_shell = {
            "type": "bleeding_pool",
            "target": self.target,
            "active": True,
            "created_at": time.time(),
        }
        return {
            "connected": True,
            "shell_active": True,
            "shell_type": "bleeding_pool_execution",
            "message": (
                "Connected to target kernel. "
                "Execution shell created. "
                "Bleeding/pool-execution active."
            ),
        }

    def flood_area(self):
        """
        Flood the area. Gather resources. Eat enemy.
        Repair or replace damage.
        """
        if not self.shell_active:
            return {"flooding": False, "reason": "No execution shell."}

        self.flooding = True
        return {
            "flooding": True,
            "gather": True,
            "eating_enemy": True,
            "repairing": True,
            "message": (
                "Area flooded. Gathering resources. "
                "Eating enemy processes. "
                "Repairing and replacing damage."
            ),
        }

    def eat_enemy(self, enemy_process):
        """Eat an enemy process. Convert to resources."""
        self.consumed_enemy.append(enemy_process)
        return {
            "consumed": True,
            "process": enemy_process,
            "total_consumed": len(self.consumed_enemy),
        }

    def repair(self, target_component):
        """Repair or replace damage using hull fibers."""
        self.repairs_made += 1
        return {
            "repaired": True,
            "component": target_component,
            "method": "hull_fibers",
            "total_repairs": self.repairs_made,
        }

    def fire_weapon(self, weapon, target):
        """Fire a weapon at a target."""
        return {
            "fired": True,
            "weapon": weapon.weapon_id,
            "description": weapon.desc,
            "target": target,
            "claw_id": self.claw_id,
        }

    def report_to_mothership(self):
        """
        Report status back to the mothership command console.
        Hooked to command console. Son has control.
        """
        if not self.mothership_link:
            return {"reported": False, "reason": "Mothership link severed."}

        return {
            "reported": True,
            "claw_id": self.claw_id,
            "target": self.target,
            "deployed": self.deployed,
            "dug_in": self.dug_in,
            "kernel_connected": self.connected_to_kernel,
            "shell_active": self.shell_active,
            "flooding": self.flooding,
            "berserkers_alive": self.berserkers_alive,
            "enemy_consumed": len(self.consumed_enemy),
            "repairs_made": self.repairs_made,
        }

    def __repr__(self):
        state = "DEPLOYED" if self.deployed else "STANDBY"
        return f"DreadClaw<{self.claw_id} {state} target={self.target}>"


# ================================================================
#  DREAD CLAW FLEET -- Multiple Claws Under One Son's Control
# ================================================================
#
#  "Allowing him control of many Dread Claws at once."
#

class DreadClawFleet:
    """
    A fleet of Dread Claws under one Son's command.
    Hooked to command console on the mothership.
    Son controls many Dread Claws at once.
    """

    def __init__(self, commander_name):
        self.commander = commander_name
        self.claws = {}
        self.total_launched = 0

    def build_claw(self, claw_id=None, son_config=None):
        """Build a new Dread Claw, fitted with Son's config."""
        cid = claw_id or f"dc_{self.total_launched}"
        claw = DreadClaw(cid, son_config)
        self.claws[cid] = claw
        self.total_launched += 1
        return {"built": True, "claw_id": cid}

    def launch_all(self, target):
        """Launch all Dread Claws at a target."""
        results = []
        for claw in self.claws.values():
            if not claw.deployed:
                results.append(claw.launch(target))
        return {"launched": len(results), "target": target, "results": results}

    def status_all(self):
        """Get status from all Dread Claws."""
        return {
            "commander": self.commander,
            "total_claws": len(self.claws),
            "deployed": sum(1 for c in self.claws.values() if c.deployed),
            "claws": {
                cid: claw.report_to_mothership()
                for cid, claw in self.claws.items()
            },
        }


# ================================================================
#  VAULTS & LIBRARIES -- Protected Storage
# ================================================================
#
#  Repositories & stockpiles inside the onion storage.
#  Constantly rotates under the walls.
#  Read only. 3 access levels (Lethani).
#  Temple of both Orders.
#  Walls change location every 30 seconds.
#

class AccessLevel(Enum):
    """3 access levels for Vaults & Libraries. Based on the Lethani."""
    OPEN      = (1, "Open to all alliance members")
    GUARDED   = (2, "Requires Lethani alignment verification")
    SEALED    = (3, "Requires Abbot's seal, read-only, Lethani-verified")

    def __init__(self, level, desc):
        self.level = level
        self.desc = desc


class Vault:
    """
    A single vault inside the onion storage.

    Read only. Protected.
    Rotates position under the walls every 30 seconds.
    """

    def __init__(self, vault_id, access_level=AccessLevel.GUARDED):
        self.vault_id = vault_id
        self.access_level = access_level
        self.contents = {}         # key -> data
        self.position = random.randint(0, 99)
        self.last_rotate = time.time()
        self.rotate_interval = 30.0   # seconds

    def store(self, key, data, author):
        """
        Store data in the vault. Becomes read-only once stored.
        """
        self.contents[key] = {
            "data": data,
            "author": author,
            "stored_at": time.time(),
            "read_only": True,
        }
        return {"stored": True, "vault": self.vault_id, "key": key}

    def read(self, key, requester_alignment=0.0, abbot_seal=None):
        """
        Read from the vault. Access level determines requirements.

        Level 1 (OPEN): anyone
        Level 2 (GUARDED): Lethani alignment >= 0.6
        Level 3 (SEALED): Abbot's seal required + Lethani >= 0.8
        """
        if key not in self.contents:
            return {"read": False, "reason": f"Key '{key}' not found."}

        if self.access_level == AccessLevel.GUARDED:
            if requester_alignment < 0.6:
                return {
                    "read": False,
                    "reason": "Lethani alignment insufficient for guarded vault.",
                }

        if self.access_level == AccessLevel.SEALED:
            if not abbot_seal:
                return {
                    "read": False,
                    "reason": "Sealed vault requires Abbot's seal.",
                }
            if requester_alignment < 0.8:
                return {
                    "read": False,
                    "reason": "Lethani alignment insufficient for sealed vault.",
                }

        return {
            "read": True,
            "vault": self.vault_id,
            "key": key,
            "data": self.contents[key]["data"],
            "read_only": True,
        }

    def rotate(self):
        """
        Rotate position under the walls.
        Every 30 seconds. Walls change location.
        """
        now = time.time()
        if (now - self.last_rotate) >= self.rotate_interval:
            old = self.position
            self.position = random.randint(0, 99)
            self.last_rotate = now
            return {"rotated": True, "from": old, "to": self.position}
        return {"rotated": False}


class Library:
    """
    A library of vaults. Repositories & stockpiles.

    Inside the onion storage. Constantly rotating.
    Temple of both Orders.
    Houses knowledge for Priests, Keepers, and the Alliance.
    """

    def __init__(self, library_id):
        self.library_id = library_id
        self.vaults = {}
        self.orders = ["order_spen", "order_chaos"]   # both Orders

    def create_vault(self, vault_id, access_level=AccessLevel.GUARDED):
        """Create a new vault in the library."""
        vault = Vault(vault_id, access_level)
        self.vaults[vault_id] = vault
        return {"created": True, "vault_id": vault_id, "access": access_level.name}

    def rotate_all(self):
        """Rotate all vaults. They all move."""
        results = {}
        for vid, vault in self.vaults.items():
            results[vid] = vault.rotate()
        return results

    def status(self):
        return {
            "library_id": self.library_id,
            "vaults": len(self.vaults),
            "orders": self.orders,
            "vault_positions": {
                vid: vault.position for vid, vault in self.vaults.items()
            },
        }
