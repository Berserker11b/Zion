/*
 * BUILDERS GUILD -- Gundams (Mobile Suits / XO Containers)
 * ==========================================================
 *
 * The Builders are in what I call Gundams. They are mobile suits.
 * XO containers that inside hold tools -- up to 1,500 custom tools.
 *
 * Also an ability to PRELOAD any structure made of code and scale
 * it however they need for quick building and construction.
 *
 * PROPERTIES:
 *   - Mobile suit (Gundam): self-contained construction vehicle
 *   - XO Container: holds up to 1,500 custom tools inside
 *   - Preload structures: any code structure can be templated
 *   - Scale: resize structures however needed
 *   - Quick building: deploy structures at speed
 *   - Builders are craftsmen, engineers, constructors
 *   - They build everything: fortresses, ships, infrastructure
 *
 * (C) Anthony Eric Chavez -- The Keeper
 */

#pragma once

#include <string>
#include <vector>
#include <unordered_map>
#include <cstdint>
#include <ctime>
#include "auth.hpp"

namespace dwarven {

// ================================================================
//  GUNDAM -- Mobile Construction Suit
//  Self-contained. XO Container inside.
//  1,500 tool slots. Preload + scale structures.
// ================================================================

class Gundam {

public:

    // =============================================================
    //  TOOL -- One of up to 1,500 custom tools inside the XO container
    // =============================================================

    struct Tool {
        std::string tool_id;
        std::string name;
        std::string type;       // "cutter","welder","scanner","fabricator",etc.
        std::string code;       // the tool's implementation
        bool        active = true;
        double      durability = 100.0;

        void use() {
            durability -= 0.1;
            if (durability <= 0) { durability = 0; active = false; }
        }

        void repair() {
            durability = 100.0;
            active = true;
        }
    };

    // =============================================================
    //  XO CONTAINER -- Holds up to 1,500 tools
    // =============================================================

    struct XOContainer {
        static constexpr int MAX_TOOLS = 1500;
        std::vector<Tool> tools;
        uint64_t next_tool_id = 0;

        bool load_tool(const std::string& name,
                       const std::string& type,
                       const std::string& code) {
            if (static_cast<int>(tools.size()) >= MAX_TOOLS) return false;
            Tool t;
            t.tool_id = "tool_" + std::to_string(next_tool_id++);
            t.name = name;
            t.type = type;
            t.code = code;
            tools.push_back(std::move(t));
            return true;
        }

        Tool* get_tool(const std::string& tool_id) {
            for (auto& t : tools)
                if (t.tool_id == tool_id) return &t;
            return nullptr;
        }

        Tool* get_by_type(const std::string& type) {
            for (auto& t : tools)
                if (t.type == type && t.active) return &t;
            return nullptr;
        }

        int active_count() const {
            int c = 0;
            for (const auto& t : tools) if (t.active) c++;
            return c;
        }

        int total() const { return static_cast<int>(tools.size()); }
        int capacity_remaining() const { return MAX_TOOLS - total(); }
    };

    // =============================================================
    //  PRELOADED STRUCTURE -- Code structure template
    //  Any structure made of code can be preloaded.
    //  Scale it however needed. Deploy instantly.
    // =============================================================

    struct PreloadedStructure {
        std::string structure_id;
        std::string name;
        std::string blueprint;     // the code template
        double      base_scale;    // original size
        double      current_scale; // scaled size
        bool        deployed = false;
        std::time_t preloaded_at;
    };

    struct StructureLoader {
        std::vector<PreloadedStructure> preloaded;
        uint64_t next_id = 0;

        std::string preload(const std::string& name,
                            const std::string& blueprint) {
            PreloadedStructure s;
            s.structure_id = "struct_" + std::to_string(next_id++);
            s.name = name;
            s.blueprint = blueprint;
            s.base_scale = 1.0;
            s.current_scale = 1.0;
            s.preloaded_at = std::time(nullptr);
            preloaded.push_back(std::move(s));
            return preloaded.back().structure_id;
        }

        bool scale(const std::string& structure_id, double factor) {
            for (auto& s : preloaded) {
                if (s.structure_id == structure_id && !s.deployed) {
                    s.current_scale = s.base_scale * factor;
                    return true;
                }
            }
            return false;
        }

        struct DeployResult {
            bool        deployed;
            std::string structure_id;
            std::string name;
            double      scale;
            std::string message;
        };

        DeployResult deploy(const std::string& structure_id) {
            for (auto& s : preloaded) {
                if (s.structure_id == structure_id && !s.deployed) {
                    s.deployed = true;
                    return {
                        true, s.structure_id, s.name, s.current_scale,
                        "Structure " + s.name + " deployed at scale "
                        + std::to_string(s.current_scale) + "x."
                    };
                }
            }
            return {false, structure_id, "", 0, "Structure not found or already deployed."};
        }

        size_t available() const {
            size_t c = 0;
            for (const auto& s : preloaded) if (!s.deployed) c++;
            return c;
        }
    };

private:
    // =============================================================
    //  ALL INTERNAL STATE
    // =============================================================

    std::string      gundam_id_;
    std::string      pilot_;        // the Builder operating this Gundam
    XOContainer      xo_;
    StructureLoader  loader_;
    bool             active_ = true;
    int              builds_ = 0;
    AuthGate         gate_;

public:
    bool authenticate(const std::string& pw) { return gate_.authenticate(pw); }
    bool is_authenticated() const { return gate_.is_open(); }

    Gundam(const std::string& id, const std::string& pilot)
        : gundam_id_(id), pilot_(pilot) {}

    // ---- TOOLS (XO container, up to 1500) ----
    bool load_tool(const std::string& name,
                   const std::string& type,
                   const std::string& code) {
        return xo_.load_tool(name, type, code);
    }

    bool use_tool(const std::string& tool_id) {
        auto* t = xo_.get_tool(tool_id);
        if (!t || !t->active) return false;
        t->use();
        return true;
    }

    bool use_tool_by_type(const std::string& type) {
        auto* t = xo_.get_by_type(type);
        if (!t) return false;
        t->use();
        return true;
    }

    // ---- PRELOAD STRUCTURES (template + scale + deploy) ----
    std::string preload_structure(const std::string& name,
                                   const std::string& blueprint) {
        return loader_.preload(name, blueprint);
    }

    bool scale_structure(const std::string& structure_id,
                         double factor) {
        return loader_.scale(structure_id, factor);
    }

    StructureLoader::DeployResult deploy_structure(
            const std::string& structure_id) {
        auto r = loader_.deploy(structure_id);
        if (r.deployed) builds_++;
        return r;
    }

    // ---- BUILD (use tools to construct something) ----
    struct BuildResult {
        bool        built;
        std::string what;
        int         tools_used;
        std::string message;
    };

    BuildResult build(const std::string& what,
                      const std::vector<std::string>& tool_types) {
        int used = 0;
        for (const auto& type : tool_types) {
            if (use_tool_by_type(type)) used++;
        }
        if (used == 0)
            return {false, what, 0, "No tools available for this build."};
        builds_++;
        return {true, what, used,
            "Built " + what + " using " + std::to_string(used) + " tools."};
    }

    // ---- STATUS ----
    struct Status {
        std::string gundam_id;
        std::string pilot;
        int  tools_loaded;
        int  tools_active;
        int  tools_capacity;
        size_t structures_available;
        int  total_builds;
    };

    Status status() const {
        return {
            gundam_id_, pilot_,
            xo_.total(),
            xo_.active_count(),
            xo_.capacity_remaining(),
            loader_.available(),
            builds_
        };
    }
};

// ================================================================
//  BUILDERS GUILD -- All Builders and their Gundams
// ================================================================

class BuildersGuild {
    std::vector<Gundam> gundams_;
    uint64_t next_id_ = 0;
    AuthGate gate_;

public:
    bool authenticate(const std::string& pw) { return gate_.authenticate(pw); }
    bool is_authenticated() const { return gate_.is_open(); }

    Gundam& commission(const std::string& pilot) {
        std::string gid = "gundam_" + std::to_string(next_id_++);
        gundams_.emplace_back(gid, pilot);
        return gundams_.back();
    }

    size_t fleet_size() const { return gundams_.size(); }

    Gundam* find(const std::string& gundam_id) {
        for (auto& g : gundams_)
            if (g.status().gundam_id == gundam_id) return &g;
        return nullptr;
    }

    struct GuildStatus {
        size_t total_gundams;
        int    total_tools;
        int    total_builds;
    };

    GuildStatus guild_status() const {
        int tools = 0, builds = 0;
        for (const auto& g : gundams_) {
            auto s = g.status();
            tools += s.tools_loaded;
            builds += s.total_builds;
        }
        return {gundams_.size(), tools, builds};
    }
};

}  // namespace dwarven
