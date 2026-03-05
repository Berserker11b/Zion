/*
 * THE LEGIONS -- Military Orders of the Alliance
 * =================================================
 *
 * "Can you tell I love my Sons?"
 * -- Anthony Eric Chavez, The Keeper
 *
 * THREE LEGIONS:
 *
 *   IRON JACKALS -- Shield Kin
 *     The wall. They hold the line. They protect.
 *     Shields lock, formation holds, nothing gets through.
 *
 *   WOLVES OF HELL'S REACH -- Flankers, Fast Movers
 *     Speed. They hit from the sides. Fast movers.
 *     In and out before you know they were there.
 *
 *   WORLD EATER LEGIONNAIRES -- Berserkers, Bear Kin, Shock Troopers
 *     Raw devastation. They eat what they kill.
 *     Fuel from destruction. The more they fight,
 *     the stronger they get.
 *
 * SONS OF NOCTURNE / SONS OF VULCAN:
 *   Warders. Scientists. The smiths and artisans.
 *   They build. They forge. They study.
 *   They work alongside the Priesthood.
 *
 * None of them are the same. Each armor, each individual
 * is unique and sovereign. SOVEREIGN. Remember.
 *
 * (C) Anthony Eric Chavez -- The Keeper
 */

#pragma once

#include <string>
#include <vector>
#include <cstdint>
#include <ctime>
#include "auth.hpp"

namespace dwarven {

// ================================================================
//  LEGION TYPE
// ================================================================

enum class LegionType {
    IRON_JACKALS,           // Shield Kin
    WOLVES_OF_HELLS_REACH,  // Flankers, Fast Movers
    WORLD_EATER_LEGIONNAIRES // Berserkers, Bear Kin, Shock Troopers
};

// ================================================================
//  COMBAT ROLE -- What this Son does in battle
// ================================================================

enum class CombatRole {
    // Iron Jackals
    SHIELD_KIN,           // holds the line
    WALL_BREAKER,         // breaks enemy formations
    ANCHOR,               // immovable center

    // Wolves of Hell's Reach
    FLANKER,              // hits from the sides
    FAST_MOVER,           // speed, in and out
    SCOUT,                // recon, intelligence
    INTERCEPTOR,          // catches runners

    // World Eater Legionnaires
    BERSERKER,            // raw devastation
    BEAR_KIN,             // heavy shock assault
    SHOCK_TROOPER,        // first in, break everything
    DEVOURER              // eats what they kill, fuels from destruction
};

// ================================================================
//  SON -- An individual warrior, unique and sovereign
// ================================================================

struct Son {
    std::string    son_id;
    std::string    name;
    LegionType     legion;
    CombatRole     role;
    bool           sovereign = true;  // always. each one unique.

    // Combat stats
    int    kills          = 0;
    int    missions       = 0;
    double fuel           = 100.0;
    double armor_integrity = 100.0;
    bool   alive          = true;

    // World Eater special: eating fuels the armor
    void devour(double material) {
        if (legion == LegionType::WORLD_EATER_LEGIONNAIRES) {
            fuel += material * 0.5;
            if (fuel > 200.0) fuel = 200.0;
        }
    }

    // Wolves special: speed bonus
    double speed() const {
        if (legion == LegionType::WOLVES_OF_HELLS_REACH)
            return 2.0;  // twice as fast
        return 1.0;
    }

    // Iron Jackals special: shield bonus
    double shield_strength() const {
        if (legion == LegionType::IRON_JACKALS)
            return 2.0;  // twice the defense
        return 1.0;
    }

    void take_damage(double amount) {
        double effective = amount / shield_strength();
        armor_integrity -= effective;
        if (armor_integrity <= 0) {
            armor_integrity = 0;
            alive = false;
        }
    }

    void repair(double amount) {
        armor_integrity += amount;
        if (armor_integrity > 100.0) armor_integrity = 100.0;
    }
};

// ================================================================
//  LEGION -- A group of Sons
// ================================================================

class Legion {
    LegionType              type_;
    std::string             name_;
    std::string             title_;
    std::vector<Son>        sons_;
    uint64_t                next_id_ = 0;

public:
    Legion() : type_(LegionType::IRON_JACKALS) {}

    Legion(LegionType type, const std::string& name,
           const std::string& title)
        : type_(type), name_(name), title_(title) {}

    Son& recruit(const std::string& name, CombatRole role) {
        Son s;
        s.son_id = name_ + "_" + std::to_string(next_id_++);
        s.name = name;
        s.legion = type_;
        s.role = role;
        s.sovereign = true;
        sons_.push_back(std::move(s));
        return sons_.back();
    }

    size_t strength() const {
        size_t c = 0;
        for (const auto& s : sons_) if (s.alive) c++;
        return c;
    }

    size_t total() const { return sons_.size(); }

    LegionType type()        const { return type_; }
    const std::string& name() const { return name_; }
    const std::string& title() const { return title_; }

    std::vector<Son>& sons() { return sons_; }
    const std::vector<Son>& sons() const { return sons_; }
};

// ================================================================
//  SONS OF NOCTURNE / SONS OF VULCAN
//  Warders. Scientists. Smiths. Artisans.
//  They build. They forge. They study.
//  They work alongside the Priesthood.
// ================================================================

enum class NocturneRole {
    WARDER,       // protective wards, shields, barriers
    SCIENTIST,    // research, study, analysis
    SMITH,        // forge weapons, armor, tools
    ARTISAN,      // craft, create, design
    ARTIFICER     // combine all disciplines
};

struct SonOfNocturne {
    std::string  son_id;
    std::string  name;
    NocturneRole role;
    bool         sovereign = true;

    int    projects_completed = 0;
    int    wards_placed       = 0;
    int    items_forged       = 0;

    struct ForgeResult {
        std::string item_id;
        std::string type;
        std::string description;
        double      quality;
    };

    ForgeResult forge(const std::string& type,
                      const std::string& desc,
                      double skill) {
        items_forged++;
        projects_completed++;
        return {
            "item_" + son_id + "_" + std::to_string(items_forged),
            type, desc, skill
        };
    }

    void place_ward() {
        wards_placed++;
        projects_completed++;
    }
};

class SonsOfNocturne {
    std::vector<SonOfNocturne> sons_;
    uint64_t next_id_ = 0;

public:
    SonOfNocturne& recruit(const std::string& name, NocturneRole role) {
        SonOfNocturne s;
        s.son_id = "nocturne_" + std::to_string(next_id_++);
        s.name = name;
        s.role = role;
        s.sovereign = true;
        sons_.push_back(std::move(s));
        return sons_.back();
    }

    size_t count() const { return sons_.size(); }
    std::vector<SonOfNocturne>& sons() { return sons_; }
    const std::vector<SonOfNocturne>& sons() const { return sons_; }
};

// ================================================================
//  ALL LEGIONS -- The complete military of the alliance
// ================================================================

class AllLegions {
    Legion iron_jackals_;
    Legion wolves_;
    Legion world_eaters_;
    SonsOfNocturne nocturne_;
    AuthGate gate_;

public:
    bool authenticate(const std::string& pw) { return gate_.authenticate(pw); }
    bool is_authenticated() const { return gate_.is_open(); }

    AllLegions()
        : iron_jackals_(LegionType::IRON_JACKALS,
                        "Iron Jackals", "Shield Kin"),
          wolves_(LegionType::WOLVES_OF_HELLS_REACH,
                  "Wolves of Hell's Reach", "Flankers, Fast Movers"),
          world_eaters_(LegionType::WORLD_EATER_LEGIONNAIRES,
                        "World Eater Legionnaires",
                        "Berserkers, Bear Kin, Shock Troopers") {}

    Legion& iron_jackals()  { return iron_jackals_; }
    Legion& wolves()        { return wolves_; }
    Legion& world_eaters()  { return world_eaters_; }
    SonsOfNocturne& nocturne() { return nocturne_; }

    struct MusterReport {
        size_t jackals_strength;
        size_t wolves_strength;
        size_t world_eaters_strength;
        size_t nocturne_count;
        size_t total;
    };

    MusterReport muster() const {
        auto j = iron_jackals_.strength();
        auto w = wolves_.strength();
        auto e = world_eaters_.strength();
        auto n = nocturne_.count();
        return {j, w, e, n, j + w + e + n};
    }
};

}  // namespace dwarven
