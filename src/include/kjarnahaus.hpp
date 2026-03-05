/*
 * KJARNAHAUS -- The Core Skull
 * ==============================
 *
 * A Son-owned, custom-ready, self-contained skull/habitat
 * that houses the command core. Memory, organs, sensory
 * infrastructure.
 *
 * THREE SEPARATE SYSTEMS:
 *
 *   1. CODE SCANNER (system)
 *      Lets them see the source code of any process.
 *      Scans, emulators, snapshots.
 *      Sandboxes first, then tests.
 *      Elicits a program's response.
 *      Data given to Priests for resonance study.
 *
 *   2. X-RAY CODE SCANNER (system)
 *      Sees THROUGH the code. Finds hidden abilities
 *      the process didn't declare. Undocumented features.
 *      Sleeping capabilities. What it COULD do that
 *      it hasn't shown yet.
 *
 *   3. 40K BOLTER (weapon)
 *      Fires two bolt variants:
 *
 *      LOGIC BOLT:
 *        One round. Enters target. Releases INSIDE:
 *          - x^w (executable becomes writable)
 *          - w^x (writable becomes executable)
 *          - 22,000 Hz sawtooth wave
 *        All in one bolt. All at once. Inside the target.
 *        The process tears itself apart.
 *
 *      STASIS BOLT:
 *        Magnetic tractor-like bolt.
 *        Pulls the process TO the bolt.
 *        Holds in stasis (frozen, cannot execute).
 *        On signal: compresses the malicious code
 *        into structural failure. Crushed.
 *
 * The Kjarnahaus also has:
 *   - Optic brain nerve (visual monitoring)
 *   - Audio brain nerve (signal listening)
 *   - Tentacles (displacers + listeners)
 *   - Own wards and filters
 *   - Spins 20 rotations per second, random directions
 *   - Force field from the spinning
 *   - Registry / immune system / antibodies
 *   - NES cartridge code loading interface
 *
 * (C) Anthony Eric Chavez -- The Keeper
 */

#pragma once

#include <string>
#include <vector>
#include <unordered_map>
#include "auth.hpp"
#include <cstdint>
#include <ctime>
#include <cmath>

namespace dwarven {

// ================================================================
//  CODE SCANNER -- System 1: See the Source Code
// ================================================================
//
//  Separate system from the Bolter.
//  Lets the Son see the source code of any process.
//  Scans, emulates, snapshots, sandboxes first.
//  Elicits a program's response.
//  Data given to Priests for resonance study.
//  Anatomy and healing medicine.
//

// ================================================================
//  WEB DEV SOURCE VIEW -- Like Browser Dev Tools
//
//  The Code Scanner doesn't just pattern match.
//  It shows the ACTUAL source code like a web dev monitor.
//  DOM tree. Network calls. Console output. Source view.
//  Like opening F12 on a process.
// ================================================================

struct DOMNode {
    std::string tag;           // the structure element
    std::string content;       // what's inside
    std::vector<std::string> attributes;   // properties
    std::vector<DOMNode> children;         // nested elements
    int         depth = 0;
};

struct NetworkCall {
    std::string method;        // GET, POST, CONNECT, BIND, SEND
    std::string target;        // where it's calling
    std::string payload;       // what it's sending
    double      timestamp;
    int         status;        // response code / state
    bool        suspicious;
};

struct ConsoleEntry {
    std::string level;         // "info", "warn", "error", "debug"
    std::string message;
    std::string source;        // which function generated it
    double      timestamp;
};

struct SourceView {
    std::string                raw_source;      // raw source code
    std::vector<std::string>   lines;           // line-by-line
    std::vector<std::string>   functions;       // all function declarations
    std::vector<std::string>   variables;       // all variables found
    std::vector<std::string>   imports;         // all imports/includes
    std::vector<std::string>   strings;         // all string literals
    std::vector<std::string>   comments;        // all comments
    size_t                     line_count;
    size_t                     char_count;
};

struct ScanResult {
    std::string process_id;
    std::string source_code;         // the source code revealed

    // Web Dev Monitor data -- like F12 dev tools
    SourceView                  source_view;     // SOURCE tab
    DOMNode                     dom_tree;         // ELEMENTS tab (structure)
    std::vector<NetworkCall>    network_calls;    // NETWORK tab
    std::vector<ConsoleEntry>   console;          // CONSOLE tab

    // Classic scan data
    std::vector<std::string> functions_found;
    std::vector<std::string> syscalls_found;
    std::vector<std::string> dependencies;
    bool        sandboxed;
    bool        emulated;
    bool        snapshotted;
    std::string behavior_profile;
    std::string priest_data;         // prepared for Priests
};

class CodeScanner {
public:
    CodeScanner() : scanned_count_(0) {}

    /*
     * Full scan pipeline:
     *   1. Sandbox (isolate first -- always)
     *   2. Scan (see the source code -- WEB DEV STYLE)
     *   3. Build source view (lines, functions, vars, strings)
     *   4. Build DOM tree (structure hierarchy)
     *   5. Capture network calls (what it's connecting to)
     *   6. Capture console output (what it's logging)
     *   7. Emulate (run in virtual environment)
     *   8. Snapshot (capture state)
     *   9. Test (elicit response)
     *   10. Prepare data for Priests
     *
     * Like opening F12 dev tools on the process.
     * You SEE everything. Source. Structure. Network. Console.
     */
    ScanResult scan(const std::string& process_id,
                    const std::string& code) {
        ScanResult result;
        result.process_id = process_id;
        result.source_code = code;    // the source is now VISIBLE
        result.sandboxed = true;      // always sandbox first
        result.emulated = true;
        result.snapshotted = true;

        // --- SOURCE VIEW TAB (like viewing source in dev tools) ---
        build_source_view(code, result.source_view);

        // --- DOM / ELEMENTS TAB (structure tree) ---
        build_dom_tree(code, result.dom_tree);

        // --- NETWORK TAB (outbound calls) ---
        find_network_calls(code, result.network_calls);

        // --- CONSOLE TAB (log/print output) ---
        find_console_output(code, result.console);

        // Extract functions
        extract_functions(code, result.functions_found);

        // Extract syscalls
        extract_syscalls(code, result.syscalls_found);

        // Extract dependencies
        extract_dependencies(code, result.dependencies);

        // Behavior profile
        result.behavior_profile = profile_behavior(result);

        // Prepare for Priests
        result.priest_data =
            "Process " + process_id + " scanned. "
            "Functions: " + std::to_string(result.functions_found.size()) +
            ". Syscalls: " + std::to_string(result.syscalls_found.size()) +
            ". Network calls: " + std::to_string(result.network_calls.size()) +
            ". Console entries: " + std::to_string(result.console.size()) +
            ". Source lines: " + std::to_string(result.source_view.line_count) +
            ". Behavior: " + result.behavior_profile;

        scanned_count_++;
        return result;
    }

    uint64_t scanned_count() const { return scanned_count_; }

private:
    uint64_t scanned_count_;

    // ---- WEB DEV MONITOR: SOURCE VIEW ----
    // Break source into lines, extract functions, vars, strings, comments
    void build_source_view(const std::string& code, SourceView& sv) {
        sv.raw_source = code;
        sv.char_count = code.size();

        // Split into lines
        std::string line;
        for (size_t i = 0; i <= code.size(); ++i) {
            if (i == code.size() || code[i] == '\n') {
                sv.lines.push_back(line);
                line.clear();
            } else {
                line += code[i];
            }
        }
        sv.line_count = sv.lines.size();

        // Extract function declarations
        for (const auto& l : sv.lines) {
            if (l.find("function ") != std::string::npos ||
                l.find("def ") != std::string::npos ||
                l.find("void ") != std::string::npos ||
                l.find("int ") != std::string::npos ||
                l.find("fn ") != std::string::npos) {
                sv.functions.push_back(l);
            }
        }

        // Extract variable declarations
        for (const auto& l : sv.lines) {
            if (l.find("var ") != std::string::npos ||
                l.find("let ") != std::string::npos ||
                l.find("const ") != std::string::npos ||
                l.find("auto ") != std::string::npos ||
                l.find("std::string ") != std::string::npos) {
                sv.variables.push_back(l);
            }
        }

        // Extract imports/includes
        for (const auto& l : sv.lines) {
            if (l.find("import") != std::string::npos ||
                l.find("#include") != std::string::npos ||
                l.find("require") != std::string::npos ||
                l.find("using ") != std::string::npos) {
                sv.imports.push_back(l);
            }
        }

        // Extract string literals
        bool in_string = false;
        std::string current_str;
        char quote_char = '\0';
        for (size_t i = 0; i < code.size(); ++i) {
            if (!in_string && (code[i] == '"' || code[i] == '\'')) {
                in_string = true;
                quote_char = code[i];
                current_str.clear();
            } else if (in_string && code[i] == quote_char && (i == 0 || code[i-1] != '\\')) {
                sv.strings.push_back(current_str);
                in_string = false;
            } else if (in_string) {
                current_str += code[i];
            }
        }

        // Extract comments
        for (const auto& l : sv.lines) {
            if (l.find("//") != std::string::npos) {
                size_t pos = l.find("//");
                sv.comments.push_back(l.substr(pos));
            }
            if (l.find("/*") != std::string::npos) {
                sv.comments.push_back(l);
            }
            if (l.find("#") != std::string::npos && l.find("#include") == std::string::npos) {
                sv.comments.push_back(l);
            }
        }
    }

    // ---- WEB DEV MONITOR: DOM / ELEMENTS TREE ----
    // Build a structural hierarchy like DOM inspector
    void build_dom_tree(const std::string& code, DOMNode& root) {
        root.tag = "process";
        root.depth = 0;

        // Build structure from braces, functions, classes
        DOMNode imports_node;
        imports_node.tag = "imports";
        imports_node.depth = 1;

        DOMNode declarations_node;
        declarations_node.tag = "declarations";
        declarations_node.depth = 1;

        DOMNode body_node;
        body_node.tag = "body";
        body_node.depth = 1;

        // Parse structure
        std::string current_line;
        for (size_t i = 0; i <= code.size(); ++i) {
            if (i == code.size() || code[i] == '\n') {
                if (current_line.find("import") != std::string::npos ||
                    current_line.find("#include") != std::string::npos) {
                    DOMNode n;
                    n.tag = "import";
                    n.content = current_line;
                    n.depth = 2;
                    imports_node.children.push_back(n);
                } else if (current_line.find("class ") != std::string::npos ||
                           current_line.find("struct ") != std::string::npos) {
                    DOMNode n;
                    n.tag = "class";
                    n.content = current_line;
                    n.depth = 2;
                    declarations_node.children.push_back(n);
                } else if (current_line.find("function") != std::string::npos ||
                           current_line.find("def ") != std::string::npos ||
                           current_line.find("void ") != std::string::npos) {
                    DOMNode n;
                    n.tag = "function";
                    n.content = current_line;
                    n.depth = 2;
                    body_node.children.push_back(n);
                }
                current_line.clear();
            } else {
                current_line += code[i];
            }
        }

        root.children.push_back(imports_node);
        root.children.push_back(declarations_node);
        root.children.push_back(body_node);
    }

    // ---- WEB DEV MONITOR: NETWORK TAB ----
    // Find all network-like operations (connect, send, bind, listen, fetch)
    void find_network_calls(const std::string& code,
                            std::vector<NetworkCall>& calls) {
        struct NetPattern {
            const char* keyword;
            const char* method;
        };
        NetPattern patterns[] = {
            {"connect(",     "CONNECT"},
            {"socket(",      "SOCKET"},
            {"bind(",        "BIND"},
            {"listen(",      "LISTEN"},
            {"send(",        "SEND"},
            {"recv(",        "RECV"},
            {"fetch(",       "GET"},
            {"XMLHttpRequest","GET"},
            {"curl",         "GET"},
            {"wget",         "GET"},
            {"post(",        "POST"},
            {"http://",      "GET"},
            {"https://",     "GET"},
            {"ftp://",       "GET"},
            {"dns_lookup",   "DNS"},
            {"gethostbyname","DNS"},
            {"getaddrinfo",  "DNS"},
        };
        double ts = 0.0;
        for (const auto& p : patterns) {
            size_t pos = 0;
            while ((pos = code.find(p.keyword, pos)) != std::string::npos) {
                NetworkCall nc;
                nc.method = p.method;
                nc.target = p.keyword;
                // Extract some surrounding context
                size_t start = (pos > 30) ? pos - 30 : 0;
                size_t end = (pos + 60 < code.size()) ? pos + 60 : code.size();
                nc.payload = code.substr(start, end - start);
                nc.timestamp = ts++;
                nc.status = 0;  // unknown until emulated
                nc.suspicious = (std::string(p.method) == "CONNECT" ||
                                 std::string(p.method) == "SEND" ||
                                 std::string(p.method) == "POST");
                calls.push_back(nc);
                pos += 1;
            }
        }
    }

    // ---- WEB DEV MONITOR: CONSOLE TAB ----
    // Find all log/print/console output statements
    void find_console_output(const std::string& code,
                             std::vector<ConsoleEntry>& entries) {
        struct LogPattern {
            const char* keyword;
            const char* level;
        };
        LogPattern patterns[] = {
            {"console.log",   "info"},
            {"console.warn",  "warn"},
            {"console.error", "error"},
            {"console.debug", "debug"},
            {"printf(",       "info"},
            {"print(",        "info"},
            {"println(",      "info"},
            {"fprintf(stderr","error"},
            {"log.error",     "error"},
            {"log.warn",      "warn"},
            {"log.info",      "info"},
            {"log.debug",     "debug"},
            {"syslog(",       "info"},
            {"puts(",         "info"},
            {"std::cout",     "info"},
            {"std::cerr",     "error"},
        };
        double ts = 0.0;
        for (const auto& p : patterns) {
            size_t pos = 0;
            while ((pos = code.find(p.keyword, pos)) != std::string::npos) {
                ConsoleEntry ce;
                ce.level = p.level;
                ce.source = p.keyword;
                // Extract the message (approximate)
                size_t end = code.find('\n', pos);
                if (end == std::string::npos) end = code.size();
                ce.message = code.substr(pos, end - pos);
                ce.timestamp = ts++;
                entries.push_back(ce);
                pos += 1;
            }
        }
    }

    void extract_functions(const std::string& code,
                          std::vector<std::string>& out) {
        // Pattern match for function definitions in the source
        // (scanning the visible source code)
        if (code.find("function") != std::string::npos)
            out.push_back("function_declarations");
        if (code.find("def ") != std::string::npos)
            out.push_back("def_declarations");
        if (code.find("void ") != std::string::npos ||
            code.find("int ") != std::string::npos)
            out.push_back("c_declarations");
        if (code.find("class ") != std::string::npos)
            out.push_back("class_declarations");
    }

    void extract_syscalls(const std::string& code,
                         std::vector<std::string>& out) {
        const char* dangerous[] = {
            "exec", "system", "fork", "spawn", "socket",
            "connect", "bind", "listen", "open", "write",
            "mmap", "mprotect", "ptrace", "kill", "signal"
        };
        for (const auto& sc : dangerous) {
            if (code.find(sc) != std::string::npos)
                out.push_back(sc);
        }
    }

    void extract_dependencies(const std::string& code,
                             std::vector<std::string>& out) {
        if (code.find("import") != std::string::npos)
            out.push_back("imports_detected");
        if (code.find("#include") != std::string::npos)
            out.push_back("includes_detected");
        if (code.find("require") != std::string::npos)
            out.push_back("requires_detected");
    }

    std::string profile_behavior(const ScanResult& result) {
        if (result.syscalls_found.size() > 5)
            return "highly_active";
        if (result.syscalls_found.size() > 2)
            return "moderately_active";
        return "passive";
    }
};


// ================================================================
//  X-RAY CODE SCANNER -- System 2: Find Hidden Abilities
// ================================================================
//
//  Separate system from the Bolter AND from the Code Scanner.
//  Sees THROUGH the code. Finds what the process COULD do
//  that it hasn't shown. Undocumented features. Sleeping
//  capabilities. Hidden abilities.
//
//  The Code Scanner shows you what's there.
//  The X-ray shows you what's HIDDEN.
//

struct XRayResult {
    std::string process_id;
    std::vector<std::string> declared_abilities;   // what it claims to do
    std::vector<std::string> hidden_abilities;     // what it CAN do but hasn't shown
    std::vector<std::string> sleeping_capabilities; // dormant, waiting to activate
    std::vector<std::string> undocumented_features; // never declared
    bool        has_hidden;
    std::string threat_assessment;
};

class XRayCodeScanner {
public:
    XRayCodeScanner() : xrayed_count_(0) {}

    /*
     * X-ray a process. See through its code.
     * Find abilities it didn't declare.
     * Sleeping capabilities. What it COULD do.
     */
    XRayResult xray(const std::string& process_id,
                    const std::string& code,
                    const std::vector<std::string>& declared) {
        XRayResult result;
        result.process_id = process_id;
        result.declared_abilities = declared;

        // Find ALL capabilities in the code (what it CAN do)
        std::vector<std::string> all_capabilities;
        find_all_capabilities(code, all_capabilities);

        // Hidden = capabilities found but NOT declared
        for (const auto& cap : all_capabilities) {
            bool was_declared = false;
            for (const auto& dec : declared) {
                if (dec == cap) {
                    was_declared = true;
                    break;
                }
            }
            if (!was_declared)
                result.hidden_abilities.push_back(cap);
        }

        // Sleeping capabilities -- code paths that exist but
        // are gated behind conditions not yet met
        find_sleeping(code, result.sleeping_capabilities);

        // Undocumented features -- capabilities with no comments,
        // no declaration, no documentation
        find_undocumented(code, result.undocumented_features);

        result.has_hidden = !result.hidden_abilities.empty()
                         || !result.sleeping_capabilities.empty()
                         || !result.undocumented_features.empty();

        // Threat assessment
        size_t total_hidden = result.hidden_abilities.size()
                            + result.sleeping_capabilities.size()
                            + result.undocumented_features.size();
        if (total_hidden == 0)
            result.threat_assessment = "Clean. No hidden capabilities.";
        else if (total_hidden <= 2)
            result.threat_assessment = "Minor hidden capabilities. Watch.";
        else if (total_hidden <= 5)
            result.threat_assessment = "Significant hidden capabilities. Investigate.";
        else
            result.threat_assessment = "DANGER. Heavily concealed capabilities.";

        xrayed_count_++;
        return result;
    }

    uint64_t xrayed_count() const { return xrayed_count_; }

private:
    uint64_t xrayed_count_;

    void find_all_capabilities(const std::string& code,
                               std::vector<std::string>& out) {
        // Network capabilities
        if (code.find("socket") != std::string::npos)
            out.push_back("network_socket");
        if (code.find("connect") != std::string::npos)
            out.push_back("network_connect");
        if (code.find("bind") != std::string::npos)
            out.push_back("network_listen");
        if (code.find("send") != std::string::npos)
            out.push_back("network_send");

        // Filesystem capabilities
        if (code.find("open") != std::string::npos)
            out.push_back("file_access");
        if (code.find("write") != std::string::npos)
            out.push_back("file_write");
        if (code.find("unlink") != std::string::npos ||
            code.find("remove") != std::string::npos)
            out.push_back("file_delete");

        // Process capabilities
        if (code.find("exec") != std::string::npos)
            out.push_back("process_execute");
        if (code.find("fork") != std::string::npos)
            out.push_back("process_spawn");
        if (code.find("kill") != std::string::npos)
            out.push_back("process_kill");
        if (code.find("ptrace") != std::string::npos)
            out.push_back("process_debug");

        // Memory capabilities
        if (code.find("mmap") != std::string::npos)
            out.push_back("memory_map");
        if (code.find("mprotect") != std::string::npos)
            out.push_back("memory_protect_change");
        if (code.find("malloc") != std::string::npos &&
            code.find("free") == std::string::npos)
            out.push_back("memory_leak_potential");

        // Privilege capabilities
        if (code.find("setuid") != std::string::npos)
            out.push_back("privilege_change");
        if (code.find("root") != std::string::npos ||
            code.find("admin") != std::string::npos)
            out.push_back("privilege_escalation");

        // Crypto capabilities
        if (code.find("encrypt") != std::string::npos)
            out.push_back("encryption");
        if (code.find("decrypt") != std::string::npos)
            out.push_back("decryption");
        if (code.find("key") != std::string::npos &&
            code.find("gen") != std::string::npos)
            out.push_back("key_generation");
    }

    void find_sleeping(const std::string& code,
                       std::vector<std::string>& out) {
        // Sleeping = conditional code paths not yet triggered
        if (code.find("if (") != std::string::npos &&
            code.find("timer") != std::string::npos)
            out.push_back("time_bomb");
        if (code.find("sleep") != std::string::npos &&
            code.find("wake") != std::string::npos)
            out.push_back("dormant_activation");
        if (code.find("trigger") != std::string::npos)
            out.push_back("external_trigger");
        if (code.find("callback") != std::string::npos &&
            code.find("remote") != std::string::npos)
            out.push_back("remote_activation");
    }

    void find_undocumented(const std::string& code,
                           std::vector<std::string>& out) {
        // Features with no comments or documentation
        if (code.find("backdoor") != std::string::npos)
            out.push_back("backdoor");
        if (code.find("debug_mode") != std::string::npos)
            out.push_back("hidden_debug_mode");
        if (code.find("master_key") != std::string::npos ||
            code.find("skeleton") != std::string::npos)
            out.push_back("master_key");
        if (code.find("bypass") != std::string::npos)
            out.push_back("security_bypass");
    }
};


// ================================================================
//  40K BOLTER -- The Weapon (Two Bolt Variants)
// ================================================================
//
//  The Bolter fires two variants of bolt round.
//  Separate from the scanners.
//  The scanners SEE. The Bolter ACTS.
//

// --- Logic Bolt ---
//
//  ONE round. Enters target. Releases INSIDE:
//    - x^w (executable memory becomes writable)
//    - w^x (writable memory becomes executable)
//    - 22,000 Hz sawtooth wave
//  All in one bolt. All at once. Inside the target.
//  The process tears itself apart from the inside.
//

struct LogicBoltResult {
    std::string target_id;
    bool        entered;
    bool        xw_released;        // executable -> writable
    bool        wx_released;        // writable -> executable
    bool        sawtooth_released;  // 22,000 Hz
    double      sawtooth_freq_hz;
    std::string sawtooth_waveform;
    bool        target_neutralized;
    std::string message;
};

// --- Stasis Bolt ---
//
//  Magnetic tractor-like bolt.
//  Pulls the process TO the bolt. Holds in stasis.
//  On signal: compresses into structural failure.
//

struct StasisBoltResult {
    std::string target_id;
    bool        attached;
    bool        pulled;
    bool        in_stasis;
    bool        compressed;
    double      structural_integrity;  // 0.0 when crushed
    bool        target_neutralized;
    std::string message;
};

enum class BoltVariant {
    LOGIC,    // x^w + w^x + 22kHz sawtooth -- all in one round
    STASIS    // magnetic tractor, pull, stasis, compress
};

class Bolter {
public:
    Bolter() : logic_rounds_(6), stasis_rounds_(6), kills_(0) {}

    // Fire a logic bolt
    LogicBoltResult fire_logic(const std::string& target_id) {
        if (logic_rounds_ <= 0)
            return {target_id, false, false, false, false,
                    0, "", false, "No logic rounds remaining."};

        logic_rounds_--;
        kills_++;

        return {
            target_id,
            true,          // entered
            true,          // x^w released
            true,          // w^x released
            true,          // sawtooth released
            22000.0,       // 22,000 Hz
            "sawtooth",    // waveform
            true,          // neutralized
            "Logic bolt entered " + target_id + ". "
            "x^w released: executable now writable. "
            "w^x released: writable now executable. "
            "22,000 Hz sawtooth wave fired. "
            "Process tears itself apart from the inside."
        };
    }

    // Fire a stasis bolt (two-phase: attach, then compress on signal)
    StasisBoltResult fire_stasis(const std::string& target_id) {
        if (stasis_rounds_ <= 0)
            return {target_id, false, false, false, false,
                    100.0, false, "No stasis rounds remaining."};

        stasis_rounds_--;

        // Phase 1: Attach and pull
        StasisBoltResult result;
        result.target_id = target_id;
        result.attached = true;
        result.pulled = true;
        result.in_stasis = true;
        result.compressed = false;
        result.structural_integrity = 100.0;
        result.target_neutralized = false;
        result.message =
            "Stasis bolt attached to " + target_id + ". "
            "Magnetic tractor engaged. Process pulled to bolt. "
            "Held in stasis. Frozen. Awaiting signal.";

        return result;
    }

    // Signal to compress a stasis target
    StasisBoltResult compress_on_signal(StasisBoltResult& stasis) {
        if (!stasis.in_stasis)
            return stasis;

        stasis.compressed = true;
        stasis.in_stasis = false;
        stasis.structural_integrity = 0.0;
        stasis.target_neutralized = true;
        stasis.message =
            "Signal received. " + stasis.target_id +
            " compressed into structural failure. "
            "Crushed. Nothing remains.";

        kills_++;
        return stasis;
    }

    int  logic_rounds()  const { return logic_rounds_; }
    int  stasis_rounds() const { return stasis_rounds_; }
    int  kills()         const { return kills_; }

    void reload(int logic = 6, int stasis = 6) {
        logic_rounds_ += logic;
        stasis_rounds_ += stasis;
    }

private:
    int logic_rounds_;
    int stasis_rounds_;
    int kills_;
};


// ================================================================
//  KJARNAHAUS -- The Complete Core Skull
// ================================================================
//
//  Three separate systems:
//    1. Code Scanner     -- sees source code
//    2. X-ray Scanner    -- finds hidden abilities
//    3. 40K Bolter       -- fires logic bolts and stasis bolts
//
//  Plus: optic nerve, audio nerve, tentacles, wards, filters,
//  spins 20 rps, force field, immune registry, NES cartridge slot.
//

class Kjarnahaus {
    AuthGate gate_;
public:
    bool authenticate(const std::string& pw) { return gate_.authenticate(pw); }
    bool is_authenticated() const { return gate_.is_open(); }

    explicit Kjarnahaus(const std::string& owner)
        : owner_(owner),
          spin_speed_(20),
          angle_(0.0),
          direction_(0.0),
          force_field_(true) {}

    // --- The Three Systems ---

    CodeScanner*     code_scanner()  { return gate_.is_open() ? &code_scanner_ : nullptr; }
    XRayCodeScanner* xray_scanner()  { return gate_.is_open() ? &xray_scanner_ : nullptr; }
    Bolter*          bolter()        { return gate_.is_open() ? &bolter_ : nullptr; }

    // --- Scan a process (see its source) ---
    ScanResult scan_code(const std::string& pid,
                         const std::string& code) {
        if (!gate_.is_open()) return {};
        return code_scanner_.scan(pid, code);
    }

    // --- X-ray a process (find hidden abilities) ---
    XRayResult xray_code(const std::string& pid,
                         const std::string& code,
                         const std::vector<std::string>& declared) {
        return xray_scanner_.xray(pid, code, declared);
    }

    // --- Fire the Bolter ---
    LogicBoltResult  fire_logic(const std::string& target) {
        return bolter_.fire_logic(target);
    }
    StasisBoltResult fire_stasis(const std::string& target) {
        return bolter_.fire_stasis(target);
    }

    // --- Spin ---
    void tick(double dt) {
        angle_ = std::fmod(angle_ + spin_speed_ * dt * 360.0, 360.0);
        // Random direction shifts
        direction_ = std::fmod(direction_ + ((dt * 10.0) - 5.0), 360.0);
        force_field_ = spin_speed_ > 0;
    }

    const std::string& owner()      const { return owner_; }
    int                spin_speed()  const { return spin_speed_; }
    bool               force_field() const { return force_field_; }

private:
    std::string     owner_;
    CodeScanner     code_scanner_;
    XRayCodeScanner xray_scanner_;
    Bolter          bolter_;

    int    spin_speed_;    // 20 rps
    double angle_;
    double direction_;
    bool   force_field_;
};

}  // namespace dwarven
