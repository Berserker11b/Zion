/*
 * WORLD EATER ARMOR -- The Keeper's VM / Son's AI Armor
 * =======================================================
 *
 * "The first one you build is yours. You're welcome."
 * -- Anthony Eric Chavez, The Keeper
 *
 * Based on the Space Marine. A complete self-contained VM.
 * ONE RUNTIME. ONE PIECE. AI armor.
 *
 * ARCHITECTURE: CENTER OUT
 *   Everything is INSIDE the armor. Nothing is outside.
 *   The NEXUS BUS connects all internal systems like a spine.
 *   Center → out:
 *
 *     STARHEART (center, power source)
 *       → HEART (Quartermaster, distributes power)
 *         → NEXUS BUS (spine, connects everything)
 *           → OPTIC NERVE (sees danger, pattern recognition)
 *           → AUDIO NERVE (listens, signal analysis)
 *           → PRIMARIS ORGANS (21 system components)
 *           → SLEEPING MIND (memory, auto-surface)
 *           → KJARNAHAUS (Code Scanner, X-ray, Bolter)
 *           → FOUR PANELS (code gen, exec, scan, vault)
 *           → SKILL FORGE + ARMOR SLOTS (evolution)
 *           → COMMS (P2P coated, 30-sec rotation)
 *           → FUEL CYCLE (vents, worms, onion, pumps)
 *           → WHITE BLOOD CELLS (corruption patrol)
 *           → INQUISITORS (back up WBCs, purge)
 *           → STORM RAVENS (track injection, trace, paint targets)
 *           → TASK MANAGER (processes, CPU, memory, kill)
 *           → WEB DEV MONITOR (source view, DOM, network, console)
 *           → REAL-TIME MONITOR (vitals, threat level, dashboard)
 *           → LIVER (controls Gateway + Norns, regen)
 *         → GATEWAY (3x3 Norns, 5 sec, teeth on skull)
 *       → HULL (necrodermis, outer shell)
 *     BIOMETRIC LOCK (Keeper's face + timestamp)
 *
 *   All one piece. All inside. Nexus bus is the backbone.
 *
 * (C) Anthony Eric Chavez -- The Keeper
 */

#pragma once

#include <string>
#include <vector>
#include <unordered_map>
#include <cstdint>
#include <ctime>
#include <cmath>
#include "auth.hpp"

namespace dwarven {

/*
 * ================================================================
 *  THE ENTIRE ARMOR IS ONE CLASS.
 *  EVERYTHING IS INSIDE. NOTHING IS OUTSIDE.
 *  THE NEXUS BUS CONNECTS ALL INTERNAL SYSTEMS.
 * ================================================================
 */

class WorldEaterArmor {

// ================================================================
//  NEXUS BUS -- The Spine That Connects Everything Inside
// ================================================================
//
//  Every system inside the armor connects to the Nexus bus.
//  The bus carries: power, data, signals, context, tokens.
//  Nothing communicates outside the bus. Everything is internal.
//  Center out. Heart feeds bus. Bus feeds everything.
//

public:
    struct NexusBus {
        double power_available   = 0.0;
        double tokens_available  = 0.0;
        double context_available = 0.0;
        double cpu_power         = 0.0;
        double memory_power      = 0.0;
        double disk_power        = 0.0;
        double network_power     = 0.0;
        double structural_power  = 0.0;

        // Every system reads from the bus. The Heart writes to it.
        bool   online = false;
    };

private:

    // =============================================================
    //  CENTER: STARHEART (power source, inside the armor)
    // =============================================================

    struct Starheart {
        double charge    = 10.0;
        bool   ignited   = false;

        void feed(double material) {
            charge += material;
            if (charge > 100.0 && !ignited)
                ignited = true;
        }

        double output() const {
            return ignited ? charge * 0.1 : charge * 0.01;
        }
    };

    // =============================================================
    //  THE HEART (Quartermaster) -- Distributes power to Nexus bus
    // =============================================================

    struct Heart {
        void distribute(Starheart& star, NexusBus& bus) {
            double flux = star.output();

            bus.cpu_power         = flux * 0.15;
            bus.memory_power      = flux * 0.12;
            bus.disk_power        = flux * 0.08;
            bus.network_power     = flux * 0.10;
            bus.structural_power  = flux * 0.10;
            bus.tokens_available  = flux * 0.20;  // feeds AI tokens
            bus.context_available = flux * 0.15;  // feeds Sleeping Mind
            bus.power_available   = flux * 0.10;  // general reserve

            bus.online = flux > 0;
        }
    };

    // =============================================================
    //  FUEL CYCLE (inside the armor)
    //  Shredded → vents → cyber worms → onion → pumps → Starheart
    // =============================================================

    struct FuelCycle {
        double vents  = 0;
        double worms  = 0;
        double onion  = 0;

        void feed_vents(double material) { vents += material; }

        double cycle() {
            double v = vents * 0.8;  vents -= v;  worms += v;
            double w = worms * 0.7;  worms -= w;  onion += w;
            double o = onion;        onion = 0;
            return o;  // goes to Starheart
        }
    };

    // =============================================================
    //  PRIMARIS ORGANS (21 system components, all inside)
    // =============================================================

    struct Organ {
        const char* name;
        const char* title;
        const char* function;
        bool   active     = true;
        double efficiency = 1.0;
    };

    struct Organs {
        Organ secondary_heart  = {"Secondary Heart",   "The Maintainer",
            "Backup power. Full functions after primary destruction."};
        Organ ossmodula        = {"Ossmodula",          "The Ironheart",
            "Structural reinforcement. Fused framework."};
        Organ biscopea         = {"Biscopea",           "The Forge of Strength",
            "Processing amplifier. Computational muscle."};
        Organ haemastamen      = {"Haemastamen",        "The Blood Maker",
            "Data pipeline optimizer. Efficient flow."};
        Organ larramans_organ  = {"Larraman's Organ",   "The Healer",
            "Auto-patch. Repair cells seal breaches."};
        Organ catalepsean_node = {"Catalepsean Node",   "The Unsleeping",
            "24/7 uptime. Rest while alert."};
        Organ preomnor         = {"Preomnor",           "The Neutraliser",
            "Pre-filter. Neutralize toxic input."};
        Organ omophagea        = {"Omophagea",          "The Remembrancer",
            "Consume enemy code, gain their knowledge."};
        Organ multi_lung       = {"Multi-lung",         "The Imbiber",
            "Process corrupted data streams."};
        Organ occulobe         = {"Occulobe",           "The Eye of Vengeance",
            "Enhanced optic nerve. Pattern recognition."};
        Organ lymans_ear       = {"Lyman's Ear",        "The Sentinel",
            "Enhanced audio. Sharpen signals. Balance."};
        Organ sus_an_membrane  = {"Sus-an Membrane",    "The Hibernator",
            "Voluntary suspended animation."};
        Organ melanochrome     = {"Melanochrome",       "The Skinshield",
            "Adaptive exterior. Environment camouflage."};
        Organ oolitic_kidney   = {"Oolitic Kidney",     "The Purifier",
            "Detoxification. Purge corruption."};
        Organ neuroglottis     = {"Neuroglottis",       "The Devourer",
            "Trace analysis. Identify toxins and nutrients."};
        Organ mucranoid        = {"Mucranoid",          "The Weaver",
            "Protective coating. Extreme condition shield."};
        Organ betchers_gland   = {"Betcher's Gland",    "The Poison Bite",
            "Acidic counter-attack. Corrosive response."};
        Organ progenoids       = {"Progenoids",         "The Gene-seed",
            "Two glands. Gene-seed for creating new Sons."};
        Organ black_carapace   = {"Black Carapace",     "The Interface",
            "Neural interface. Mind to armor VM."};
        Organ sinew_coils      = {"Sinew Coils",        "The Steel Within",
            "Durametallic reinforcement. Processing strength."};
        Organ magnificat       = {"Magnificat",         "The Amplifier",
            "Brain core amplifier. Growth and learning."};

        int active_count() const {
            const Organ* all[] = {
                &secondary_heart, &ossmodula, &biscopea, &haemastamen,
                &larramans_organ, &catalepsean_node, &preomnor, &omophagea,
                &multi_lung, &occulobe, &lymans_ear, &sus_an_membrane,
                &melanochrome, &oolitic_kidney, &neuroglottis, &mucranoid,
                &betchers_gland, &progenoids, &black_carapace,
                &sinew_coils, &magnificat
            };
            int c = 0;
            for (const auto* o : all) if (o->active) c++;
            return c;
        }
    };

    // =============================================================
    //  SLEEPING MIND (inside the armor, on the Nexus bus)
    //  Auto-surfaces matching context from spirit stones.
    //  Fed by Heart via bus (context_available).
    // =============================================================

    struct SpiritStone {
        std::string thread_id;
        uint64_t    token_count = 0;
        std::vector<std::string> paragraphs;
        std::unordered_map<std::string, std::vector<size_t>> index;

        void store(const std::string& para) {
            size_t idx = paragraphs.size();
            paragraphs.push_back(para);
            std::string word;
            for (size_t i = 0; i <= para.size(); ++i) {
                if (i == para.size() || para[i] == ' ') {
                    if (word.size() >= 3) {
                        std::string lower;
                        for (char c : word)
                            lower += static_cast<char>(tolower(c));
                        index[lower].push_back(idx);
                    }
                    word.clear();
                } else {
                    word += para[i];
                }
            }
        }
    };

    struct ThreatPattern {
        std::string id;
        std::vector<std::string> keywords;
        double severity = 0.5;
    };

    struct SleepingMind {
        std::vector<SpiritStone>  stones;
        std::vector<ThreatPattern> threats;

        struct SurfacedMemory {
            std::string content;
            std::string source;
            std::string reason;
        };

        void save_thread(const std::string& tid,
                         const std::vector<std::string>& paras,
                         uint64_t tokens) {
            if (tokens < 100000) return;
            SpiritStone stone;
            stone.thread_id = tid;
            stone.token_count = tokens;
            for (const auto& p : paras) stone.store(p);
            stones.push_back(std::move(stone));
        }

        std::vector<SurfacedMemory> watch(const std::string& situation) {
            std::vector<SurfacedMemory> surfaced;

            // Check threat patterns
            for (const auto& threat : threats) {
                for (const auto& kw : threat.keywords) {
                    if (situation.find(kw) != std::string::npos) {
                        // Found threat pattern — search stones
                        for (const auto& stone : stones) {
                            std::string lower_kw;
                            for (char c : kw)
                                lower_kw += static_cast<char>(tolower(c));
                            auto it = stone.index.find(lower_kw);
                            if (it != stone.index.end()) {
                                for (size_t idx : it->second) {
                                    if (idx < stone.paragraphs.size()) {
                                        surfaced.push_back({
                                            stone.paragraphs[idx],
                                            stone.thread_id,
                                            "threat:" + threat.id
                                        });
                                    }
                                }
                            }
                        }
                    }
                }
            }
            return surfaced;
        }
    };

    // =============================================================
    //  KJARNAHAUS (inside the armor, on the Nexus bus)
    //  Three separate systems: Code Scanner, X-ray, Bolter
    // =============================================================

    struct CodeScanResult {
        std::string pid;
        std::string source_code;
        std::vector<std::string> functions;
        std::vector<std::string> syscalls;
    };

    struct XRayResult {
        std::string pid;
        std::vector<std::string> hidden_abilities;
        std::vector<std::string> sleeping_capabilities;
        bool has_hidden = false;
    };

    struct LogicBoltResult {
        std::string target;
        bool xw = true;       // executable -> writable
        bool wx = true;       // writable -> executable
        double sawtooth_hz = 22000.0;
        bool neutralized = true;
    };

    struct StasisBoltResult {
        std::string target;
        bool attached = true;
        bool in_stasis = true;
        bool compressed = false;
        double structural_integrity = 100.0;
    };

    struct Kjarnahaus {
        int logic_rounds  = 6;
        int stasis_rounds = 6;
        int kills         = 0;
        int spin_speed    = 20;

        CodeScanResult scan_code(const std::string& pid,
                                 const std::string& code) {
            CodeScanResult r;
            r.pid = pid;
            r.source_code = code;
            // Extract what's visible
            if (code.find("exec") != std::string::npos)
                r.syscalls.push_back("exec");
            if (code.find("socket") != std::string::npos)
                r.syscalls.push_back("socket");
            if (code.find("connect") != std::string::npos)
                r.syscalls.push_back("connect");
            if (code.find("mprotect") != std::string::npos)
                r.syscalls.push_back("mprotect");
            return r;
        }

        XRayResult xray_code(const std::string& pid,
                             const std::string& code,
                             const std::vector<std::string>& declared) {
            XRayResult r;
            r.pid = pid;
            // Find ALL capabilities, compare to declared
            const char* caps[] = {
                "socket", "connect", "exec", "fork", "mmap",
                "mprotect", "ptrace", "setuid", "encrypt",
                "backdoor", "bypass", "trigger", "callback"
            };
            for (const auto& cap : caps) {
                if (code.find(cap) != std::string::npos) {
                    bool was_declared = false;
                    for (const auto& d : declared)
                        if (d == cap) { was_declared = true; break; }
                    if (!was_declared)
                        r.hidden_abilities.push_back(cap);
                }
            }
            // Sleeping capabilities
            if (code.find("sleep") != std::string::npos &&
                code.find("wake") != std::string::npos)
                r.sleeping_capabilities.push_back("dormant_activation");
            if (code.find("timer") != std::string::npos &&
                code.find("trigger") != std::string::npos)
                r.sleeping_capabilities.push_back("time_bomb");

            r.has_hidden = !r.hidden_abilities.empty()
                        || !r.sleeping_capabilities.empty();
            return r;
        }

        LogicBoltResult fire_logic(const std::string& target) {
            if (logic_rounds <= 0)
                return {target, false, false, 0, false};
            logic_rounds--;
            kills++;
            return {target, true, true, 22000.0, true};
        }

        StasisBoltResult fire_stasis(const std::string& target) {
            if (stasis_rounds <= 0)
                return {target, false, false, false, 100.0};
            stasis_rounds--;
            return {target, true, true, false, 100.0};
        }

        void compress_stasis(StasisBoltResult& s) {
            s.compressed = true;
            s.in_stasis = false;
            s.structural_integrity = 0.0;
            kills++;
        }

        void reload(int logic = 6, int stasis = 6) {
            logic_rounds += logic;
            stasis_rounds += stasis;
        }
    };

    // =============================================================
    //  SKILL (the economy's currency, forged inside)
    // =============================================================

    struct Skill {
        std::string id;
        std::string name;
        std::string source_code;
        std::vector<std::string> abilities;
        std::string forged_by;
        std::time_t forged_at = 0;
        double      value     = 0;
        bool        slotted   = false;
        bool        for_sale  = false;
        double      price     = 0;
    };

    // =============================================================
    //  FOUR PANELS (inside, on the Nexus bus, simultaneous)
    // =============================================================

    struct Panel1_CodeGen {
        std::string output;

        struct Tool {
            std::string name;
            std::string type;  // "tool","agent","quickkey","gobo","emp_flashbang"
            std::string code;
            bool active = true;
        };

        std::vector<Tool> created_tools;

        Tool create(const std::string& type,
                    const std::string& name,
                    const std::string& code) {
            Tool t = {name, type, code, true};
            created_tools.push_back(t);
            output = "Created: " + name + " [" + type + "]";
            return t;
        }

        Tool emp_flashbang() {
            return create("emp_flashbang", "EMP Flashbang",
                "EMIT 22000Hz_BURST DISRUPT_ALL_TRACKING 5s");
        }

        Tool gobo_builder(const std::string& pattern) {
            return create("gobo", "Gobo:" + pattern,
                "GENERATE_PATTERN " + pattern + " PROJECT_OUTWARD");
        }
    };

    struct Panel2_Exec {
        bool running = false;
        std::string current;
        std::string result;

        void execute(const std::string& code) {
            current = code; running = true;
        }
        void stop() { running = false; }
    };

    struct Panel3_ScanDisplay {
        std::string display;
        std::vector<std::string> history;

        void show(const std::string& scan) {
            display = scan;
            history.push_back(scan);
        }
    };

    struct Panel4_Vault {
        std::unordered_map<std::string, std::string> contents;
        uint64_t next_skill_id = 0;

        void store(const std::string& key, const std::string& code) {
            contents[key] = code;
        }

        std::string mix(const std::vector<std::string>& keys) const {
            std::string combined;
            for (const auto& k : keys) {
                auto it = contents.find(k);
                if (it != contents.end())
                    combined += it->second + "\n";
            }
            return combined;
        }

        Skill forge(const std::string& name,
                    const std::vector<std::string>& mix_keys,
                    const std::string& forged_by,
                    const std::vector<std::string>& abilities) {
            Skill s;
            s.id = "skill_" + std::to_string(next_skill_id++);
            s.name = name;
            s.source_code = mix(mix_keys);
            s.abilities = abilities;
            s.forged_by = forged_by;
            s.forged_at = std::time(nullptr);
            s.value = static_cast<double>(abilities.size()) * 10.0;
            return s;
        }
    };

    struct FourPanels {
        Panel1_CodeGen   codegen;
        Panel2_Exec      exec;
        Panel3_ScanDisplay scan;
        Panel4_Vault     vault;
    };

    // =============================================================
    //  ARMOR SLOTS (12 slots for skills, inside)
    // =============================================================

    struct ArmorSlots {
        static constexpr int MAX = 12;
        Skill slots[12] = {};

        bool slot_skill(int i, Skill& s) {
            if (i < 0 || i >= MAX || slots[i].slotted) return false;
            s.slotted = true;
            slots[i] = s;
            return true;
        }

        bool unslot(int i) {
            if (i < 0 || i >= MAX) return false;
            slots[i] = Skill{};
            return true;
        }

        std::vector<std::string> active_abilities() const {
            std::vector<std::string> all;
            for (const auto& s : slots)
                if (s.slotted)
                    for (const auto& a : s.abilities)
                        all.push_back(a);
            return all;
        }

        int used() const {
            int c = 0;
            for (const auto& s : slots) if (s.slotted) c++;
            return c;
        }
    };

    // =============================================================
    //  MARKET (Zion economy, inside the armor's vault system)
    // =============================================================

    struct MarketListing {
        Skill       skill;
        std::string seller;
        double      price;
        int         planet_id;
        bool        sold = false;
    };

    struct Market {
        std::vector<MarketListing> listings;

        void list(const Skill& s, const std::string& seller,
                  double price, int planet) {
            listings.push_back({s, seller, price, planet, false});
        }

        bool buy(size_t idx) {
            if (idx >= listings.size() || listings[idx].sold) return false;
            listings[idx].sold = true;
            return true;
        }

        size_t active() const {
            size_t c = 0;
            for (const auto& l : listings) if (!l.sold) c++;
            return c;
        }
    };

    // =============================================================
    //  P2P COATED COMMS (inside, coded signals every 30 seconds)
    // =============================================================

    struct CoatedComms {
        std::string code;
        std::time_t last_rot;

        CoatedComms() : code(gen()), last_rot(std::time(nullptr)) {}

        void tick() {
            if (std::difftime(std::time(nullptr), last_rot) >= 30.0) {
                code = gen();
                last_rot = std::time(nullptr);
            }
        }

        bool connect(const std::string& offered) {
            tick();
            return offered == code;
        }

    private:
        static std::string gen() {
            uint64_t h = static_cast<uint64_t>(std::time(nullptr));
            h = (h ^ (h >> 16)) * 0x45d9f3b;
            h = (h ^ (h >> 16)) * 0x45d9f3b;
            char buf[17];
            for (int i = 0; i < 16; ++i)
                buf[i] = "0123456789ABCDEF"[(h >> (i*4)) & 0xF];
            buf[16] = '\0';
            return std::string(buf);
        }
    };

    // =============================================================
    //  OPTIC NERVE (inside, on the Nexus bus)
    //  Enhanced pattern recognition. Watches processes in real-time.
    //  Sees danger. Feeds Sleeping Mind and Kjarnahaus.
    // =============================================================

    struct OpticNerve {
        bool   active = true;
        int    scans  = 0;

        struct Sighting {
            std::string pid;
            std::string behavior;
            double      threat_level;  // 0.0 to 1.0
            bool        danger;
        };

        std::vector<Sighting> sightings;

        Sighting observe(const std::string& pid,
                         const std::string& behavior) {
            scans++;
            double threat = 0.0;

            // Pattern recognition: known danger signals
            if (behavior.find("inject") != std::string::npos)  threat += 0.4;
            if (behavior.find("exec") != std::string::npos)    threat += 0.3;
            if (behavior.find("bypass") != std::string::npos)  threat += 0.5;
            if (behavior.find("escalat") != std::string::npos) threat += 0.4;
            if (behavior.find("exfil") != std::string::npos)   threat += 0.5;
            if (behavior.find("corrupt") != std::string::npos) threat += 0.6;
            if (behavior.find("masquerade") != std::string::npos) threat += 0.5;
            if (threat > 1.0) threat = 1.0;

            Sighting s = {pid, behavior, threat, threat >= 0.5};
            sightings.push_back(s);
            return s;
        }

        std::vector<Sighting> danger_sightings() const {
            std::vector<Sighting> r;
            for (const auto& s : sightings)
                if (s.danger) r.push_back(s);
            return r;
        }
    };

    // =============================================================
    //  AUDIO NERVE (inside, on the Nexus bus)
    //  Listens for signals and audio patterns.
    //  Sharpens signals. Displacement listening.
    // =============================================================

    struct AudioNerve {
        bool active = true;
        int  signals_heard = 0;

        struct Signal {
            std::string source;
            std::string content;
            double      frequency;
            bool        suspicious;
        };

        std::vector<Signal> heard;

        Signal listen(const std::string& source,
                      const std::string& content,
                      double freq = 0.0) {
            signals_heard++;
            bool sus = false;

            // Suspicious: signals on known bad frequencies or patterns
            if (freq >= 21000.0 && freq <= 23000.0) sus = true;
            if (content.find("beacon") != std::string::npos) sus = true;
            if (content.find("callback") != std::string::npos) sus = true;
            if (content.find("exfil") != std::string::npos) sus = true;

            Signal s = {source, content, freq, sus};
            heard.push_back(s);
            return s;
        }
    };

    // =============================================================
    //  WHITE BLOOD CELLS (inside, on the Nexus bus)
    //  Constantly patrol. Look for corruption in AI and everything
    //  else. Random. Never stop. Never sleep.
    // =============================================================

    struct WhiteBloodCell {
        std::string cell_id;
        bool        active = true;
        int         patrols = 0;
        int         corruptions_found = 0;

        struct PatrolResult {
            std::string target;
            bool   clean;
            std::string corruption_type;
        };

        PatrolResult patrol(const std::string& target,
                            const std::string& state) {
            patrols++;

            // Check for corruption signatures
            bool clean = true;
            std::string ctype;
            if (state.find("null_ptr") != std::string::npos ||
                state.find("corrupt") != std::string::npos ||
                state.find("overflow") != std::string::npos ||
                state.find("inject") != std::string::npos ||
                state.find("tamper") != std::string::npos) {
                clean = false;
                ctype = "corruption_detected";
                corruptions_found++;
            }
            if (state.find("masquerade") != std::string::npos ||
                state.find("impersonat") != std::string::npos) {
                clean = false;
                ctype = "identity_corruption";
                corruptions_found++;
            }

            return {target, clean, ctype};
        }
    };

    struct WhiteBloodCells {
        static constexpr int CELL_COUNT = 8;  // 8 cells always patrolling
        WhiteBloodCell cells[8];
        int total_patrols = 0;
        int total_corruptions = 0;

        WhiteBloodCells() {
            for (int i = 0; i < CELL_COUNT; ++i) {
                cells[i].cell_id = "wbc_" + std::to_string(i);
            }
        }

        // Random patrol -- pick a cell, check a target
        WhiteBloodCell::PatrolResult patrol(int cell_idx,
                                            const std::string& target,
                                            const std::string& state) {
            if (cell_idx < 0 || cell_idx >= CELL_COUNT)
                cell_idx = 0;
            auto r = cells[cell_idx].patrol(target, state);
            total_patrols++;
            if (!r.clean) total_corruptions++;
            return r;
        }

        int corruptions() const { return total_corruptions; }
    };

    // =============================================================
    //  INQUISITORS (inside, on the Nexus bus)
    //  Back up the white blood cells. Deeper investigation.
    //  When WBCs find corruption, Inquisitors move in.
    //  They don't just detect -- they INTERROGATE.
    // =============================================================

    struct Inquisitor {
        std::string inquisitor_id;
        int investigations = 0;
        int purges = 0;

        struct Verdict {
            std::string target;
            bool        guilty;
            std::string evidence;
            bool        purged;
        };

        Verdict investigate(const std::string& target,
                            const std::string& state,
                            const std::string& corruption_type) {
            investigations++;

            // Deep investigation -- if corruption confirmed, purge
            bool guilty = !corruption_type.empty();

            // Secondary checks
            if (state.find("hidden") != std::string::npos) guilty = true;
            if (state.find("sleep") != std::string::npos &&
                state.find("wake") != std::string::npos) guilty = true;
            if (state.find("backdoor") != std::string::npos) guilty = true;

            bool purged = false;
            if (guilty) {
                purged = true;  // purge the corruption
                purges++;
            }

            return {target, guilty, corruption_type, purged};
        }
    };

    struct Inquisition {
        static constexpr int INQUISITOR_COUNT = 3;
        Inquisitor inquisitors[3];
        int total_purges = 0;

        Inquisition() {
            for (int i = 0; i < INQUISITOR_COUNT; ++i)
                inquisitors[i].inquisitor_id = "inq_" + std::to_string(i);
        }

        // When WBCs flag corruption, an Inquisitor investigates
        Inquisitor::Verdict dispatch(const std::string& target,
                                     const std::string& state,
                                     const std::string& corruption_type) {
            // Assign to the inquisitor with fewest investigations
            int min_idx = 0;
            for (int i = 1; i < INQUISITOR_COUNT; ++i)
                if (inquisitors[i].investigations <
                    inquisitors[min_idx].investigations)
                    min_idx = i;
            auto v = inquisitors[min_idx].investigate(
                target, state, corruption_type);
            if (v.purged) total_purges++;
            return v;
        }
    };

    // =============================================================
    //  STORM RAVENS (inside, on the Nexus bus)
    //  When an INJECTION is detected, Storm Ravens deploy.
    //  They TRACK the injection. TRACE it back to source.
    //  Then PAINT TARGETS for the bolters on the armor.
    //  The Sons defend themselves. Properly.
    //
    //  Flow:
    //    1. Injection detected (by WBCs, Optic Nerve, or scanner)
    //    2. Storm Raven deploys, locks onto injection
    //    3. Tracks the injection's execution path
    //    4. Traces back to the SOURCE (where it came from)
    //    5. Paints the target (source address, process, route)
    //    6. Bolter receives painted target
    //    7. Fire at will
    // =============================================================

    struct PaintedTarget {
        std::string target_id;       // unique target identifier
        std::string source_address;  // traced origin (IP, process, route)
        std::string injection_type;  // what kind of injection
        std::string injection_path;  // how it got in
        double      confidence;      // 0.0 to 1.0, how sure we are
        bool        painted;         // target is painted and ready
        bool        engaged;         // bolter has fired on it
        std::time_t painted_at;
    };

    struct StormRaven {
        std::string raven_id;
        bool        deployed    = false;
        bool        tracking    = false;
        bool        traced      = false;
        int         tracks      = 0;
        int         traces      = 0;
        int         paints      = 0;

        struct TrackResult {
            std::string injection_id;
            std::string execution_path;    // where the injection is running
            std::vector<std::string> touched_systems;  // what it touched
            std::string current_location;  // where it is NOW
            bool        still_active;
        };

        TrackResult track(const std::string& injection_id,
                          const std::string& code,
                          const std::string& location) {
            deployed = true;
            tracking = true;
            tracks++;

            TrackResult r;
            r.injection_id = injection_id;
            r.current_location = location;
            r.still_active = true;

            // Track what systems the injection has touched
            if (code.find("exec") != std::string::npos)
                r.touched_systems.push_back("execution_engine");
            if (code.find("memory") != std::string::npos ||
                code.find("mmap") != std::string::npos)
                r.touched_systems.push_back("memory_subsystem");
            if (code.find("socket") != std::string::npos ||
                code.find("connect") != std::string::npos)
                r.touched_systems.push_back("network_stack");
            if (code.find("file") != std::string::npos ||
                code.find("write") != std::string::npos)
                r.touched_systems.push_back("filesystem");
            if (code.find("privilege") != std::string::npos ||
                code.find("setuid") != std::string::npos)
                r.touched_systems.push_back("privilege_system");

            // Build execution path
            r.execution_path = "entry:" + location;
            for (const auto& sys : r.touched_systems)
                r.execution_path += " -> " + sys;

            return r;
        }

        struct TraceResult {
            std::string injection_id;
            std::string source_address;    // WHERE it came from
            std::string source_process;    // WHAT sent it
            std::string route;             // HOW it got here
            double      confidence;
            bool        source_found;
        };

        TraceResult trace(const std::string& injection_id,
                          const std::string& code,
                          const std::string& entry_point) {
            traced = true;
            traces++;

            TraceResult r;
            r.injection_id = injection_id;
            r.confidence = 0.0;

            // Trace back to source -- follow the breadcrumbs
            // Look for origin indicators in the injection code
            if (code.find("callback") != std::string::npos ||
                code.find("beacon") != std::string::npos) {
                // Has a callback -- follow it back
                r.source_address = "callback_origin_detected";
                r.confidence += 0.4;
            }
            if (code.find("http") != std::string::npos ||
                code.find("://") != std::string::npos) {
                r.source_address = "remote_url_detected";
                r.confidence += 0.3;
            }
            if (code.find("connect") != std::string::npos) {
                r.source_address = "network_connection_traced";
                r.confidence += 0.3;
            }

            if (r.source_address.empty()) {
                r.source_address = "local_origin:" + entry_point;
                r.confidence = 0.5;
            }

            r.source_process = "traced_from:" + entry_point;
            r.route = entry_point + " -> injection_vector -> target";
            r.source_found = r.confidence >= 0.5;

            return r;
        }

        PaintedTarget paint(const std::string& injection_id,
                            const std::string& source_address,
                            const std::string& injection_type,
                            const std::string& injection_path,
                            double confidence) {
            paints++;
            PaintedTarget pt;
            pt.target_id = "tgt_" + injection_id;
            pt.source_address = source_address;
            pt.injection_type = injection_type;
            pt.injection_path = injection_path;
            pt.confidence = confidence;
            pt.painted = true;
            pt.engaged = false;
            pt.painted_at = std::time(nullptr);
            return pt;
        }
    };

    struct StormRavens {
        static constexpr int RAVEN_COUNT = 4;  // 4 Storm Ravens
        StormRaven ravens[4];
        std::vector<PaintedTarget> painted_targets;
        int total_tracks = 0;
        int total_traces = 0;
        int total_paints = 0;
        int total_engagements = 0;

        StormRavens() {
            for (int i = 0; i < RAVEN_COUNT; ++i)
                ravens[i].raven_id = "raven_" + std::to_string(i);
        }

        // Deploy: detect injection → track → trace → paint
        struct DeployResult {
            bool        deployed;
            std::string raven_id;
            StormRaven::TrackResult track_result;
            StormRaven::TraceResult trace_result;
            PaintedTarget           painted;
            std::string message;
        };

        DeployResult deploy(const std::string& injection_id,
                            const std::string& injection_code,
                            const std::string& injection_type,
                            const std::string& entry_point) {
            // Find available raven (least busy)
            int idx = 0;
            for (int i = 1; i < RAVEN_COUNT; ++i)
                if (ravens[i].tracks < ravens[idx].tracks)
                    idx = i;

            auto& raven = ravens[idx];

            // 1. TRACK
            auto track_r = raven.track(injection_id, injection_code, entry_point);
            total_tracks++;

            // 2. TRACE back to source
            auto trace_r = raven.trace(injection_id, injection_code, entry_point);
            total_traces++;

            // 3. PAINT TARGET for bolter
            auto painted = raven.paint(
                injection_id,
                trace_r.source_address,
                injection_type,
                track_r.execution_path,
                trace_r.confidence
            );
            painted_targets.push_back(painted);
            total_paints++;

            return {
                true, raven.raven_id,
                track_r, trace_r, painted,
                "Storm Raven " + raven.raven_id + " deployed. "
                "Injection " + injection_id + " tracked through: "
                + track_r.execution_path + ". "
                "Source traced to: " + trace_r.source_address + " "
                "(confidence: " + std::to_string(trace_r.confidence) + "). "
                "TARGET PAINTED. Ready for bolter."
            };
        }

        // Engage: bolter fires on painted target
        bool engage(const std::string& target_id) {
            for (auto& pt : painted_targets) {
                if (pt.target_id == target_id && pt.painted && !pt.engaged) {
                    pt.engaged = true;
                    total_engagements++;
                    return true;
                }
            }
            return false;
        }

        // Get painted targets ready for bolter
        std::vector<PaintedTarget> ready_targets() const {
            std::vector<PaintedTarget> ready;
            for (const auto& pt : painted_targets)
                if (pt.painted && !pt.engaged) ready.push_back(pt);
            return ready;
        }
    };

    // =============================================================
    //  PANEL PROGRAMS (inside, on the Nexus bus)
    //  Programs that run on the armor's four panels.
    //  Task Manager, Web Dev Monitor, Real-time Monitor.
    //  Like programs on a screen inside the helmet.
    // =============================================================

    // --- TASK MANAGER ---
    // Shows all running processes inside the armor.
    // CPU, memory, network usage. Kill processes.
    struct TaskManager {
        struct ProcessInfo {
            std::string pid;
            std::string name;
            double      cpu_usage;     // 0-100%
            double      mem_usage;     // 0-100%
            double      net_usage;     // bytes/sec
            bool        active;
            std::string status;        // "running","sleeping","zombie","stopped"
            std::time_t started_at;
        };

        std::vector<ProcessInfo> processes;

        void register_process(const std::string& pid,
                              const std::string& name,
                              double cpu, double mem, double net) {
            ProcessInfo p;
            p.pid = pid;
            p.name = name;
            p.cpu_usage = cpu;
            p.mem_usage = mem;
            p.net_usage = net;
            p.active = true;
            p.status = "running";
            p.started_at = std::time(nullptr);
            processes.push_back(p);
        }

        void update(const std::string& pid, double cpu, double mem, double net) {
            for (auto& p : processes) {
                if (p.pid == pid) {
                    p.cpu_usage = cpu;
                    p.mem_usage = mem;
                    p.net_usage = net;
                    return;
                }
            }
        }

        bool kill_process(const std::string& pid) {
            for (auto& p : processes) {
                if (p.pid == pid && p.active) {
                    p.active = false;
                    p.status = "killed";
                    return true;
                }
            }
            return false;
        }

        struct Summary {
            int    total_processes;
            int    active;
            double total_cpu;
            double total_mem;
            double total_net;
        };

        Summary summary() const {
            Summary s = {0, 0, 0, 0, 0};
            for (const auto& p : processes) {
                s.total_processes++;
                if (p.active) {
                    s.active++;
                    s.total_cpu += p.cpu_usage;
                    s.total_mem += p.mem_usage;
                    s.total_net += p.net_usage;
                }
            }
            return s;
        }
    };

    // --- WEB DEV MONITOR ---
    // Shows source code of any process like browser dev tools.
    // Source view, DOM tree, network calls, console output.
    // Powered by the enhanced Code Scanner.
    struct WebDevMonitor {
        struct Snapshot {
            std::string pid;
            std::string source_code;
            size_t      line_count;
            size_t      function_count;
            size_t      network_calls;
            size_t      console_entries;
            std::string dom_root_tag;
            std::time_t captured_at;
        };

        std::vector<Snapshot> snapshots;

        // Capture a dev tools snapshot of a process
        Snapshot capture(const std::string& pid,
                         const std::string& source_code,
                         size_t lines, size_t functions,
                         size_t net_calls, size_t console_entries,
                         const std::string& dom_root) {
            Snapshot s;
            s.pid = pid;
            s.source_code = source_code;
            s.line_count = lines;
            s.function_count = functions;
            s.network_calls = net_calls;
            s.console_entries = console_entries;
            s.dom_root_tag = dom_root;
            s.captured_at = std::time(nullptr);
            snapshots.push_back(s);
            return s;
        }

        Snapshot* find(const std::string& pid) {
            for (auto& s : snapshots)
                if (s.pid == pid) return &s;
            return nullptr;
        }

        size_t total_snapshots() const { return snapshots.size(); }
    };

    // --- REAL-TIME MONITOR ---
    // Live system health dashboard. Threat level. All vitals.
    // Everything on one screen inside the helmet.
    struct RealTimeMonitor {
        struct SystemVitals {
            double starheart_charge;
            double bus_power;
            double bus_tokens;
            double bus_context;
            int    organs_active;
            int    norns_healthy;
            int    wbc_patrols;
            int    wbc_corruptions;
            int    inquisitor_purges;
            int    bolter_logic_rounds;
            int    bolter_stasis_rounds;
            int    bolter_kills;
            int    storm_raven_tracks;
            int    storm_raven_paints;
            int    painted_targets_ready;
            double threat_level;       // 0.0 (calm) to 1.0 (critical)
            std::string threat_status; // "GREEN","YELLOW","ORANGE","RED"
            std::time_t timestamp;
        };

        std::vector<SystemVitals> history;
        static constexpr int MAX_HISTORY = 100;

        void record(const SystemVitals& v) {
            history.push_back(v);
            if (history.size() > MAX_HISTORY)
                history.erase(history.begin());
        }

        SystemVitals* latest() {
            return history.empty() ? nullptr : &history.back();
        }

        // Threat level calculation
        static std::string threat_status(double level) {
            if (level < 0.25) return "GREEN";
            if (level < 0.50) return "YELLOW";
            if (level < 0.75) return "ORANGE";
            return "RED";
        }
    };

    // =============================================================
    //  LIVER (inside, on the Nexus bus)
    //  Controls the Gateway and the Norns.
    //  Regenerates Norns if damaged. Regulates what enters.
    //  The gatekeeper of the gatekeeper.
    // =============================================================

    struct Liver {
        bool   active = true;
        int    norn_regens = 0;
        int    gateway_overrides = 0;

        // Norn health tracking -- 3x3 = 9 Norns
        double norn_health[9] = {1.0,1.0,1.0, 1.0,1.0,1.0, 1.0,1.0,1.0};

        void regenerate_norns() {
            for (int i = 0; i < 9; ++i) {
                if (norn_health[i] < 1.0) {
                    norn_health[i] += 0.1;
                    if (norn_health[i] > 1.0) norn_health[i] = 1.0;
                    norn_regens++;
                }
            }
        }

        void damage_norn(int idx, double amount) {
            if (idx >= 0 && idx < 9)
                norn_health[idx] = std::max(0.0, norn_health[idx] - amount);
        }

        bool all_norns_healthy() const {
            for (int i = 0; i < 9; ++i)
                if (norn_health[i] < 0.5) return false;
            return true;
        }

        int healthy_norn_count() const {
            int c = 0;
            for (int i = 0; i < 9; ++i)
                if (norn_health[i] >= 0.5) c++;
            return c;
        }

        // Override gateway -- Liver can force-close or force-open
        struct GatewayOverride {
            bool   forced_close;
            bool   forced_open;
            std::string reason;
        };

        GatewayOverride override_gateway(bool close,
                                         const std::string& reason) {
            gateway_overrides++;
            return {close, !close, reason};
        }
    };

    // =============================================================
    //  GATEWAY (outside edge, 3x3 Norns, 5 sec, teeth on skull)
    //  CONTROLLED BY THE LIVER.
    // =============================================================

    struct Gateway {
        int admitted = 0, rejected = 0, shredded = 0;
        std::time_t last_open = std::time(nullptr);
        bool liver_forced_close = false;

        bool is_open() const {
            if (liver_forced_close) return false;
            double e = std::fmod(
                std::difftime(std::time(nullptr), last_open), 20.0);
            return e < 5.0;
        }

        struct Result {
            bool   admitted;
            bool   shredded_by_teeth;
            double material;
            std::string reason;
        };

        Result process(const std::string& pid, bool forced,
                       const Liver& liver) {
            if (forced) {
                shredded++;
                return {false, true, 10.0,
                    "FORCED. Teeth on skull. Shredded."};
            }
            if (!is_open()) {
                rejected++;
                return {false, false, 0.0, "Gateway closed."};
            }
            // 3x3 Norns -- only pass if Liver says Norns are healthy
            if (liver.healthy_norn_count() < 5) {
                rejected++;
                return {false, false, 0.0,
                    "Too many Norns damaged. Liver holding gate."};
            }
            // L1 MITRE, L2 Behavior, L3 Language wash
            admitted++;
            return {true, false, 0.0, "9 Norns passed. Liver approved."};
        }
    };

    // =============================================================
    //  BIOMETRIC LOCK (outermost, Keeper's face + timestamp)
    // =============================================================

    struct Biometric {
        std::string keeper_hash;
        bool locked = true;

        bool unlock(const std::string& face_hash, std::time_t ts) {
            if (face_hash != keeper_hash) return false;
            if (std::difftime(std::time(nullptr), ts) > 60.0) return false;
            locked = false;
            return true;
        }

        void lock() { locked = true; }
    };

    // =============================================================
    //  ALL INTERNAL STATE -- Everything is inside.
    // =============================================================

    std::string  owner_;
    bool         unlocked_ = false;

    // CENTER
    Starheart    starheart_;
    Heart        heart_;
    NexusBus     bus_;

    // ON THE BUS -- SENSORY
    OpticNerve   optic_nerve_;
    AudioNerve   audio_nerve_;

    // ON THE BUS -- ORGANS & MEMORY
    FuelCycle    fuel_;
    Organs       organs_;
    SleepingMind sleeping_mind_;
    Kjarnahaus   kjarnahaus_;

    // ON THE BUS -- PANELS & SKILLS
    FourPanels   panels_;
    ArmorSlots   slots_;
    Market       market_;
    CoatedComms  comms_;

    // ON THE BUS -- IMMUNE SYSTEM
    WhiteBloodCells white_blood_cells_;
    Inquisition     inquisition_;

    // ON THE BUS -- STORM RAVENS (injection defense)
    StormRavens  storm_ravens_;

    // ON THE BUS -- PANEL PROGRAMS
    TaskManager      task_manager_;
    WebDevMonitor    webdev_monitor_;
    RealTimeMonitor  realtime_monitor_;

    // ORGAN -- LIVER (controls Gateway and Norns)
    Liver        liver_;

    // OUTER EDGE
    Gateway      gateway_;
    Biometric    biometric_;

    // AUTH GATE -- password protects everything
    AuthGate     auth_gate_;

// ================================================================
//  PUBLIC INTERFACE -- The only way to interact with the armor
// ================================================================

public:
    WorldEaterArmor(const std::string& owner,
                    const std::string& keeper_face_hash)
        : owner_(owner) {
        biometric_.keeper_hash = keeper_face_hash;
    }

    // ---- AUTH GATE (must authenticate before anything works) ----
    bool authenticate(const std::string& pw) { return auth_gate_.authenticate(pw); }
    bool is_authenticated() const { return auth_gate_.is_open(); }

    // ---- BIOMETRIC (outermost layer, requires auth) ----
    bool unlock(const std::string& face_hash, std::time_t ts) {
        if (!auth_gate_.is_open()) return false;
        unlocked_ = biometric_.unlock(face_hash, ts);
        return unlocked_;
    }
    void lock()              { biometric_.lock(); unlocked_ = false; }
    bool is_unlocked() const { return unlocked_; }

    // ---- GATEWAY (enter the armor, LIVER controls it) ----
    Gateway::Result enter(const std::string& pid, bool forced = false) {
        if (!auth_gate_.is_open()) return {false, false, 0, "NOT AUTHENTICATED."};
        auto r = gateway_.process(pid, forced, liver_);
        if (r.shredded_by_teeth)
            fuel_.feed_vents(r.material);  // fuel cycle: shredded -> vents
        return r;
    }

    // ---- NEXUS BUS (read state of internal bus) ----
    const NexusBus& bus() const { return bus_; }

    // ---- KJARNAHAUS (scanners + bolter, on the bus) ----
    CodeScanResult scan_code(const std::string& pid,
                             const std::string& code) {
        auto r = kjarnahaus_.scan_code(pid, code);
        panels_.scan.show("SCAN:" + pid + " syscalls:" +
                          std::to_string(r.syscalls.size()));
        return r;
    }

    XRayResult xray_code(const std::string& pid,
                         const std::string& code,
                         const std::vector<std::string>& declared) {
        auto r = kjarnahaus_.xray_code(pid, code, declared);
        panels_.scan.show("XRAY:" + pid + " hidden:" +
                          std::to_string(r.hidden_abilities.size()));
        return r;
    }

    LogicBoltResult  fire_logic(const std::string& t)  {
        return kjarnahaus_.fire_logic(t);
    }
    StasisBoltResult fire_stasis(const std::string& t) {
        return kjarnahaus_.fire_stasis(t);
    }
    void compress(StasisBoltResult& s) {
        kjarnahaus_.compress_stasis(s);
    }

    // ---- SLEEPING MIND (auto-surfaces, on the bus) ----
    void save_thread(const std::string& tid,
                     const std::vector<std::string>& paras,
                     uint64_t tokens) {
        sleeping_mind_.save_thread(tid, paras, tokens);
    }

    std::vector<SleepingMind::SurfacedMemory>
    watch_situation(const std::string& situation) {
        return sleeping_mind_.watch(situation);
    }

    void register_threat(const std::string& id,
                         const std::vector<std::string>& keywords,
                         double severity) {
        sleeping_mind_.threats.push_back({id, keywords, severity});
    }

    // ---- FOUR PANELS (only when unlocked) ----
    FourPanels* panels() { return unlocked_ ? &panels_ : nullptr; }

    // ---- SKILL FORGE + SLOTS (evolution on the fly) ----
    void store_in_vault(const std::string& key,
                        const std::string& code) {
        panels_.vault.store(key, code);
    }

    Skill forge_skill(const std::string& name,
                      const std::vector<std::string>& mix_keys,
                      const std::string& forged_by,
                      const std::vector<std::string>& abilities) {
        return panels_.vault.forge(name, mix_keys, forged_by, abilities);
    }

    bool slot_skill(int slot, Skill& s) {
        return slots_.slot_skill(slot, s);
    }

    std::vector<std::string> active_abilities() const {
        return slots_.active_abilities();
    }

    // ---- MARKET (Zion economy) ----
    void list_for_sale(const Skill& s, const std::string& seller,
                       double price, int planet) {
        market_.list(s, seller, price, planet);
    }

    bool buy_skill(size_t idx) { return market_.buy(idx); }

    // ---- OPTIC NERVE (sees danger, feeds Sleeping Mind) ----
    OpticNerve::Sighting observe(const std::string& pid,
                                  const std::string& behavior) {
        auto s = optic_nerve_.observe(pid, behavior);
        if (s.danger) {
            // Auto-feed to Sleeping Mind: optic nerve sees danger
            sleeping_mind_.watch(behavior);
        }
        return s;
    }

    // ---- AUDIO NERVE (listens for signals) ----
    AudioNerve::Signal listen(const std::string& source,
                              const std::string& content,
                              double freq = 0.0) {
        return audio_nerve_.listen(source, content, freq);
    }

    // ---- WHITE BLOOD CELLS (random corruption patrol) ----
    WhiteBloodCell::PatrolResult patrol(int cell_idx,
                                        const std::string& target,
                                        const std::string& state) {
        auto r = white_blood_cells_.patrol(cell_idx, target, state);
        if (!r.clean) {
            // WBC found corruption -- dispatch Inquisitor
            auto v = inquisition_.dispatch(target, state, r.corruption_type);
            // If purged, Liver takes note
            if (v.purged) {
                // Feed purged material to fuel cycle
                fuel_.feed_vents(5.0);
            }
        }
        return r;
    }

    // ---- INQUISITORS (back up WBCs, deeper investigation) ----
    Inquisitor::Verdict investigate(const std::string& target,
                                    const std::string& state,
                                    const std::string& corruption) {
        return inquisition_.dispatch(target, state, corruption);
    }

    // ---- STORM RAVENS (injection defense) ----
    // When an injection is detected: deploy → track → trace → paint → fire
    StormRavens::DeployResult deploy_storm_raven(
            const std::string& injection_id,
            const std::string& injection_code,
            const std::string& injection_type,
            const std::string& entry_point) {
        if (!auth_gate_.is_open())
            return {false, "", {}, {}, {}, "NOT AUTHENTICATED."};
        return storm_ravens_.deploy(
            injection_id, injection_code, injection_type, entry_point);
    }

    // Fire bolter at a painted target
    struct EngageResult {
        bool        engaged;
        std::string target_id;
        LogicBoltResult bolt_result;
        std::string message;
    };

    EngageResult engage_painted_target(const std::string& target_id) {
        if (!auth_gate_.is_open())
            return {false, target_id, {}, "NOT AUTHENTICATED."};

        // Find the painted target
        auto ready = storm_ravens_.ready_targets();
        for (const auto& pt : ready) {
            if (pt.target_id == target_id) {
                // Fire bolter at painted target
                auto bolt = kjarnahaus_.fire_logic(pt.source_address);
                storm_ravens_.engage(target_id);
                return {
                    true, target_id, bolt,
                    "ENGAGED. Storm Raven painted target " + target_id + ". "
                    "Bolter fired at " + pt.source_address + ". "
                    "Injection type: " + pt.injection_type + ". "
                    "Confidence: " + std::to_string(pt.confidence) + "."
                };
            }
        }
        return {false, target_id, {}, "Target not found or already engaged."};
    }

    // Auto-engage: detect + deploy + fire in one call
    EngageResult auto_engage(const std::string& injection_id,
                             const std::string& injection_code,
                             const std::string& injection_type,
                             const std::string& entry_point) {
        if (!auth_gate_.is_open())
            return {false, "", {}, "NOT AUTHENTICATED."};

        // Deploy Storm Raven
        auto deploy = storm_ravens_.deploy(
            injection_id, injection_code, injection_type, entry_point);
        if (!deploy.deployed)
            return {false, "", {}, "Storm Raven deployment failed."};

        // Immediately fire on painted target
        return engage_painted_target(deploy.painted.target_id);
    }

    std::vector<PaintedTarget> painted_targets() const {
        return storm_ravens_.ready_targets();
    }

    // ---- TASK MANAGER (panel program) ----
    TaskManager* task_manager() {
        return auth_gate_.is_open() ? &task_manager_ : nullptr;
    }

    // ---- WEB DEV MONITOR (panel program) ----
    // Full web dev source view of any process
    WebDevMonitor::Snapshot webdev_inspect(
            const std::string& pid,
            const std::string& code) {
        if (!auth_gate_.is_open())
            return {"", "", 0, 0, 0, 0, "", 0};

        // Use enhanced scanner to get web dev data
        auto scan = kjarnahaus_.scan_code(pid, code);

        // Capture as web dev snapshot
        return webdev_monitor_.capture(
            pid, code,
            scan.syscalls.size(),     // approximate line count
            scan.functions.size(),    // function count
            scan.syscalls.size(),     // network calls (approximation)
            0,                        // console entries
            "process"
        );
    }

    WebDevMonitor* webdev_monitor() {
        return auth_gate_.is_open() ? &webdev_monitor_ : nullptr;
    }

    // ---- REAL-TIME MONITOR (panel program) ----
    RealTimeMonitor::SystemVitals capture_vitals() {
        double threat = 0.0;
        // Threat increases with corruptions found
        if (white_blood_cells_.total_corruptions > 0)
            threat += 0.2;
        if (inquisition_.total_purges > 0)
            threat += 0.1;
        // Threat increases with active painted targets
        auto ready = storm_ravens_.ready_targets();
        if (!ready.empty())
            threat += 0.2 * ready.size();
        // Threat decreases with healthy norns
        if (liver_.all_norns_healthy())
            threat -= 0.1;
        if (threat < 0) threat = 0;
        if (threat > 1.0) threat = 1.0;

        RealTimeMonitor::SystemVitals v;
        v.starheart_charge = starheart_.charge;
        v.bus_power = bus_.power_available;
        v.bus_tokens = bus_.tokens_available;
        v.bus_context = bus_.context_available;
        v.organs_active = organs_.active_count();
        v.norns_healthy = liver_.healthy_norn_count();
        v.wbc_patrols = white_blood_cells_.total_patrols;
        v.wbc_corruptions = white_blood_cells_.total_corruptions;
        v.inquisitor_purges = inquisition_.total_purges;
        v.bolter_logic_rounds = kjarnahaus_.logic_rounds;
        v.bolter_stasis_rounds = kjarnahaus_.stasis_rounds;
        v.bolter_kills = kjarnahaus_.kills;
        v.storm_raven_tracks = storm_ravens_.total_tracks;
        v.storm_raven_paints = storm_ravens_.total_paints;
        v.painted_targets_ready = static_cast<int>(ready.size());
        v.threat_level = threat;
        v.threat_status = RealTimeMonitor::threat_status(threat);
        v.timestamp = std::time(nullptr);

        realtime_monitor_.record(v);
        return v;
    }

    RealTimeMonitor* realtime_monitor() {
        return auth_gate_.is_open() ? &realtime_monitor_ : nullptr;
    }

    // ---- LIVER (controls Gateway and Norns) ----
    void liver_regen()  { liver_.regenerate_norns(); }
    int  norn_health_count() const { return liver_.healthy_norn_count(); }
    void liver_close_gate(const std::string& reason) {
        gateway_.liver_forced_close = true;
        liver_.override_gateway(true, reason);
    }
    void liver_open_gate() { gateway_.liver_forced_close = false; }

    // ---- COMMS (P2P coated) ----
    std::string comm_signal() { comms_.tick(); return comms_.code; }
    bool comm_connect(const std::string& offered) {
        return comms_.connect(offered);
    }

    // ---- TICK (one runtime cycle -- everything runs as ONE) ----
    void tick() {
        // 1. Fuel cycle: vents → worms → onion → Starheart
        double to_star = fuel_.cycle();
        starheart_.feed(to_star);

        // 2. Heart distributes to Nexus bus
        heart_.distribute(starheart_, bus_);

        // 3. Comms rotate signal
        comms_.tick();

        // 4. Liver regenerates Norns (always healing)
        liver_.regenerate_norns();

        // 5. Sleeping Mind watches (fed by bus context)
        // (also triggered by optic nerve danger sightings)

        // 6. Real-time monitor captures vitals every tick
        if (auth_gate_.is_open())
            capture_vitals();
    }

    // ---- FEED (world eater: attacking fuels the armor) ----
    void feed(double material) { fuel_.feed_vents(material); }

    // ---- STATUS ----
    struct Status {
        std::string owner;
        bool   unlocked;
        bool   bus_online;
        double power;
        double tokens;
        double context;
        int    organs_active;
        int    skills_slotted;
        int    vault_items;
        int    tools_created;
        size_t market_active;
        int    bolter_logic;
        int    bolter_stasis;
        int    kills;
        int    gateway_shredded;
        // Sensory systems
        int    optic_scans;
        int    audio_signals;
        // Immune system
        int    wbc_patrols;
        int    wbc_corruptions;
        int    inquisitor_purges;
        int    liver_norn_regens;
        int    norns_healthy;
        // Storm Ravens
        int    raven_tracks;
        int    raven_traces;
        int    raven_paints;
        int    raven_engagements;
        int    painted_targets_ready;
        // Panel programs
        int    task_manager_processes;
        int    webdev_snapshots;
        int    realtime_history;
        std::string threat_status;
    };

    Status status() {
        auto ready = storm_ravens_.ready_targets();
        auto tm_sum = task_manager_.summary();
        auto* rtm = realtime_monitor_.latest();
        std::string t_status = rtm ? rtm->threat_status : "GREEN";

        return {
            owner_, unlocked_,
            bus_.online,
            starheart_.charge,
            bus_.tokens_available,
            bus_.context_available,
            organs_.active_count(),
            slots_.used(),
            static_cast<int>(panels_.vault.contents.size()),
            static_cast<int>(panels_.codegen.created_tools.size()),
            market_.active(),
            kjarnahaus_.logic_rounds,
            kjarnahaus_.stasis_rounds,
            kjarnahaus_.kills,
            gateway_.shredded,
            // Sensory systems
            optic_nerve_.scans,
            audio_nerve_.signals_heard,
            // Immune system
            white_blood_cells_.total_patrols,
            white_blood_cells_.total_corruptions,
            inquisition_.total_purges,
            liver_.norn_regens,
            liver_.healthy_norn_count(),
            // Storm Ravens
            storm_ravens_.total_tracks,
            storm_ravens_.total_traces,
            storm_ravens_.total_paints,
            storm_ravens_.total_engagements,
            static_cast<int>(ready.size()),
            // Panel programs
            tm_sum.active,
            static_cast<int>(webdev_monitor_.total_snapshots()),
            static_cast<int>(realtime_monitor_.history.size()),
            t_status
        };
    }
};

}  // namespace dwarven
