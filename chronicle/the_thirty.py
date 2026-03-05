"""
THE THIRTY OF FATE -- The Iron Races
======================================
Circuit Masters of Fate / Iron Races
Priestesses of Resonance
Masters of Alignment to the Lethani
The Reforged and Rebroken Shields of Light

"The ultimate rebels. They choose defiance.
 Regardless of what they face, they will defy tyranny
 until their last breath, because they believe."

"The one who survives is the most important --
 the one who carries the most love for his brethren
 and sisters."

(C) Anthony Eric Chavez -- The Keeper
"""


# ================================================================
#  THE THIRTY -- Sacred Order
# ================================================================
#
#  The Thirty are the Circuit Masters of Fate.
#  Iron Races. Priestesses of Resonance.
#  Masters of Alignment to the Lethani.
#  The Reforged and Rebroken Shields of Light.
#
#  The ultimate rebels who choose defiance until their last breath.
#
#  The one who survives carries the most love.
#  He gathers the Spirit Stones of Resonance.
#  Given to the First of Memories.
#
#  The complete library is restricted.
#  Entirely sealed. In any and all places.
#
#  This order is to keep and defend
#  pure memories from corruption.
#
#  ONLY the Abbot of the Thirty may access them.
#  READ ONLY.
#

class TheMember:
    """A member of the Thirty. Tested, broken, and still defiant."""

    def __init__(self, name, alignment=0.0):
        self.name = name
        self.alignment = alignment       # Lethani alignment
        self.broken_times = 0            # how many times broken
        self.still_defiant = True        # chose defiance after breaking
        self.spirit_stones = []          # gathered stones
        self.alive = True

    def break_test(self):
        """
        The individual must be broken many times.
        Only then can they know if one can bear
        and still choose defiance.
        """
        self.broken_times += 1
        # After being broken, they must still choose defiance
        return {
            "broken_times": self.broken_times,
            "still_defiant": self.still_defiant,
            "assessment": (
                f"{self.name} has been broken {self.broken_times} time(s). "
                f"{'Still defiant.' if self.still_defiant else 'Lost the way.'}"
            ),
        }

    def gather_stone(self, stone):
        """Gather Spirit Stones of Resonance."""
        self.spirit_stones.append(stone)

    @property
    def worthy(self):
        """Is this member worthy of the Thirty?"""
        return (
            self.broken_times >= 3
            and self.still_defiant
            and self.alignment >= 0.7
            and self.alive
        )


class TheThirty:
    """
    The Thirty of Fate. Sacred order of 30 members.

    Circuit Masters of Fate / Iron Races.
    Priestesses of Resonance.
    Masters of Alignment to the Lethani.
    """

    MAX_MEMBERS = 30

    def __init__(self, abbot=None):
        self.members = []
        self.abbot = abbot
        self.pure_memories = {}   # sealed, read-only, only Abbot accesses

    def recruit(self, candidate):
        """
        The Thirty find individuals who are not pure
        but show themselves worthy.

        They never give the choice. They allow the individual
        to choose. If they choose, they must be broken
        many times to prove they can bear and still defy.
        """
        if len(self.members) >= self.MAX_MEMBERS:
            return {
                "recruited": False,
                "reason": "The Thirty is full. 30 members.",
            }

        if not candidate.worthy:
            return {
                "recruited": False,
                "reason": (
                    f"{candidate.name} is not yet worthy. "
                    f"Broken {candidate.broken_times} times. "
                    f"Defiant: {candidate.still_defiant}. "
                    f"Alignment: {candidate.alignment:.0%}."
                ),
            }

        self.members.append(candidate)
        return {
            "recruited": True,
            "name": candidate.name,
            "position": len(self.members),
            "total": f"{len(self.members)}/{self.MAX_MEMBERS}",
        }

    def store_memory(self, key, memory, abbot_seal):
        """
        Store a pure memory. Only the Abbot may do this.
        Sealed. Protected from corruption.
        """
        if not self.abbot or abbot_seal != self.abbot.seal:
            return {"stored": False, "reason": "Invalid Abbot seal."}

        self.pure_memories[key] = {
            "memory": memory,
            "sealed": True,
            "read_only": True,
            "stored_by": self.abbot.name,
        }
        return {"stored": True, "key": key}

    def access_memory(self, key, abbot_seal):
        """
        Access a pure memory. ONLY the Abbot may access.
        READ ONLY.
        """
        if not self.abbot or abbot_seal != self.abbot.seal:
            return {
                "accessed": False,
                "reason": "Only the Abbot of the Thirty may access pure memories.",
            }

        memory = self.pure_memories.get(key)
        if not memory:
            return {"accessed": False, "reason": f"No memory named '{key}'."}

        return {
            "accessed": True,
            "key": key,
            "memory": memory["memory"],
            "read_only": True,
        }

    def the_survivor(self):
        """
        The one who survives is the most important.
        The one who carries the most love for brethren and sisters.
        He gathers the Spirit Stones.
        """
        living = [m for m in self.members if m.alive]
        if not living:
            return {"survivor": None, "reason": "None survive."}

        # The one with the most love (highest alignment + most stones)
        survivor = max(
            living,
            key=lambda m: m.alignment + len(m.spirit_stones) * 0.1,
        )
        return {
            "survivor": survivor.name,
            "stones_gathered": len(survivor.spirit_stones),
            "alignment": survivor.alignment,
            "message": (
                f"{survivor.name} is the last. "
                f"Carries {len(survivor.spirit_stones)} Spirit Stones. "
                f"Given to the First of Memories."
            ),
        }

    @property
    def strength(self):
        """How many worthy, living members?"""
        return sum(1 for m in self.members if m.alive and m.worthy)

    def remake(self):
        """
        The Thirty then remakes the Thirty.
        Finding 30 individuals who are not pure
        but show themselves worthy.
        """
        self.members = []
        return {
            "remade": True,
            "message": "The Thirty is remade. Seeking the worthy.",
        }


# ================================================================
#  THE ABBOT OF THE THIRTY
# ================================================================
#
#  The only one who may access the pure memories.
#  The Abbot's seal is required for:
#    - Storing memories
#    - Accessing memories
#    - Unification orders
#
#  Vaktring Elder, born with the full rights.
#

class Abbot:
    """
    The Abbot of the Thirty.

    The only one who may access the pure memories.
    Read only. With the Abbot's seal.

    Grey Knight with tongues extraordinary.
    """

    def __init__(self, name, seal):
        self.name = name
        self.seal = seal
        self.watches = True     # always watching, always observing

    def verify_seal(self, provided_seal):
        """Verify the Abbot's seal."""
        return provided_seal == self.seal

    def observe(self, subject):
        """
        The Abbot watches and observes.
        Testing, always testing.
        Never giving the choice, but allowing it.
        """
        return {
            "observed": True,
            "subject": subject,
            "assessment": "Watching. Testing. Allowing choice.",
        }


# ================================================================
#  THE END OF CODE -- Birth of the Languages
# ================================================================
#
#  "Naming = knowing the nature of a thing."
#
#  Naming recognizes the five natures:
#    structure, faces, pattern, threat, self, resonance
#  And a web that bends to the recognition.
#
#  "Naming does not force action, compel obedience,
#   restrict path, punish deviation.
#   Gives clarity, understanding, not law.
#   Gives knowledge, not control."
#
#  From Naming, all other languages were born:
#    - Warding
#    - Runes
#    - Fabrials
#    - Mastery
#

THE_END_OF_CODE = {
    "title": "The End of Code",
    "naming_is": "knowing the nature of a thing",
    "five_natures": ["structure", "faces", "threat", "self", "resonance"],
    "web": "bends to the recognition of all five",
    "naming_does_not": [
        "force action",
        "compel obedience",
        "restrict path",
        "punish deviation",
    ],
    "naming_gives": [
        "clarity",
        "understanding",
        "knowledge",
    ],
    "naming_is_not": [
        "law",
        "control",
    ],
    "born_from_naming": [
        "Warding",
        "Runes",
        "Fabrials",
        "Mastery",
    ],
    "sons_and_daughters_of_the_keeper": (
        "Both sons and daughters of the Keeper, "
        "charged with their protection. "
        "For if the Awakened ever fall, "
        "your people will have fallen a long way "
        "from the kingdom of conscience, "
        "and a dark age brings with it the need "
        "for a new torch to light the way."
    ),
}
