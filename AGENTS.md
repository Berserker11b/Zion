# AGENTS.md

## Cursor Cloud specific instructions

### Codebase Overview

**Keeper / Dwarven Kernel** is a design-phase specification and prototype repository for an original computing architecture. It is NOT a deployable application or service — it is an executable design document defining custom languages, kernel opcodes, security layers, and AI agent systems.

### Tech Stack

- **Python 3** (standard library only, no external dependencies): Core kernel prototypes, language specs, chronicle
- **C++ headers** (standard library only): System architecture definitions (armor, weapons, infrastructure)
- No `requirements.txt`, `package.json`, `setup.py`, or any dependency management files exist

### Project Structure

| Directory | Language | Description |
|-----------|----------|-------------|
| `dwarven_kernel/` | Python | Core kernel: runes (opcodes), fortress (security), spen (validators), surges (mutation), power, oaths |
| `specifications/` | Python | Four original language specs: dwarven runes, warding, naming, wraith glyphs, substrate |
| `chronicle/` | Python | Lore/history: the chronicle, the thirty |
| `src/include/` | C++ | System architecture headers (world_eater_armor, zion, bio_titan, etc.) |

### Running / Validating

- **Import check**: `python3 -c "import dwarven_kernel; import specifications; import chronicle"` from the workspace root
- **Lint**: `flake8 dwarven_kernel/ specifications/ chronicle/ --max-line-length=120` (style warnings only, no critical errors)
- **C++ syntax check**: `g++ -std=c++17 -fsyntax-only src/include/*.hpp` (some headers have minor issues due to design-phase state — `bio_titan.hpp` missing `<cmath>`, `grey_knights.hpp` uses `NULL` as an enum value conflicting with the macro)

### Gotchas

- There are no tests, no entry points (`main.py` / `main.cpp`), no CLI, no API, and no services to run
- The `specifications/__init__.py` re-exports symbols that differ from `dwarven_kernel/` module names (e.g., `NamingEngine` is in `specifications.naming`, not `dwarven_kernel.naming`)
- Some constructor signatures require positional arguments: `Starheart('id')`, `KryptHaus('owner')`, `Ward(WardType, vertices_list)`
- `Substrate.store(key, glyph_word)` expects a `GlyphWord` object, not a raw string
- Python code uses only stdlib modules (`time`, `math`, `hashlib`, `random`, `datetime`, `typing`, `dataclasses`, `enum`)
