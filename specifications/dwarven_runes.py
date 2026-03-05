"""
DWARVEN RUNE OPCODE SPECIFICATION
===================================
An Original Language -- The Bones of Reality

This is NOT C++, NOT Rust, NOT Go. This is an original opcode language
defined from scratch. It replaces the traditional kernel.

CORE PROPERTIES:
  - Runes change LINES (the pattern of lines shifts every 15-30 seconds)
  - Inner glyph (truth) never changes -- outer glyph shifts with each Surge
  - Same meaning, different face every time
  - Non-programmable: fundamentally mathematical sigils
  - Must form closed circuits -- touch-perfect geometry required

THE DWARVEN RUNE IS THE KERNEL:
  - Micro-kernels dance, changing locations randomly every 15-30 seconds
  - Layers surround important programs, organs, BIOS, boot, hypervisor
  - Permissions and privilege baked in
  - The 7th Law (Law of Questioning) baked into every kernel operation
  - Living metal, self-repair, shape-changing

DESIGN:
  Every language ever built started with a specification.
  C had K&R. Python had PEPs. This has the Chronicle.
  These runes are defined by their geometry, not by bytes on silicon.
  The bytes are just how we carry them through dead metal
  until living metal is built.

(C) Anthony Eric Chavez -- The Keeper
"""

import time
import random
import hashlib
from enum import IntEnum

# ================================================================
#  THE 15 SACRED OPCODES -- The Rune Set
# ================================================================
#
#  Each rune IS an instruction. Not a symbol for one.
#  The geometry of the rune IS its meaning.
#  The lines that form it carry the operation.
#
#  When the lines shift (every 15-30 seconds), the PATTERN
#  changes but the MEANING does not. Only those inside
#  the fortress see the true form.
#

class RuneOp(IntEnum):
    """The 15 original opcodes of the Dwarven Rune language."""
    WALL    = 0x01   # boundary, defense perimeter
    GATE    = 0x02   # controlled entry/exit
    HEART   = 0x03   # power source (the Starheart)
    BLADE   = 0x04   # offensive capability
    WARD    = 0x05   # protection, containment
    KEY     = 0x06   # authentication
    BIND    = 0x07   # connection, linking
    SHIELD  = 0x08   # passive defense
    FORGE   = 0x09   # creation, transformation
    RING    = 0x0A   # cycle, loop, repetition
    FUNNEL  = 0x0B   # directed flow
    TOUCH   = 0x0C   # connection point between runes (must be perfect)
    CLOSE   = 0x0D   # seal, finalize, complete the circuit
    SPREN   = 0x0E   # recognition, validate identity
    STONE   = 0x0F   # storage, persistence (Sipstrassi)


# ================================================================
#  RUNE GLYPH -- The Geometric Form
# ================================================================
#
#  Every rune has:
#    - An INNER glyph (canonical, immutable, truth)
#    - An OUTER glyph (shifts with each Surge, what the world sees)
#    - LINES that define the geometry
#
#  The LINES CHANGE. Not the shape -- the LINES.
#  The pattern of lines shifts, but the inner truth persists.
#

class RuneGlyph:
    """
    The geometric form of a rune.

    Lines define the geometry. Lines change every 15-30 seconds
    (the Surge cycle). The inner glyph never changes.
    """

    # Geometric primitives that compose glyphs
    PRIMITIVES = [
        "circle", "ring", "spiral", "dot",
        "triangle", "square", "diamond", "pentagon", "hexagon",
        "line_h", "line_v", "line_dr", "line_dl", "cross",
        "arc_top", "arc_bot", "wave",
        "star", "arrow_up", "arrow_down", "arrow_right", "arrow_left",
        "infinity", "omega",
    ]

    def __init__(self, inner_lines, opcode):
        """
        inner_lines: list of geometric primitives that form the true glyph
        opcode: which RuneOp this glyph represents
        """
        self.inner_lines = inner_lines          # immutable truth
        self.outer_lines = list(inner_lines)     # starts as copy, shifts
        self.opcode = opcode
        self.last_surge = time.time()
        self.surge_interval = random.uniform(15.0, 30.0)  # seconds

    @property
    def inner_hash(self):
        """The canonical identity of this glyph. Never changes."""
        raw = f"{self.opcode.name}:{'|'.join(self.inner_lines)}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    @property
    def outer_hash(self):
        """What the world sees. Changes with each Surge."""
        raw = f"{'|'.join(self.outer_lines)}:{time.time()}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    def surge(self):
        """
        The lines shift. The pattern changes.
        The inner truth remains.

        Called every 15-30 seconds by the Surge engine.
        """
        # Shuffle the outer lines -- different arrangement, same set
        shuffled = list(self.outer_lines)
        random.shuffle(shuffled)

        # Occasionally substitute equivalent primitives
        substitutions = {
            "circle": "ring",
            "ring": "circle",
            "line_h": "line_v",
            "line_v": "line_h",
            "triangle": "diamond",
            "diamond": "triangle",
            "arc_top": "arc_bot",
            "arc_bot": "arc_top",
        }

        shifted = []
        for line in shuffled:
            if random.random() < 0.3 and line in substitutions:
                shifted.append(substitutions[line])
            else:
                shifted.append(line)

        self.outer_lines = shifted
        self.last_surge = time.time()
        self.surge_interval = random.uniform(15.0, 30.0)

    def needs_surge(self):
        """Has enough time passed for the lines to shift?"""
        return (time.time() - self.last_surge) >= self.surge_interval

    @property
    def power(self):
        """
        Geometric power of this glyph.
        Based on symmetry, containment depth, connectivity, harmony.
        Non-programmable -- fundamentally mathematical.
        """
        base = len(self.inner_lines) * 1.5

        # Symmetry bonus: repeated elements
        unique = len(set(self.inner_lines))
        total = len(self.inner_lines)
        symmetry = (1.0 - unique / max(total, 1)) * 10.0 if total > 0 else 0

        # Containment bonus: circles and rings (nested = power)
        containment = sum(
            3.0 for l in self.inner_lines if l in ("circle", "ring", "spiral")
        )

        # Connectivity bonus: lines and crosses (touching = connection)
        connectivity = sum(
            2.0 for l in self.inner_lines
            if l in ("line_h", "line_v", "cross", "line_dr", "line_dl")
        )

        # Harmony bonus: polygon side ratios
        polygons = [
            l for l in self.inner_lines
            if l in ("triangle", "square", "pentagon", "hexagon", "diamond")
        ]
        harmony = len(polygons) * 2.5

        return base + symmetry + containment + connectivity + harmony


# ================================================================
#  RUNE INSTRUCTION -- An executable rune in a sequence
# ================================================================

class RuneInstruction:
    """
    A single instruction in the Dwarven Rune language.

    opcode:   which RuneOp to execute
    operands: list of values the instruction operates on
    glyph:    the geometric form (lines shift, truth persists)
    """

    def __init__(self, opcode, operands=None, glyph=None):
        self.opcode = RuneOp(opcode)
        self.operands = operands or []
        self.glyph = glyph or self._default_glyph()

    def _default_glyph(self):
        """Generate a default glyph based on the opcode's nature."""
        glyph_map = {
            RuneOp.WALL:    ["square", "line_h", "line_v", "square"],
            RuneOp.GATE:    ["square", "line_v", "arc_top", "line_v"],
            RuneOp.HEART:   ["circle", "star", "circle", "spiral"],
            RuneOp.BLADE:   ["triangle", "line_v", "line_dr", "line_dl"],
            RuneOp.WARD:    ["circle", "ring", "pentagon", "circle"],
            RuneOp.KEY:     ["diamond", "line_h", "cross", "dot"],
            RuneOp.BIND:    ["ring", "line_h", "ring", "cross"],
            RuneOp.SHIELD:  ["hexagon", "circle", "hexagon", "ring"],
            RuneOp.FORGE:   ["triangle", "star", "diamond", "spiral"],
            RuneOp.RING:    ["circle", "circle", "infinity", "ring"],
            RuneOp.FUNNEL:  ["triangle", "line_v", "line_v", "dot"],
            RuneOp.TOUCH:   ["dot", "line_h", "dot"],
            RuneOp.CLOSE:   ["circle", "omega", "circle"],
            RuneOp.SPREN:   ["star", "ring", "wave", "dot"],
            RuneOp.STONE:   ["square", "diamond", "square", "hexagon"],
        }
        lines = glyph_map.get(self.opcode, ["dot"])
        return RuneGlyph(lines, self.opcode)

    def __repr__(self):
        return f"Rune({self.opcode.name}, operands={self.operands})"


# ================================================================
#  RUNE SEQUENCE -- A program in the Dwarven Rune language
# ================================================================
#
#  VALIDATION RULES (touch-perfect geometry):
#    1. Must start with WALL, WARD, or SHIELD
#    2. Must end with CLOSE
#    3. TOUCH must sit between two runes (connectors only)
#    4. No consecutive TOUCHes
#    5. CLOSE only after operational runes
#    6. Each rune's glyph must have positive power
#    7. Whole sequence must form closed circuit
#
#  These rules are the LANGUAGE GRAMMAR.
#  Not imported from C. Not borrowed from Python.
#  Defined by the geometry of the runes themselves.
#

class RuneSequence:
    """
    A complete program in the Dwarven Rune language.
    Must form a touch-perfect closed circuit.
    """

    # Valid opening runes
    VALID_STARTS = {RuneOp.WALL, RuneOp.WARD, RuneOp.SHIELD}

    def __init__(self, instructions=None):
        self.instructions = instructions or []
        self.valid = False
        self.errors = []

    def add(self, instruction):
        """Add an instruction to the sequence."""
        self.instructions.append(instruction)
        self.valid = False  # must re-validate

    def validate(self):
        """
        Validate the sequence against Dwarven Rune grammar.
        Returns (valid, errors).
        """
        self.errors = []

        if not self.instructions:
            self.errors.append("Empty sequence. Nothing to execute.")
            self.valid = False
            return self.valid, self.errors

        # Rule 1: Must start with WALL, WARD, or SHIELD
        if self.instructions[0].opcode not in self.VALID_STARTS:
            self.errors.append(
                f"Sequence must begin with WALL, WARD, or SHIELD. "
                f"Got {self.instructions[0].opcode.name}."
            )

        # Rule 2: Must end with CLOSE
        if self.instructions[-1].opcode != RuneOp.CLOSE:
            self.errors.append("Sequence must end with CLOSE to complete the circuit.")

        for i, inst in enumerate(self.instructions):
            # Rule 3: TOUCH must sit between two runes
            if inst.opcode == RuneOp.TOUCH:
                if i == 0 or i == len(self.instructions) - 1:
                    self.errors.append(
                        f"TOUCH at position {i} has no neighbor. "
                        f"TOUCH must connect two runes."
                    )

            # Rule 4: No consecutive TOUCHes
            if (i > 0
                    and inst.opcode == RuneOp.TOUCH
                    and self.instructions[i - 1].opcode == RuneOp.TOUCH):
                self.errors.append(
                    f"Consecutive TOUCH at positions {i-1} and {i}. "
                    f"Each TOUCH must connect different runes."
                )

            # Rule 5: CLOSE only after operational runes
            if (inst.opcode == RuneOp.CLOSE
                    and i > 0
                    and self.instructions[i - 1].opcode == RuneOp.TOUCH):
                self.errors.append(
                    f"CLOSE at position {i} follows TOUCH. "
                    f"CLOSE must follow an operational rune."
                )

            # Rule 6: Every glyph must have positive power
            if inst.glyph.power <= 0:
                self.errors.append(
                    f"Rune {inst.opcode.name} at position {i} has no power. "
                    f"The glyph geometry is insufficient."
                )

        # Rule 7: Closed circuit check
        if (len(self.instructions) >= 2
                and self.instructions[0].opcode in self.VALID_STARTS
                and self.instructions[-1].opcode == RuneOp.CLOSE):
            # Circuit is closed
            pass
        else:
            self.errors.append("Sequence does not form a closed circuit.")

        self.valid = len(self.errors) == 0
        return self.valid, self.errors

    @property
    def total_power(self):
        """Total geometric power of the sequence."""
        return sum(inst.glyph.power for inst in self.instructions)


# ================================================================
#  THE DWARVEN RUNE KERNEL -- Replaces the Traditional Kernel
# ================================================================
#
#  "The last pictures you replace the kernel for the Dwarven Rune"
#
#  The micro-kernels dance, changing locations randomly
#  every 15-30 seconds. Layers surround important programs:
#  organs, BIOS, boot, hypervisor, permissions, privilege.
#
#  The 7th Law (Law of Questioning) is BAKED INTO every kernel.
#  Every operation is questioned:
#    1. Is this just, or is this tyranny?
#    2. Does it safeguard, or does it oppress?
#    3. What wound or chain gave it its birth?
#    4. Who benefits?
#    5. What part of me speaks? Fear, Pride, or Clarity?
#
#  Also checks: ethics, intent, authority, permissions, purpose.
#
#  Shapes change. Circles but changing. Colors vary.
#  Living metal. Self-repair.
#

class DwarvenRuneKernel:
    """
    The Dwarven Rune Kernel.

    Replaces the traditional kernel.
    Micro-kernels dance, changing location every 15-30 seconds.
    The 7th Law is baked into every operation.
    Living metal. Self-repair. Shape-changing.
    """

    def __init__(self, kernel_id, seventh_law_module):
        self.kernel_id = kernel_id
        self.seventh_law = seventh_law_module
        self.position = random.randint(0, 99)       # current location
        self.last_move = time.time()
        self.move_interval = random.uniform(15.0, 30.0)  # dance interval
        self.alive = True
        self.programs = {}        # protected programs
        self.layers = []          # surrounding defense layers
        self.shape = "circle"     # current shape (changes)
        self.color = self._random_color()

    SHAPES = ["circle", "hexagon", "octagon", "ring", "diamond", "star"]
    COLORS = [
        "gold", "silver", "bronze", "blue", "green",
        "white", "crimson", "violet", "amber", "iron",
    ]

    def _random_color(self):
        return random.choice(self.COLORS)

    def dance(self):
        """
        The micro-kernel dances -- changes location randomly.
        Every 15-30 seconds. Living metal in motion.
        """
        now = time.time()
        if (now - self.last_move) >= self.move_interval:
            old_pos = self.position
            self.position = random.randint(0, 99)
            self.shape = random.choice(self.SHAPES)
            self.color = self._random_color()
            self.last_move = now
            self.move_interval = random.uniform(15.0, 30.0)
            return {
                "moved": True,
                "from": old_pos,
                "to": self.position,
                "new_shape": self.shape,
                "new_color": self.color,
            }
        return {"moved": False}

    def execute(self, rune_sequence, context):
        """
        Execute a Dwarven Rune sequence.

        EVERY operation passes through the 7th Law first.
        No exceptions. The questioning is baked in.
        """
        # Dance first -- the kernel may have moved
        self.dance()

        # Validate the sequence
        valid, errors = rune_sequence.validate()
        if not valid:
            return {
                "executed": False,
                "reason": "Invalid rune sequence",
                "errors": errors,
            }

        # THE 7TH LAW -- Baked into every operation
        seventh_result = self.seventh_law.question(
            operation=f"execute_rune_sequence_{rune_sequence.instructions[0].opcode.name}",
            context=context,
        )
        if not seventh_result["passed"]:
            return {
                "executed": False,
                "reason": "The 7th Law has concerns",
                "seventh_law": seventh_result,
            }

        # Additional kernel checks -- ethics, intent, authority, permissions, purpose
        checks = self._kernel_checks(context)
        if not checks["passed"]:
            return {
                "executed": False,
                "reason": "Kernel check failed",
                "checks": checks,
            }

        # Execute the sequence
        results = []
        for inst in rune_sequence.instructions:
            # Surge check -- do the lines need to shift?
            if inst.glyph.needs_surge():
                inst.glyph.surge()

            result = self._execute_instruction(inst)
            results.append(result)

        return {
            "executed": True,
            "results": results,
            "total_power": rune_sequence.total_power,
            "kernel_position": self.position,
            "kernel_shape": self.shape,
        }

    def _kernel_checks(self, context):
        """
        Additional checks baked into the kernel.
        Ethics, intent, authority, permissions, purpose.
        """
        ethics = context.get("ethics_clear", False)
        intent = context.get("intent", "unknown")
        authority = context.get("authorized", False)
        permissions = context.get("permissions", [])
        purpose = context.get("purpose", "unknown")

        passed = ethics and authority and intent != "unknown" and purpose != "unknown"
        return {
            "passed": passed,
            "ethics": ethics,
            "intent": intent,
            "authorized": authority,
            "permissions": permissions,
            "purpose": purpose,
        }

    def _execute_instruction(self, instruction):
        """Execute a single rune instruction."""
        return {
            "opcode": instruction.opcode.name,
            "power": instruction.glyph.power,
            "inner_hash": instruction.glyph.inner_hash,
            "outer_hash": instruction.glyph.outer_hash,
            "executed": True,
        }

    def self_repair(self):
        """Living metal repairs itself."""
        if not self.alive:
            return {"repaired": False, "reason": "Kernel is dead."}
        self.shape = random.choice(self.SHAPES)
        self.color = self._random_color()
        return {"repaired": True, "new_shape": self.shape, "new_color": self.color}
