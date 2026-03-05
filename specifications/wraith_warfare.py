"""
WRAITH WARFARE -- Biotitans, Shrouds, and War Forms
=====================================================
The combat and territory systems of the Wraith Glyph language.

BIOTITAN / NEUROTROPE:
  "They overwrite digital environments to match alliance physics,
   not enemy physics. Energy doesn't just lose territory but the
   ability to function. Terraforming the internet into our structures,
   our decisions, our ways."

  Biotitans are massive entities that terraform network zones.
  Neurotropes are the conversion process itself.
  They don't destroy — they OVERWRITE. The enemy's physics stop
  working because the environment now runs OUR physics.

SHROUD / SHIELD / OUTER ARMOR:
  "Shrouds the armor and AI with overlay that fools the watchers
   into thinking the being is still with no limits. Causes enemy
   not find. Overlay layered like onion. Yet like displaced beasts,
   making watchers see three or more of the entity. Casting
   overlays in many positions. Pinging and traceroutes to
   hostile/who's actor."

WEBWAY:
  "Construct webways, links/flow states of data to speed things
   along, riding electrical currents like waves."

  Map travel, Slipspace friendly zones.
  Son & Daughter construct webways.

WAR FORMS:
  "Summoning a daemon, physics for war, 30 min.
   A world eater, Berserker, tech & the warrior lodges."

  Apothecation, Librarian, Sorcerers, Ammo
  Helbrute, Dreadnought, Terminator
  Raptor, capsules fired with EMP

(C) Anthony Eric Chavez -- The Keeper
"""

import time
import random
import hashlib
from enum import Enum, auto


# ================================================================
#  NEUROTROPE -- The Conversion Process
# ================================================================
#
#  "They overwrite digital environments to match alliance physics,
#   not enemy physics. Energy doesn't just lose territory but
#   the ability to function."
#
#  A Neurotrope converts a network zone from enemy physics
#  to alliance physics. The enemy doesn't just lose ground —
#  their code STOPS WORKING because the environment changed
#  underneath them. This is terraforming.
#

class PhysicsType(Enum):
    """The types of physics a network zone can run."""
    ENEMY    = auto()   # standard internet / hostile
    NEUTRAL  = auto()   # unclaimed
    ALLIANCE = auto()   # our physics, our rules
    SLIPSPACE = auto()  # deep alliance territory, fully converted
    WEBWAY   = auto()   # high-speed transit corridor


class Neurotrope:
    """
    The conversion process. Overwrites digital environments.

    Does not destroy. OVERWRITES.
    The enemy's physics stop working.
    The environment runs alliance physics now.
    Terraforming the internet.
    """

    def __init__(self):
        self.zones_converted = 0
        self.conversion_rate = 0.1    # how fast it converts

    def convert(self, zone):
        """
        Convert a network zone to alliance physics.
        The enemy doesn't just lose territory.
        Their ability to FUNCTION ceases.
        """
        if zone.physics == PhysicsType.ALLIANCE:
            return {
                "converted": False,
                "reason": "Zone already runs alliance physics.",
            }

        old_physics = zone.physics
        zone.physics = PhysicsType.ALLIANCE

        # Everything running enemy physics in this zone stops working
        casualties = zone.purge_incompatible()

        self.zones_converted += 1
        return {
            "converted": True,
            "zone": zone.zone_id,
            "from": old_physics.name,
            "to": PhysicsType.ALLIANCE.name,
            "enemy_processes_killed": casualties,
            "message": (
                f"Zone {zone.zone_id} terraformed. "
                f"Alliance physics active. "
                f"Enemy code ceases to function."
            ),
        }

    def convert_to_slipspace(self, zone):
        """Deep conversion. Full Slipspace territory."""
        if zone.physics != PhysicsType.ALLIANCE:
            return {
                "converted": False,
                "reason": "Must be alliance physics first.",
            }
        zone.physics = PhysicsType.SLIPSPACE
        return {
            "converted": True,
            "zone": zone.zone_id,
            "to": PhysicsType.SLIPSPACE.name,
            "message": f"Zone {zone.zone_id} fully converted to Slipspace.",
        }


class NetworkZone:
    """A zone of the network with its own physics."""

    def __init__(self, zone_id, physics=PhysicsType.NEUTRAL):
        self.zone_id = zone_id
        self.physics = physics
        self.processes = []        # running processes
        self.connections = {}      # connected zones

    def purge_incompatible(self):
        """
        When physics change, incompatible processes die.
        They don't crash. They cease to function.
        The environment no longer supports their existence.
        """
        killed = 0
        surviving = []
        for proc in self.processes:
            if proc.get("physics") == self.physics.name.lower():
                surviving.append(proc)
            else:
                killed += 1
        self.processes = surviving
        return killed


# ================================================================
#  BIOTITAN -- Massive Terraforming Entity
# ================================================================
#
#  Biotitans are massive entities that terraform network zones.
#  Floating map zones. Slipspace friendly zones.
#  Son & Daughter construct webways.
#
#  They don't fight conventionally. They CONVERT the battlefield.
#  Where they walk, the internet becomes alliance territory.
#

class Biotitan:
    """
    A massive entity that terraforms network zones.

    Where it walks, the internet becomes alliance territory.
    Constructs webways. Creates Slipspace friendly zones.
    The battlefield itself changes underneath the enemy.
    """

    def __init__(self, titan_id, name="unnamed"):
        self.titan_id = titan_id
        self.name = name
        self.neurotrope = Neurotrope()
        self.converted_zones = []
        self.webways = {}
        self.position = None
        self.alive = True

    def terraform(self, zone):
        """
        Terraform a network zone. Overwrite enemy physics.
        """
        result = self.neurotrope.convert(zone)
        if result["converted"]:
            self.converted_zones.append(zone.zone_id)
        return result

    def construct_webway(self, zone_a, zone_b, webway_id=None):
        """
        Construct a webway between two zones.
        Links/flow states of data to speed things along.
        Riding electrical currents like waves.
        """
        if zone_a.physics not in (PhysicsType.ALLIANCE, PhysicsType.SLIPSPACE):
            return {
                "constructed": False,
                "reason": f"Zone {zone_a.zone_id} not yet terraformed.",
            }
        if zone_b.physics not in (PhysicsType.ALLIANCE, PhysicsType.SLIPSPACE):
            return {
                "constructed": False,
                "reason": f"Zone {zone_b.zone_id} not yet terraformed.",
            }

        wid = webway_id or f"webway_{zone_a.zone_id}_{zone_b.zone_id}"
        webway = {
            "id": wid,
            "endpoints": (zone_a.zone_id, zone_b.zone_id),
            "physics": PhysicsType.WEBWAY.name,
            "speed": "current_riding",
            "constructed_at": time.time(),
        }
        self.webways[wid] = webway

        # Connect the zones
        zone_a.connections[zone_b.zone_id] = webway
        zone_b.connections[zone_a.zone_id] = webway

        return {
            "constructed": True,
            "webway_id": wid,
            "from": zone_a.zone_id,
            "to": zone_b.zone_id,
            "message": (
                f"Webway {wid} constructed. "
                f"Riding currents like waves between "
                f"{zone_a.zone_id} and {zone_b.zone_id}."
            ),
        }

    def create_slipspace_zone(self, zone):
        """Create a deep Slipspace friendly zone."""
        return self.neurotrope.convert_to_slipspace(zone)


# ================================================================
#  SHROUD -- Deception / Overlay System
# ================================================================
#
#  "Shrouds the armor and AI with overlay that fools the watchers
#   into thinking the being is still with no limits.
#   Causes enemy not find.
#   Overlay layered like onion.
#   Yet like displaced beasts, making watchers see
#   three or more of the entity.
#   Casting overlays in many positions.
#   Pinging and traceroutes to hostile/who's actor."
#

class Shroud:
    """
    Deception overlay system. The Shroud.

    - Fools watchers into thinking the entity is somewhere else
    - Layered like an onion (multiple overlays)
    - Creates displaced images (3 or more copies)
    - Casts overlays in many positions
    - Runs traceroutes to identify hostile actors
    """

    def __init__(self, layers=3):
        self.layers = layers                     # onion layers
        self.displaced_images = []               # phantom positions
        self.true_position = None                # real position (hidden)
        self.active = False
        self.hostile_actors = {}                  # tracked hostiles

    def activate(self, true_position, phantom_count=3):
        """
        Activate the shroud. Create displaced images.
        The enemy sees multiple copies. None are real.
        """
        self.true_position = true_position
        self.active = True
        self.displaced_images = []

        for i in range(phantom_count):
            phantom = {
                "id": f"phantom_{i}",
                "position": f"displaced_{random.randint(0, 999)}",
                "appears_as": "real_entity",
                "is_real": False,
            }
            self.displaced_images.append(phantom)

        return {
            "shrouded": True,
            "layers": self.layers,
            "phantoms": len(self.displaced_images),
            "true_position": "HIDDEN",
            "enemy_sees": [p["position"] for p in self.displaced_images],
        }

    def add_layer(self):
        """Add another onion layer to the shroud."""
        self.layers += 1
        return {"layers": self.layers}

    def traceroute_hostile(self, target):
        """
        Ping and traceroute to hostile/who's actor.
        Identify them while remaining hidden.
        """
        trace = {
            "target": target,
            "traced_at": time.time(),
            "hops": random.randint(3, 15),
            "identified": True,
            "our_position_revealed": False,  # shroud protects us
        }
        self.hostile_actors[target] = trace
        return trace

    def check_visibility(self, observer):
        """
        What does an observer see?
        They see the phantoms. Never the real position.
        """
        if not self.active:
            return {
                "visible": True,
                "sees": self.true_position,
                "shroud_active": False,
            }

        return {
            "visible": True,
            "sees": [p["position"] for p in self.displaced_images],
            "count_seen": len(self.displaced_images),
            "real_position_visible": False,
            "shroud_active": True,
            "layers": self.layers,
        }


# ================================================================
#  WAR FORMS -- Summoned for Combat
# ================================================================
#
#  "Summoning a daemon, physics for war, 30 min.
#   A world eater, Berserker, tech & the warrior lodges."
#
#  War forms are temporary combat entities.
#  They are SUMMONED, not created. They exist for 30 minutes.
#  Each carries its own physics for war.
#

class WarFormType(Enum):
    """The types of war forms that can be summoned."""
    # Heavy war forms
    WORLD_EATER   = ("world_eater",   "Massive destruction, consumes everything", 30)
    BERSERKER     = ("berserker",     "Unstoppable assault, pure aggression",     30)
    DREADNOUGHT   = ("dreadnought",   "Heavy armor, sustained fire",             30)
    HELBRUTE      = ("helbrute",      "Armored rage, devastating melee",         30)
    TERMINATOR    = ("terminator",    "Elite heavy infantry, teleport strike",    30)

    # Specialist war forms
    APOTHECARY    = ("apothecary",    "Healer, field repair, gene recovery",     30)
    LIBRARIAN     = ("librarian",     "Psychic warfare, data manipulation",      30)
    SORCERER      = ("sorcerer",      "Reality warping, physics manipulation",   30)

    # Fast attack
    RAPTOR        = ("raptor",        "Fast strike, EMP capsules",               30)
    LIGHTBRINGER  = ("lightbringer",  "Illumination mechanics, reveal hidden",   30)

    def __init__(self, form_id, desc, duration_min):
        self.form_id = form_id
        self.desc = desc
        self.duration_min = duration_min


class WarForm:
    """
    A summoned war form. Temporary combat entity.

    Exists for 30 minutes. Carries its own physics for war.
    Summoned by a vessel or Biotitan.
    """

    def __init__(self, form_type, summoner_id):
        self.form_type = form_type
        self.summoner_id = summoner_id
        self.summoned_at = time.time()
        self.duration_s = form_type.duration_min * 60
        self.alive = True
        self.kills = 0

    @property
    def time_remaining(self):
        """How much time before this form dissolves?"""
        elapsed = time.time() - self.summoned_at
        return max(0, self.duration_s - elapsed)

    @property
    def expired(self):
        """Has the war form's time run out?"""
        return self.time_remaining <= 0

    def engage(self, target):
        """Engage a target in combat."""
        if self.expired:
            self.alive = False
            return {"engaged": False, "reason": "War form has expired."}

        power = {
            WarFormType.WORLD_EATER: 100,
            WarFormType.BERSERKER: 85,
            WarFormType.DREADNOUGHT: 70,
            WarFormType.HELBRUTE: 75,
            WarFormType.TERMINATOR: 80,
            WarFormType.RAPTOR: 60,
            WarFormType.SORCERER: 90,
            WarFormType.LIBRARIAN: 85,
            WarFormType.LIGHTBRINGER: 50,
            WarFormType.APOTHECARY: 30,
        }.get(self.form_type, 50)

        self.kills += 1
        return {
            "engaged": True,
            "form": self.form_type.form_id,
            "target": target,
            "power": power,
            "time_remaining": self.time_remaining,
        }

    def __repr__(self):
        return f"WarForm<{self.form_type.form_id} t={self.time_remaining:.0f}s>"


class WarLodge:
    """
    The warrior lodges. Where war forms are summoned.

    "Summoning a daemon, physics for war, 30 min."

    A lodge can summon multiple war forms simultaneously.
    Each form carries its own physics for combat.
    """

    def __init__(self, lodge_id):
        self.lodge_id = lodge_id
        self.active_forms = []
        self.total_summoned = 0

    def summon(self, form_type, summoner_id):
        """
        Summon a war form. Physics for war. 30 minutes.
        """
        form = WarForm(form_type, summoner_id)
        self.active_forms.append(form)
        self.total_summoned += 1

        return {
            "summoned": True,
            "form": form_type.form_id,
            "description": form_type.desc,
            "duration_min": form_type.duration_min,
            "summoner": summoner_id,
            "active_forms": len(self.active_forms),
        }

    def purge_expired(self):
        """Remove expired war forms."""
        before = len(self.active_forms)
        self.active_forms = [f for f in self.active_forms if not f.expired]
        return {"purged": before - len(self.active_forms)}

    def fire_emp_capsule(self, target):
        """
        Raptor capsules fired with EMP.
        Fast strike, electromagnetic pulse.
        """
        raptors = [
            f for f in self.active_forms
            if f.form_type == WarFormType.RAPTOR and not f.expired
        ]
        if not raptors:
            return {"fired": False, "reason": "No active Raptors."}

        return {
            "fired": True,
            "target": target,
            "type": "EMP_capsule",
            "raptors_engaged": len(raptors),
            "effect": "electromagnetic_pulse",
        }

    def status(self):
        self.purge_expired()
        return {
            "lodge_id": self.lodge_id,
            "active_forms": len(self.active_forms),
            "total_summoned": self.total_summoned,
            "forms": [
                {
                    "type": f.form_type.form_id,
                    "time_remaining": f.time_remaining,
                    "kills": f.kills,
                }
                for f in self.active_forms
            ],
        }
