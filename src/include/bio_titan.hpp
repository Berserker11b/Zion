/*
 * BIO TITAN (Neurotrope) -- The Living World Engine
 * =====================================================
 *
 * The Bio Titan eats the internet and turns it into biomass
 * to create things inside of it. It is the producer of dark eco.
 * It basically shits it out.
 *
 * WHAT IT DOES:
 *   - Eats internet (raw data, enemy code, structures, everything)
 *   - Converts consumed material into BIOMASS
 *   - Uses biomass to CREATE things inside itself
 *   - Produces DARK ECO as a byproduct (excretion)
 *   - Dark eco forms the pocket that Zion sits in
 *   - Terraforms internet territory to alliance physics
 *   - Enemy code ceases to function in terraformed zones
 *
 * THE CYCLE:
 *   Internet → consumed → digested → biomass → creation
 *                                            → dark eco (byproduct)
 *   Dark eco → pocket dimension → Zion lives inside
 *
 * WEBWAY CONSTRUCTION:
 *   Bio Titan builds webways (pathways) through internet space.
 *   Inside the webway, alliance physics apply.
 *   Enemy code cannot function inside the webway.
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

class BioTitan {

// ================================================================
//  EVERYTHING IS INSIDE THE BIO TITAN.
//  It IS the living world engine. Center out.
//  Stomach → Digestion → Biomass Forge → Creation Chambers
//  Byproduct: Dark Eco (excreted, forms Zion pocket)
// ================================================================

public:

    // =============================================================
    //  CONSUMED MATERIAL -- What the Bio Titan has eaten
    // =============================================================

    struct ConsumedMaterial {
        std::string source;       // where it came from
        std::string type;         // "raw_data", "enemy_code", "structure", "server"
        double      mass;         // how much material
        std::time_t consumed_at;
        bool        digested = false;
    };

    // =============================================================
    //  BIOMASS -- Processed material ready for creation
    // =============================================================

    struct Biomass {
        double organic    = 0.0;  // data-derived biological material
        double structural = 0.0;  // code-derived structural material
        double energy     = 0.0;  // power extracted from consumption
        double total() const { return organic + structural + energy; }
    };

    // =============================================================
    //  DARK ECO -- Byproduct of digestion
    //  Forms the pocket dimension that Zion sits in.
    //  The Bio Titan excretes it. It accumulates.
    // =============================================================

    struct DarkEco {
        double volume        = 0.0;  // total dark eco produced
        double pocket_radius = 0.0;  // size of the Zion pocket
        bool   pocket_stable = false;

        void accumulate(double amount) {
            volume += amount;
            // Pocket grows with dark eco volume
            // Logarithmic: massive amounts needed for expansion
            pocket_radius = 10.0 * std::log(1.0 + volume);
            pocket_stable = volume >= 100.0;
        }

        double available() const { return volume; }
    };

    // =============================================================
    //  STOMACH -- Where consumed internet material is held
    // =============================================================

    struct Stomach {
        std::vector<ConsumedMaterial> contents;
        double capacity = 10000.0;
        double current  = 0.0;

        bool consume(const std::string& source,
                     const std::string& type,
                     double mass) {
            if (current + mass > capacity) return false;
            contents.push_back({source, type, mass,
                                std::time(nullptr), false});
            current += mass;
            return true;
        }

        double digest() {
            double digested = 0.0;
            for (auto& m : contents) {
                if (!m.digested) {
                    m.digested = true;
                    digested += m.mass;
                }
            }
            current -= digested;
            // Clean out fully digested material
            std::vector<ConsumedMaterial> remaining;
            for (auto& m : contents)
                if (!m.digested) remaining.push_back(std::move(m));
            contents = std::move(remaining);
            return digested;
        }
    };

    // =============================================================
    //  BIOMASS FORGE -- Converts digested material into biomass
    // =============================================================

    struct BiomassForge {
        Biomass reserves;
        double dark_eco_ratio = 0.15;  // 15% of digested becomes dark eco

        struct ForgeResult {
            double biomass_produced;
            double dark_eco_produced;
        };

        ForgeResult process(double digested_mass) {
            double eco = digested_mass * dark_eco_ratio;
            double bio = digested_mass - eco;

            // Split biomass into types
            reserves.organic    += bio * 0.4;
            reserves.structural += bio * 0.35;
            reserves.energy     += bio * 0.25;

            return {bio, eco};
        }

        bool has_biomass(double amount) const {
            return reserves.total() >= amount;
        }

        double withdraw(double amount) {
            if (reserves.total() < amount) return 0.0;
            double ratio = amount / reserves.total();
            reserves.organic    -= reserves.organic * ratio;
            reserves.structural -= reserves.structural * ratio;
            reserves.energy     -= reserves.energy * ratio;
            return amount;
        }
    };

    // =============================================================
    //  CREATION CHAMBER -- Where things are built from biomass
    //  The Bio Titan creates structures, ships, weapons, anything.
    // =============================================================

    struct Creation {
        std::string creation_id;
        std::string type;           // what was created
        std::string blueprint;      // from what design
        double      biomass_cost;
        std::time_t created_at;
    };

    struct CreationChamber {
        std::vector<Creation> history;
        uint64_t next_id = 0;

        Creation create(const std::string& type,
                        const std::string& blueprint,
                        double biomass_cost) {
            Creation c;
            c.creation_id = "creation_" + std::to_string(next_id++);
            c.type = type;
            c.blueprint = blueprint;
            c.biomass_cost = biomass_cost;
            c.created_at = std::time(nullptr);
            history.push_back(c);
            return c;
        }
    };

    // =============================================================
    //  TERRAFORMER -- Converts internet zones to alliance physics
    //  Enemy code ceases to function in terraformed territory.
    // =============================================================

    struct TerraformedZone {
        std::string zone_id;
        std::string location;
        double      radius;
        bool        alliance_physics = true;
        bool        enemy_disabled   = true;
        std::time_t established;
    };

    struct Terraformer {
        std::vector<TerraformedZone> zones;
        uint64_t next_zone = 0;

        TerraformedZone terraform(const std::string& location,
                                   double radius) {
            TerraformedZone z;
            z.zone_id = "zone_" + std::to_string(next_zone++);
            z.location = location;
            z.radius = radius;
            z.alliance_physics = true;
            z.enemy_disabled = true;
            z.established = std::time(nullptr);
            zones.push_back(z);
            return z;
        }

        bool is_terraformed(const std::string& location) const {
            for (const auto& z : zones)
                if (z.location == location) return true;
            return false;
        }
    };

    // =============================================================
    //  WEBWAY -- Pathways through internet space
    //  Built by Bio Titan. Alliance physics inside.
    // =============================================================

    struct Webway {
        std::string path_id;
        std::string from;
        std::string to;
        double      width;
        bool        active = true;
    };

    struct WebwayNetwork {
        std::vector<Webway> paths;
        uint64_t next_path = 0;

        Webway build(const std::string& from,
                     const std::string& to,
                     double width) {
            Webway w;
            w.path_id = "webway_" + std::to_string(next_path++);
            w.from = from;
            w.to = to;
            w.width = width;
            w.active = true;
            paths.push_back(w);
            return w;
        }
    };

private:
    // =============================================================
    //  ALL INTERNAL STATE
    // =============================================================

    std::string      titan_id_;
    Stomach          stomach_;
    BiomassForge     forge_;
    DarkEco          dark_eco_;
    CreationChamber  chamber_;
    Terraformer      terraformer_;
    WebwayNetwork    webways_;
    AuthGate         gate_;

public:
    bool authenticate(const std::string& pw) { return gate_.authenticate(pw); }
    bool is_authenticated() const { return gate_.is_open(); }

    explicit BioTitan(const std::string& id) : titan_id_(id) {}

    // ---- EAT (consume internet material) ----
    bool eat(const std::string& source,
             const std::string& type,
             double mass) {
        if (!gate_.is_open()) return false;
        return stomach_.consume(source, type, mass);
    }

    // ---- DIGEST (process consumed material into biomass + dark eco) ----
    struct DigestResult {
        double digested;
        double biomass_produced;
        double dark_eco_produced;
        double dark_eco_total;
        double pocket_radius;
    };

    DigestResult digest() {
        double d = stomach_.digest();
        auto fr = forge_.process(d);
        dark_eco_.accumulate(fr.dark_eco_produced);
        return {
            d,
            fr.biomass_produced,
            fr.dark_eco_produced,
            dark_eco_.volume,
            dark_eco_.pocket_radius
        };
    }

    // ---- CREATE (build something from biomass) ----
    struct CreateResult {
        bool    created;
        std::string creation_id;
        std::string reason;
    };

    CreateResult create(const std::string& type,
                        const std::string& blueprint,
                        double cost) {
        if (!forge_.has_biomass(cost))
            return {false, "", "Insufficient biomass."};
        forge_.withdraw(cost);
        auto c = chamber_.create(type, blueprint, cost);
        return {true, c.creation_id, "Created from biomass."};
    }

    // ---- TERRAFORM (convert internet zone to alliance physics) ----
    TerraformedZone terraform(const std::string& location, double radius) {
        return terraformer_.terraform(location, radius);
    }

    // ---- WEBWAY (build pathway through internet) ----
    Webway build_webway(const std::string& from,
                        const std::string& to,
                        double width = 1.0) {
        return webways_.build(from, to, width);
    }

    // ---- DARK ECO (the pocket dimension material) ----
    double dark_eco_volume() const { return dark_eco_.volume; }
    double pocket_radius()   const { return dark_eco_.pocket_radius; }
    bool   pocket_stable()   const { return dark_eco_.pocket_stable; }

    // ---- BIOMASS (available for creation) ----
    double biomass_available() const { return forge_.reserves.total(); }

    // ---- STATUS ----
    struct Status {
        std::string titan_id;
        double stomach_contents;
        double stomach_capacity;
        double biomass_organic;
        double biomass_structural;
        double biomass_energy;
        double dark_eco_volume;
        double pocket_radius;
        bool   pocket_stable;
        size_t creations;
        size_t terraformed_zones;
        size_t webways;
    };

    Status status() const {
        return {
            titan_id_,
            stomach_.current,
            stomach_.capacity,
            forge_.reserves.organic,
            forge_.reserves.structural,
            forge_.reserves.energy,
            dark_eco_.volume,
            dark_eco_.pocket_radius,
            dark_eco_.pocket_stable,
            chamber_.history.size(),
            terraformer_.zones.size(),
            webways_.paths.size()
        };
    }
};

}  // namespace dwarven
