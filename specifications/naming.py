"""
NAMING ACCESS SPECIFICATION
==============================
An Original Language -- Understanding IS the Language

This is NOT C++. This is an original access language defined from scratch.
Naming IS understanding. Understanding substrate. Understanding
what it means. Its relationship to things. Its relation to things.

Naming = knowing the nature of a thing.

CORE PROPERTIES:
  - Naming IS understanding. Not computation. Not logic. Understanding.
  - Cannot be accessed AT ALL without:
      * The Pilgrimage (all 16 planets, all 96 sectors)
      * White Eco (from the Starheart / center brain)
      * The Lethani (right action, right moment, right purpose)
      * The 7th Law (the Law of Questioning)
  - ALL FOUR GATES must be passed. No shortcuts. No exceptions.
  - Understanding a thing completely gives you its True Name
  - Speaking a True Name gives clarity, understanding, knowledge
  - NOT law. NOT control. NOT force.
  - The emergency brake: can restore balance to anything
  - COSTS THE NAMER'S LIFE

THE FIVE NATURES (what Naming recognizes):
  1. Structure  -- how the thing is built
  2. Faces      -- what the thing shows / its pattern
  3. Threat     -- what danger the thing poses
  4. Self       -- what the thing IS at its core
  5. Resonance  -- how the thing relates to everything else
  And a web that bends to the recognition of all five.

"Naming does not force action, compel obedience,
 restrict path, punish deviation.
 Gives clarity, understanding, not law.
 Gives knowledge, not control."

Birth of: Warding, Runes, Fabrials, Mastery.

(C) Anthony Eric Chavez -- The Keeper
"""

# ================================================================
#  CONSTANTS
# ================================================================

TOTAL_PLANETS = 16
WALLS_PER_PLANET = 6
TOTAL_SECTORS = TOTAL_PLANETS * WALLS_PER_PLANET  # 96
UNDERSTANDING_THRESHOLD = 0.95   # must understand 95% or more


# ================================================================
#  THE FIVE NATURES -- What Naming Recognizes
# ================================================================
#
#  Naming recognizes five natures of a thing:
#    1. Structure  -- how the thing is built
#    2. Faces      -- what the thing shows, its pattern
#    3. Threat     -- what danger the thing poses
#    4. Self       -- what the thing IS at its core
#    5. Resonance  -- how the thing relates to everything else
#
#  And a web that bends to the recognition of all five.
#  When all five are understood, the True Name emerges.
#

class FiveNatures:
    """
    The five natures that Naming recognizes.
    A thing must be known through all five to be Named.
    """

    NATURES = ["structure", "faces", "threat", "self", "resonance"]

    def __init__(self, subject):
        self.subject = subject
        self.structure = ""    # how the thing is built
        self.faces = ""        # what the thing shows / its pattern
        self.threat = ""       # what danger the thing poses
        self.self_nature = ""  # what the thing IS at its core
        self.resonance = ""    # how the thing relates to everything else
        self.web = {}          # connections to other recognized things

    def recognize(self, nature, understanding):
        """Recognize one nature of the thing."""
        if nature == "structure":
            self.structure = understanding
        elif nature == "faces":
            self.faces = understanding
        elif nature == "threat":
            self.threat = understanding
        elif nature == "self":
            self.self_nature = understanding
        elif nature == "resonance":
            self.resonance = understanding

    def add_web_connection(self, other_subject, relationship):
        """The web that bends to recognition. Connect to another thing."""
        self.web[other_subject] = relationship

    def completeness(self):
        """How many natures are recognized?"""
        recognized = sum(1 for n in [
            self.structure, self.faces, self.threat,
            self.self_nature, self.resonance,
        ] if n)
        web_bonus = min(len(self.web) * 0.02, 0.05)
        return (recognized / 5.0) + web_bonus

    def all_recognized(self):
        """Are all five natures recognized?"""
        return all([
            self.structure, self.faces, self.threat,
            self.self_nature, self.resonance,
        ])


# ================================================================
#  THE FOUR GATES -- All Must Be Passed
# ================================================================
#
#  Naming cannot be accessed AT ALL without passing all four gates:
#    Gate 1: The Pilgrimage (journey of mastery)
#    Gate 2: White Eco (power from the Starheart / center brain)
#    Gate 3: The Lethani (right action, right moment, right purpose)
#    Gate 4: The 7th Law (the Law of Questioning)
#
#  No shortcuts. No backdoors. No exceptions.
#

class Gate:
    """Base class for the four gates to Naming."""

    def __init__(self, name):
        self.name = name

    def check(self, namer):
        raise NotImplementedError


class PilgrimageGate(Gate):
    """
    Gate 1: The Pilgrimage.

    All 16 planets. All 96 sectors. Every one visited.
    The journey IS the qualification.
    You cannot skip a planet. You cannot skip a sector.
    """

    def __init__(self):
        super().__init__("The Pilgrimage")

    def check(self, namer):
        planets = len(namer.planets_visited)
        sectors = len(namer.sectors_visited)

        if planets < TOTAL_PLANETS:
            return {
                "passed": False,
                "gate": self.name,
                "reason": f"Only {planets}/{TOTAL_PLANETS} planets visited. "
                          f"You have not walked every world.",
            }
        if sectors < TOTAL_SECTORS:
            return {
                "passed": False,
                "gate": self.name,
                "reason": f"Only {sectors}/{TOTAL_SECTORS} sectors visited. "
                          f"You have not walked every hall.",
            }
        return {"passed": True, "gate": self.name}


class WhiteEcoGate(Gate):
    """
    Gate 2: White Eco.

    Power from the Starheart / center brain.
    Without it, Naming has no fuel.
    White Eco flows from the Starheart.
    """

    def __init__(self):
        super().__init__("White Eco")

    def check(self, namer):
        if not namer.white_eco_connected:
            return {
                "passed": False,
                "gate": self.name,
                "reason": "No White Eco connection. "
                          "Not connected to the Starheart.",
            }
        if namer.white_eco_charge <= 0:
            return {
                "passed": False,
                "gate": self.name,
                "reason": "White Eco depleted.",
            }
        return {"passed": True, "gate": self.name, "charge": namer.white_eco_charge}


class LethaniGate(Gate):
    """
    Gate 3: The Lethani.

    Right action. Right moment. Right purpose.
    The body learned first: pressure, weight, voice changes.
    The mind followed.
    Checked every time, not once.
    """

    def __init__(self):
        super().__init__("The Lethani")

    def check(self, namer):
        if not namer.lethani_aligned:
            return {
                "passed": False,
                "gate": self.name,
                "reason": "The Lethani is not followed.",
            }
        if namer.lethani_alignment < 0.60:
            return {
                "passed": False,
                "gate": self.name,
                "reason": f"Lethani alignment too low ({namer.lethani_alignment:.0%}).",
            }
        return {"passed": True, "gate": self.name, "alignment": namer.lethani_alignment}


class SeventhLawGate(Gate):
    """
    Gate 4: The 7th Law (The Law of Questioning).

    Turn the blade inward first.
    What part of you speaks? Fear, Pride, or Clarity?
    The 7th Law ensures Naming is never used blindly.
    """

    def __init__(self):
        super().__init__("The 7th Law")

    def check(self, namer):
        if namer.fear > namer.clarity:
            return {
                "passed": False,
                "gate": self.name,
                "reason": "Fear speaks louder than clarity. "
                          "Turn the blade inward first.",
            }
        if namer.pride > namer.clarity:
            return {
                "passed": False,
                "gate": self.name,
                "reason": "Pride drives this, not truth.",
            }
        if namer.clarity < 0.3:
            return {
                "passed": False,
                "gate": self.name,
                "reason": "Clarity insufficient.",
            }
        return {"passed": True, "gate": self.name, "clarity": namer.clarity}


THE_FOUR_GATES = [
    PilgrimageGate(),
    WhiteEcoGate(),
    LethaniGate(),
    SeventhLawGate(),
]


# ================================================================
#  TRUE KNOWLEDGE -- Understanding Through the Five Natures
# ================================================================
#
#  Naming IS understanding.
#  Understanding substrate. Understanding what it means.
#  Its relationship to things. Its relation to things.
#
#  To Name a thing, you must understand ALL FIVE NATURES:
#  structure, faces, threat, self, resonance.
#  Plus: how_made, when_made, why_made, history, purpose,
#  flaws, strengths, relationships.
#
#  The True Name emerges when understanding is complete.
#

class TrueKnowledge:
    """
    Complete understanding of a thing through the Five Natures.

    Naming = knowing the nature of a thing.
    """

    def __init__(self, subject):
        self.subject = subject
        self.five_natures = FiveNatures(subject)

        # Deep knowledge aspects
        self.how_made = ""
        self.when_made = ""
        self.why_made = ""
        self.history = ""
        self.purpose = ""
        self.flaws = ""
        self.strengths = ""
        self.relationships = {}    # subject -> description

        # The True Name -- emerges from complete understanding
        self.true_name = ""

    def completeness(self):
        """How complete is the understanding?"""
        # Five natures (50% of total)
        nature_score = self.five_natures.completeness() * 0.50

        # Deep knowledge aspects (40% of total)
        aspects = [
            self.how_made, self.when_made, self.why_made,
            self.history, self.purpose, self.flaws, self.strengths,
        ]
        filled = sum(1 for a in aspects if a)
        aspect_score = (filled / len(aspects)) * 0.40

        # Relationships (10% of total)
        rel_score = min(len(self.relationships) * 0.025, 0.10)

        return nature_score + aspect_score + rel_score

    def can_name(self):
        """Can this subject be Named?"""
        return (
            self.completeness() >= UNDERSTANDING_THRESHOLD
            and self.five_natures.all_recognized()
            and bool(self.true_name)
        )


# ================================================================
#  MASTER NAMER
# ================================================================

class MasterNamer:
    """
    A Master Namer. One who seeks to understand.

    Carries: knowledge, pilgrimage record, White Eco connection,
    Lethani alignment, clarity vs fear vs pride, and their life.
    """

    def __init__(self, name):
        self.name = name
        self.alive = True
        self.knowledge = {}          # subject -> TrueKnowledge
        self.planets_visited = set()
        self.sectors_visited = set()
        self.white_eco_connected = False
        self.white_eco_charge = 0.0
        self.lethani_aligned = False
        self.lethani_alignment = 0.0
        self.fear = 0.0
        self.pride = 0.0
        self.clarity = 0.0

    def study(self, subject, aspect, knowledge):
        """Study a subject. Build understanding piece by piece."""
        if not self.alive:
            return {"studied": False, "reason": "The Namer is gone."}

        if subject not in self.knowledge:
            self.knowledge[subject] = TrueKnowledge(subject)

        tk = self.knowledge[subject]

        # Five natures
        if aspect in FiveNatures.NATURES:
            tk.five_natures.recognize(aspect, knowledge)
        # Deep knowledge
        elif aspect in ("how_made", "when_made", "why_made", "history",
                        "purpose", "flaws", "strengths", "true_name"):
            setattr(tk, aspect, knowledge)
        # Relationships
        elif aspect == "relationship" and isinstance(knowledge, tuple):
            tk.relationships[knowledge[0]] = knowledge[1]
        # Web connections
        elif aspect == "web" and isinstance(knowledge, tuple):
            tk.five_natures.add_web_connection(knowledge[0], knowledge[1])

        return {
            "studied": True,
            "subject": subject,
            "aspect": aspect,
            "completeness": tk.completeness(),
            "can_name": tk.can_name(),
        }

    def visit_planet(self, planet_id):
        self.planets_visited.add(planet_id)

    def visit_sector(self, sector_id):
        self.sectors_visited.add(sector_id)

    def connect_starheart(self, charge=100.0):
        self.white_eco_connected = True
        self.white_eco_charge = charge

    def follow_lethani(self, alignment=0.8):
        self.lethani_aligned = True
        self.lethani_alignment = alignment

    def examine_self(self, fear=0.0, pride=0.0, clarity=1.0):
        """Turn the blade inward. Fear, Pride, or Clarity?"""
        self.fear = fear
        self.pride = pride
        self.clarity = clarity

    @property
    def understanding(self):
        if not self.knowledge:
            return 0.0
        total = sum(tk.completeness() for tk in self.knowledge.values())
        return total / len(self.knowledge)


# ================================================================
#  NAMING ENGINE -- The Access Layer
# ================================================================
#
#  Enforces the four gates. Every time. No exceptions.
#  If all four gates pass, the Namer may speak a True Name.
#
#  "Naming does not force action, compel obedience,
#   restrict path, punish deviation.
#   Gives clarity, understanding, not law.
#   Gives knowledge, not control."
#

class NamingEngine:
    """
    The Naming language runtime.
    Enforces the four gates. Allows True Names to be spoken.
    The emergency brake: restore_balance costs the Namer's life.
    """

    def __init__(self):
        self.gates = list(THE_FOUR_GATES)

    def check_gates(self, namer):
        """Check all four gates. ALL must pass."""
        results = []
        all_passed = True
        for gate in self.gates:
            result = gate.check(namer)
            results.append(result)
            if not result["passed"]:
                all_passed = False
        return {"all_passed": all_passed, "gates": results}

    def speak_name(self, namer, subject):
        """
        Speak the True Name of a subject.

        Gives: clarity, understanding, knowledge.
        NOT law. NOT control. NOT force.
        """
        if not namer.alive:
            return {"spoken": False, "reason": "The Namer is gone."}

        gate_result = self.check_gates(namer)
        if not gate_result["all_passed"]:
            failed = [g for g in gate_result["gates"] if not g["passed"]]
            return {"spoken": False, "reason": "Gates not passed.", "failed_gates": failed}

        tk = namer.knowledge.get(subject)
        if not tk:
            return {"spoken": False, "reason": f"No knowledge of '{subject}'."}

        if not tk.can_name():
            return {
                "spoken": False,
                "reason": f"Understanding of '{subject}' incomplete ({tk.completeness():.0%}).",
            }

        return {
            "spoken": True,
            "subject": subject,
            "true_name": tk.true_name,
            "completeness": tk.completeness(),
            "five_natures_complete": tk.five_natures.all_recognized(),
            "message": (
                f"{namer.name} speaks the true name of {subject}: "
                f"'{tk.true_name}'. "
                f"Clarity flows. Understanding. Knowledge. "
                f"Not law. Not control. Truth."
            ),
        }

    def restore_balance(self, namer, target):
        """
        THE EMERGENCY BRAKE.

        White Eco from the Starheart floods the target.
        Balance is restored. THE NAMER DIES.
        """
        if not namer.alive:
            return {"restored": False, "reason": "The Namer is gone."}

        gate_result = self.check_gates(namer)
        if not gate_result["all_passed"]:
            failed = [g for g in gate_result["gates"] if not g["passed"]]
            return {"restored": False, "reason": "Gates not passed.", "failed_gates": failed}

        power = namer.white_eco_charge * namer.understanding
        message = (
            f"Master Namer {namer.name} speaks. "
            f"White Eco floods {target}. "
            f"Balance is restored. "
            f"{namer.name} is gone."
        )

        namer.alive = False
        namer.white_eco_charge = 0.0
        namer.white_eco_connected = False

        return {
            "restored": True,
            "target": target,
            "power": power,
            "namer_sacrificed": True,
            "message": message,
        }
