"""
PARSER — Touch-Perfect Rune Validation
========================================

The Spen parser. Every AI parses wards through this.

Rules:
    - Rune sequences must be TOUCH-PERFECT
    - TOUCH must sit between two runes to connect them
    - CLOSE only after a valid rune list
    - Ward must CLOSE (the circle must be complete)
    - If they don't touch perfectly, the ward doesn't work
    - Power is determined by how mathematically correct it has been parsed

"Require perfect geometry to activate."
"Non-programmable. They are fundamentally mathematical sigils and tattoos."

"Glyphs that are in a circular pattern. Every ward touches
 at the microscopic level. A header encapsulates these Glyphs.
 In order to alter them the key must be spoken or scripted like API."
"""

import time
import hashlib
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Tuple

from .runes import RuneOp, Rune, RuneSequence, INNER_GLYPHS
from .glyphs import Glyph


# ================================================================
#                    PARSE ERRORS
# ================================================================

class ParseError:
    """A parsing error — the ward doesn't work."""

    def __init__(self, message: str, position: int = -1, severity: str = "error"):
        self.message = message
        self.position = position
        self.severity = severity  # "error", "warning", "fatal"

    def __repr__(self):
        pos = f" at position {self.position}" if self.position >= 0 else ""
        return f"[{self.severity.upper()}]{pos}: {self.message}"


# ================================================================
#                    PARSE RESULT
# ================================================================

@dataclass
class RuneParseResult:
    """
    Result of parsing a rune sequence.
    Contains the validated sequence, errors, and power score.
    """
    ok: bool
    sequence: Optional[RuneSequence] = None
    errors: List[ParseError] = field(default_factory=list)
    warnings: List[ParseError] = field(default_factory=list)
    power_score: float = 0.0
    symmetry_score: float = 0.0
    containment_score: float = 0.0
    connectivity_score: float = 0.0
    parse_time_ms: float = 0.0

    @property
    def total_power(self) -> float:
        """
        Total power = parse correctness × mathematical properties.
        "When activated, its power is determined by how mathematically
         correct it has been parsed. Like mastery."
        """
        if not self.ok:
            return 0.0
        return (
            self.power_score * 0.4 +
            self.symmetry_score * 0.2 +
            self.containment_score * 0.2 +
            self.connectivity_score * 0.2
        )


# ================================================================
#                    SPEN PARSER
# ================================================================

class SpenParser:
    """
    The Spen Parser — validates rune sequences with touch-perfect precision.

    Every ward, every rune sequence, every program must pass through this.
    "All fortress AIs that need to read ward-language use this spen parser."

    Parsing rules:
        1. Must start with containment (WALL, WARD, or SHIELD)
        2. Must end with CLOSE
        3. TOUCH must be between two non-TOUCH runes
        4. No consecutive TOUCHes
        5. CLOSE only valid after at least one operational rune
        6. Each rune's glyph must have positive power (geometric validity)
        7. The whole sequence must form a closed circuit (touch-perfect)

    Header encapsulation:
        Every ward sequence is wrapped in a header that identifies it.
        The header IS the outer circle. The runes inside are the content.
    """

    def __init__(self):
        self.parse_count: int = 0
        self.error_count: int = 0

    def parse(self, tokens: List[RuneOp],
              args: Optional[List[Dict[str, Any]]] = None) -> RuneParseResult:
        """
        Parse a list of rune opcodes into a validated RuneSequence.
        Returns a RuneParseResult with power scores.
        """
        start = time.time()
        self.parse_count += 1

        errors = []
        warnings = []

        if not tokens:
            return RuneParseResult(
                ok=False,
                errors=[ParseError("Empty rune sequence.", 0, "fatal")],
                parse_time_ms=(time.time() - start) * 1000,
            )

        args = args or [{}] * len(tokens)
        if len(args) != len(tokens):
            args = args + [{}] * (len(tokens) - len(args))

        # Rule 1: Must start with containment
        containment_starts = {RuneOp.WALL, RuneOp.WARD, RuneOp.SHIELD}
        if tokens[0] not in containment_starts:
            errors.append(ParseError(
                f"Sequence must begin with containment rune (WALL, WARD, or SHIELD), "
                f"got {tokens[0].rune_id}.",
                0, "error"
            ))

        # Rule 2: Must end with CLOSE
        if tokens[-1] != RuneOp.CLOSE:
            errors.append(ParseError(
                f"Sequence must end with CLOSE to seal the circle, "
                f"got {tokens[-1].rune_id}.",
                len(tokens) - 1, "error"
            ))

        # Rule 3 & 4: TOUCH validation
        for i, tok in enumerate(tokens):
            if tok == RuneOp.TOUCH:
                if i == 0:
                    errors.append(ParseError(
                        "TOUCH cannot be the first rune.", i, "error"
                    ))
                elif i == len(tokens) - 1:
                    errors.append(ParseError(
                        "TOUCH cannot be the last rune.", i, "error"
                    ))
                elif tokens[i - 1] == RuneOp.TOUCH:
                    errors.append(ParseError(
                        "Consecutive TOUCH runes — invalid connection.", i, "error"
                    ))
                elif tokens[i + 1] == RuneOp.TOUCH:
                    errors.append(ParseError(
                        "Consecutive TOUCH runes — invalid connection.", i, "error"
                    ))

        # Rule 5: CLOSE only after operational runes
        operational = {RuneOp.HEART, RuneOp.BLADE, RuneOp.KEY, RuneOp.BIND,
                       RuneOp.FORGE, RuneOp.RING, RuneOp.FUNNEL, RuneOp.SPREN,
                       RuneOp.STONE, RuneOp.GATE}
        has_operational = any(t in operational for t in tokens)
        if not has_operational:
            warnings.append(ParseError(
                "No operational runes in sequence — ward has no active function.",
                -1, "warning"
            ))

        # Rule 6: Validate each rune's glyph has positive power
        power_scores = []
        for i, tok in enumerate(tokens):
            glyph = INNER_GLYPHS.get(tok)
            if glyph:
                p = glyph.power
                power_scores.append(p)
                if p <= 0:
                    errors.append(ParseError(
                        f"Rune {tok.rune_id} has zero geometric power — malformed glyph.",
                        i, "error"
                    ))
            else:
                power_scores.append(0)
                errors.append(ParseError(
                    f"Unknown rune {tok.rune_id} — no glyph definition.",
                    i, "fatal"
                ))

        # Rule 7: Touch-perfect connectivity
        # Every rune must connect to its neighbors through TOUCH or adjacency
        connectivity = self._check_connectivity(tokens)
        if connectivity < 0.5:
            warnings.append(ParseError(
                f"Poor connectivity ({connectivity:.0%}) — runes may not touch perfectly.",
                -1, "warning"
            ))

        # Calculate scores
        avg_power = sum(power_scores) / len(power_scores) if power_scores else 0
        symmetry = self._calculate_symmetry(tokens)
        containment = self._calculate_containment(tokens)

        ok = len(errors) == 0

        # Build the sequence if valid
        sequence = None
        if ok:
            seq = RuneSequence(name=f"parsed_{self.parse_count}")
            for i, tok in enumerate(tokens):
                rune = Rune(op=tok, args=args[i] if i < len(args) else {})
                rune.power = power_scores[i] if i < len(power_scores) else 0
                seq.runes.append(rune)
            seq.sealed = True  # parser-validated sequences are auto-sealed
            sequence = seq

        if not ok:
            self.error_count += 1

        elapsed = (time.time() - start) * 1000

        return RuneParseResult(
            ok=ok,
            sequence=sequence,
            errors=errors,
            warnings=warnings,
            power_score=avg_power,
            symmetry_score=symmetry,
            containment_score=containment,
            connectivity_score=connectivity,
            parse_time_ms=round(elapsed, 3),
        )

    def _check_connectivity(self, tokens: List[RuneOp]) -> float:
        """
        Check how well connected the rune sequence is.
        TOUCH runes between operational runes increase connectivity.
        """
        if len(tokens) <= 2:
            return 1.0

        connections = 0
        possible = len(tokens) - 1

        for i in range(len(tokens) - 1):
            # Adjacent runes are automatically connected
            connections += 0.5
            # TOUCH between them adds full connection
            if tokens[i] == RuneOp.TOUCH or tokens[i + 1] == RuneOp.TOUCH:
                connections += 0.5

        return min(connections / possible, 1.0) if possible > 0 else 0.0

    def _calculate_symmetry(self, tokens: List[RuneOp]) -> float:
        """
        Calculate symmetry of the rune sequence.
        Palindromic or mirror-symmetric sequences score higher.
        """
        n = len(tokens)
        if n <= 1:
            return 1.0

        matches = 0
        for i in range(n // 2):
            if tokens[i] == tokens[n - 1 - i]:
                matches += 1

        return matches / (n // 2) if n > 1 else 1.0

    def _calculate_containment(self, tokens: List[RuneOp]) -> float:
        """
        Calculate containment depth of the sequence.
        More containment runes = stronger warding.
        """
        containment_runes = {RuneOp.WALL, RuneOp.WARD, RuneOp.SHIELD,
                             RuneOp.CLOSE, RuneOp.RING}
        count = sum(1 for t in tokens if t in containment_runes)
        return min(count * 0.25, 1.0)

    def validate_header(self, header: Dict[str, Any]) -> bool:
        """
        Validate a ward header.
        "A header encapsulates these Glyphs."
        """
        required = {"name", "version", "key_signature"}
        return required.issubset(header.keys())

    def quick_check(self, tokens: List[RuneOp]) -> bool:
        """Fast validation — just checks structure, no power scoring."""
        if not tokens:
            return False
        if tokens[0] not in {RuneOp.WALL, RuneOp.WARD, RuneOp.SHIELD}:
            return False
        if tokens[-1] != RuneOp.CLOSE:
            return False
        for i, t in enumerate(tokens):
            if t == RuneOp.TOUCH:
                if i == 0 or i == len(tokens) - 1:
                    return False
                if tokens[i - 1] == RuneOp.TOUCH:
                    return False
        return True

    def __repr__(self):
        return f"SpenParser<parsed={self.parse_count} errors={self.error_count}>"
