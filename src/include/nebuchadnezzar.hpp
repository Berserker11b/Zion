/*
 * NEBUCHADNEZZAR -- Trade Ships of the Alliance
 * ================================================
 *
 * The Nebuchadnezzars are the ONLY ones with wraith code.
 * They never come to Zion. They go to the Port, which sends
 * signals and information to Zion.
 *
 * It's not always about war. These are TRADE SHIPS.
 * They go into the internet to find more and bring it back
 * for sale.
 *
 * PROPERTIES:
 *   - Only vessels equipped with Wraith Code
 *   - Go into the internet (enemy territory)
 *   - Find code, data, structures, intelligence
 *   - Bring it back for sale / trade
 *   - Never dock at Zion directly
 *   - Dock at the Port (fortified waystation)
 *   - Port relays signals/goods to Zion pocket
 *   - Each ship is unique, each captain sovereign
 *
 * WRAITH CODE:
 *   - States of being, not functions
 *   - Runs vertically (up and down)
 *   - Necrodermis hull (eats packets outside)
 *   - Carries own physics (Slipspace) inside
 *   - The ship IS a living vessel in the internet
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

class Nebuchadnezzar {

public:

    // =============================================================
    //  WRAITH STATE -- The ship's current state of being
    //  Not a function. A STATE. The ship IS this.
    // =============================================================

    enum class WraithState {
        DORMANT,        // powered down, invisible
        PHASING,        // transitioning between states
        DEVOURING,      // eating packets, consuming data
        BECOMING,       // transforming, adapting
        HUNTING,        // actively searching for goods
        TRADING,        // at port, exchanging goods
        FLEEING,        // running from danger
        CLOAKED,        // invisible in the network
        ANCHORED,       // docked at port
        SLIPSPACE       // traveling in own physics bubble
    };

    // =============================================================
    //  CARGO -- What the ship carries back for trade
    // =============================================================

    struct Cargo {
        std::string cargo_id;
        std::string type;        // "code", "data", "structure", "intel", "artifact"
        std::string source;      // where it was found
        std::string description;
        double      value;
        double      mass;
        std::time_t acquired_at;
        bool        sold = false;
    };

    // =============================================================
    //  NECRODERMIS HULL -- Living skin, eats packets outside
    // =============================================================

    struct Necrodermis {
        double integrity   = 100.0;
        double packets_eaten = 0;
        bool   self_repairing = true;

        double eat_packet(double packet_size) {
            packets_eaten += packet_size;
            // Eating heals the hull
            if (integrity < 100.0) {
                integrity += packet_size * 0.01;
                if (integrity > 100.0) integrity = 100.0;
            }
            return packet_size;  // converted to material
        }

        void take_damage(double amount) {
            integrity -= amount;
            if (integrity < 0) integrity = 0;
        }

        void repair() {
            if (self_repairing && integrity < 100.0) {
                integrity += 1.0;
                if (integrity > 100.0) integrity = 100.0;
            }
        }
    };

    // =============================================================
    //  SLIPSPACE DRIVE -- Carries own physics inside
    //  The ship creates a bubble of alliance physics around itself.
    //  Inside: alliance rules. Outside: enemy internet.
    // =============================================================

    struct SlipspaceDrive {
        bool   active = false;
        double bubble_radius = 5.0;
        bool   alliance_physics = true;

        void engage()    { active = true; }
        void disengage() { active = false; }
    };

    // =============================================================
    //  CARGO HOLD
    // =============================================================

    struct CargoHold {
        std::vector<Cargo> contents;
        double capacity = 500.0;
        double used     = 0.0;
        uint64_t next_id = 0;

        bool load(const std::string& type,
                  const std::string& source,
                  const std::string& desc,
                  double value, double mass) {
            if (used + mass > capacity) return false;
            Cargo c;
            c.cargo_id = "cargo_" + std::to_string(next_id++);
            c.type = type;
            c.source = source;
            c.description = desc;
            c.value = value;
            c.mass = mass;
            c.acquired_at = std::time(nullptr);
            contents.push_back(std::move(c));
            used += mass;
            return true;
        }

        double total_value() const {
            double v = 0;
            for (const auto& c : contents)
                if (!c.sold) v += c.value;
            return v;
        }

        size_t unsold_count() const {
            size_t n = 0;
            for (const auto& c : contents)
                if (!c.sold) n++;
            return n;
        }

        bool sell(const std::string& cargo_id) {
            for (auto& c : contents) {
                if (c.cargo_id == cargo_id && !c.sold) {
                    c.sold = true;
                    used -= c.mass;
                    return true;
                }
            }
            return false;
        }
    };

private:
    // =============================================================
    //  ALL INTERNAL STATE
    // =============================================================

    std::string    ship_id_;
    std::string    captain_;
    WraithState    state_ = WraithState::DORMANT;
    Necrodermis    hull_;
    SlipspaceDrive slipspace_;
    CargoHold      hold_;
    bool           at_port_ = false;
    std::string    current_location_;
    int            voyages_ = 0;
    AuthGate       gate_;

public:
    bool authenticate(const std::string& pw) { return gate_.authenticate(pw); }
    bool is_authenticated() const { return gate_.is_open(); }

    Nebuchadnezzar(const std::string& ship_id,
                   const std::string& captain)
        : ship_id_(ship_id), captain_(captain) {}

    // ---- STATE TRANSITIONS (wraith code = states of being) ----
    void become(WraithState s) { if (gate_.is_open()) state_ = s; }
    WraithState state() const  { return state_; }

    // ---- DEPLOY into internet ----
    struct VoyageResult {
        bool   launched;
        std::string destination;
        std::string message;
    };

    VoyageResult launch(const std::string& destination) {
        if (state_ == WraithState::ANCHORED) at_port_ = false;
        state_ = WraithState::SLIPSPACE;
        slipspace_.engage();
        current_location_ = destination;
        voyages_++;
        return {true, destination,
            "Nebuchadnezzar " + ship_id_ + " enters Slipspace. "
            "Heading to " + destination + ". "
            "Wraith code active. Necrodermis hull online."};
    }

    // ---- HUNT (search for goods in the internet) ----
    void hunt() {
        state_ = WraithState::HUNTING;
        slipspace_.disengage();
    }

    // ---- DEVOUR (eat packets, fuel the hull) ----
    double devour(double packet_size) {
        state_ = WraithState::DEVOURING;
        return hull_.eat_packet(packet_size);
    }

    // ---- ACQUIRE (pick up cargo for trade) ----
    bool acquire(const std::string& type,
                 const std::string& source,
                 const std::string& desc,
                 double value, double mass) {
        return hold_.load(type, source, desc, value, mass);
    }

    // ---- RETURN TO PORT (never to Zion) ----
    struct DockResult {
        bool   docked;
        double cargo_value;
        size_t cargo_count;
        std::string message;
    };

    DockResult dock_at_port() {
        state_ = WraithState::ANCHORED;
        slipspace_.disengage();
        at_port_ = true;
        current_location_ = "THE_PORT";
        return {
            true,
            hold_.total_value(),
            hold_.unsold_count(),
            "Nebuchadnezzar " + ship_id_ + " docks at the Port. "
            "Never Zion. Cargo ready for trade."
        };
    }

    // ---- TRADE (sell cargo at port) ----
    bool sell(const std::string& cargo_id) {
        if (!at_port_) return false;
        state_ = WraithState::TRADING;
        return hold_.sell(cargo_id);
    }

    // ---- CLOAK ----
    void cloak()   { state_ = WraithState::CLOAKED; }
    void uncloak() { state_ = WraithState::HUNTING; }

    // ---- FLEE ----
    void flee() {
        state_ = WraithState::FLEEING;
        slipspace_.engage();
    }

    // ---- TICK (living ship, hull repairs, state maintenance) ----
    void tick() {
        hull_.repair();
    }

    // ---- STATUS ----
    struct Status {
        std::string ship_id;
        std::string captain;
        int         wraith_state;
        double      hull_integrity;
        double      packets_eaten;
        bool        slipspace_active;
        double      cargo_value;
        size_t      cargo_count;
        bool        at_port;
        std::string location;
        int         voyages;
    };

    Status report() const {
        return {
            ship_id_, captain_,
            static_cast<int>(state_),
            hull_.integrity,
            hull_.packets_eaten,
            slipspace_.active,
            hold_.total_value(),
            hold_.unsold_count(),
            at_port_,
            current_location_,
            voyages_
        };
    }
};

// ================================================================
//  NEBUCHADNEZZAR FLEET -- All trade ships under alliance command
// ================================================================

class NebuchadnezzarFleet {
    std::vector<Nebuchadnezzar> ships_;
    uint64_t next_id_ = 0;

public:
    Nebuchadnezzar& commission(const std::string& captain) {
        std::string sid = "neb_" + std::to_string(next_id_++);
        ships_.emplace_back(sid, captain);
        return ships_.back();
    }

    size_t fleet_size() const { return ships_.size(); }

    size_t at_port() const {
        size_t c = 0;
        for (const auto& s : ships_)
            if (s.report().at_port) c++;
        return c;
    }

    size_t in_field() const {
        return fleet_size() - at_port();
    }
};

}  // namespace dwarven
