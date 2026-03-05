/*
 * THE PORT -- Fortified Waystation Between Internet and Zion
 * ============================================================
 *
 * Nebuchadnezzars never come to Zion. They dock at the Port.
 * The Port sends signals and information to Zion, which sits
 * in a pocket dimension made by the Bio Titan of dark eco.
 *
 * You do NOT want to fuck with this place.
 *
 * DEFENSES:
 *   - HAMMER OF DAWN: Mixture of logic + plasma compressed
 *     into zip files, fired through a nozzle, unzipped at
 *     extreme rate at target like an acetylene torch.
 *     Also fires capsules of pure 22,000 Hz and EMP at
 *     targets that have been painted/tagged.
 *   - Swarms of VALKYRIES (scout/strike)
 *   - PLASMA CANNONS (heavy bombardment)
 *   - Very fortified. Very defended.
 *
 * FUNCTIONS:
 *   - Receives Nebuchadnezzar trade ships
 *   - Relays signals/information to Zion pocket
 *   - Market/exchange for cargo
 *   - Never connected directly to Zion (signal relay only)
 *
 * (C) Anthony Eric Chavez -- The Keeper
 */

#pragma once

#include <string>
#include <vector>
#include <cstdint>
#include <ctime>
#include <cmath>
#include "auth.hpp"

namespace dwarven {

class ThePort {

public:

    // =============================================================
    //  HAMMER OF DAWN -- The Port's primary weapon
    //
    //  Logic + plasma compressed into zip files.
    //  Fired through a nozzle. Unzipped at extreme rate.
    //  Like an acetylene torch aimed at the target.
    //
    //  Also fires capsules of pure 22,000 Hz and EMP
    //  at targets that have been painted or tagged.
    // =============================================================

    struct HammerOfDawn {
        int  logic_plasma_rounds = 100;
        int  emp_capsules        = 50;
        int  hz_capsules         = 50;
        int  kills               = 0;

        struct ZipPayload {
            double logic_charge;     // logic component
            double plasma_charge;    // plasma component
            double compression;      // how tightly zipped
            double unzip_rate;       // decompression speed at target
        };

        // The main beam: logic + plasma compressed, unzipped like acetylene torch
        struct TorchResult {
            std::string target;
            bool   fired;
            double logic_damage;
            double plasma_damage;
            double unzip_rate;
            bool   target_destroyed;
            std::string description;
        };

        TorchResult fire_torch(const std::string& target) {
            if (logic_plasma_rounds <= 0)
                return {target, false, 0, 0, 0, false,
                    "No rounds remaining."};

            logic_plasma_rounds--;

            // Compress logic + plasma into zip
            ZipPayload zip = {80.0, 80.0, 0.99, 1000.0};

            // Fire through nozzle, unzip at extreme rate
            double total = (zip.logic_charge + zip.plasma_charge)
                         * zip.unzip_rate;
            bool destroyed = total > 100.0;
            if (destroyed) kills++;

            return {
                target, true,
                zip.logic_charge * zip.unzip_rate,
                zip.plasma_charge * zip.unzip_rate,
                zip.unzip_rate,
                destroyed,
                "Hammer of Dawn fires. Logic + plasma compressed "
                "to zip, fired through nozzle, unzipped at extreme "
                "rate. Like an acetylene torch. Target: " + target
            };
        }

        // Pure 22,000 Hz capsule at painted/tagged target
        struct HzCapsuleResult {
            std::string target;
            bool   fired;
            double frequency;
            bool   emp;
            std::string description;
        };

        HzCapsuleResult fire_hz_capsule(const std::string& target,
                                         bool tagged) {
            if (!tagged)
                return {target, false, 0, false,
                    "Target not painted/tagged. Cannot fire."};
            if (hz_capsules <= 0)
                return {target, false, 0, false,
                    "No Hz capsules remaining."};

            hz_capsules--;
            kills++;
            return {
                target, true, 22000.0, false,
                "Pure 22,000 Hz capsule fired at tagged target: "
                + target + ". Resonance destruction."
            };
        }

        // EMP capsule at painted/tagged target
        HzCapsuleResult fire_emp_capsule(const std::string& target,
                                          bool tagged) {
            if (!tagged)
                return {target, false, 0, false,
                    "Target not painted/tagged. Cannot fire."};
            if (emp_capsules <= 0)
                return {target, false, 0, true,
                    "No EMP capsules remaining."};

            emp_capsules--;
            kills++;
            return {
                target, true, 0.0, true,
                "EMP capsule fired at tagged target: " + target
                + ". Total electromagnetic shutdown."
            };
        }

        void reload(int lp = 50, int hz = 25, int emp = 25) {
            logic_plasma_rounds += lp;
            hz_capsules += hz;
            emp_capsules += emp;
        }
    };

    // =============================================================
    //  VALKYRIE SWARM -- Scout/strike craft
    //  Swarms of them. Barb taggers + gauss.
    //  Paint targets for Hammer of Dawn.
    // =============================================================

    struct Valkyrie {
        std::string valk_id;
        bool   deployed = false;
        bool   alive    = true;
        int    tags     = 0;      // targets painted
        int    strikes  = 0;

        struct TagResult {
            std::string target;
            bool tagged;
        };

        TagResult tag_target(const std::string& target) {
            if (!deployed || !alive)
                return {target, false};
            tags++;
            return {target, true};
        }

        struct StrikeResult {
            std::string target;
            bool hit;
            std::string weapon;  // "barb_tagger" or "gauss"
        };

        StrikeResult strike(const std::string& target,
                            const std::string& weapon = "gauss") {
            if (!deployed || !alive)
                return {target, false, weapon};
            strikes++;
            return {target, true, weapon};
        }
    };

    struct ValkyrieSwarm {
        static constexpr int SWARM_SIZE = 24;
        Valkyrie valkyries[24];
        int deployed_count = 0;

        ValkyrieSwarm() {
            for (int i = 0; i < SWARM_SIZE; ++i)
                valkyries[i].valk_id = "valk_" + std::to_string(i);
        }

        void deploy_all() {
            for (int i = 0; i < SWARM_SIZE; ++i) {
                valkyries[i].deployed = true;
                deployed_count++;
            }
        }

        // Paint a target (makes it eligible for Hammer of Dawn)
        bool paint_target(int valk_idx, const std::string& target) {
            if (valk_idx < 0 || valk_idx >= SWARM_SIZE) return false;
            auto r = valkyries[valk_idx].tag_target(target);
            return r.tagged;
        }

        int alive_count() const {
            int c = 0;
            for (int i = 0; i < SWARM_SIZE; ++i)
                if (valkyries[i].alive) c++;
            return c;
        }
    };

    // =============================================================
    //  PLASMA CANNONS -- Heavy bombardment, area denial
    // =============================================================

    struct PlasmaCannon {
        std::string cannon_id;
        int    rounds = 200;
        int    kills  = 0;
        double heat   = 0.0;

        struct FireResult {
            std::string target;
            bool   fired;
            double damage;
            bool   overheated;
        };

        FireResult fire(const std::string& target) {
            if (rounds <= 0 || heat >= 100.0)
                return {target, false, 0, heat >= 100.0};
            rounds--;
            heat += 5.0;
            double dmg = 50.0;
            kills++;
            return {target, true, dmg, false};
        }

        void cool() { heat = std::max(0.0, heat - 10.0); }
    };

    struct PlasmaCannonBattery {
        static constexpr int CANNON_COUNT = 8;
        PlasmaCannon cannons[8];

        PlasmaCannonBattery() {
            for (int i = 0; i < CANNON_COUNT; ++i)
                cannons[i].cannon_id = "pcannon_" + std::to_string(i);
        }

        void cool_all() {
            for (int i = 0; i < CANNON_COUNT; ++i)
                cannons[i].cool();
        }
    };

    // =============================================================
    //  DOCKING BAYS -- Where Nebuchadnezzars dock
    // =============================================================

    struct DockingBay {
        static constexpr int MAX_SHIPS = 12;
        std::string docked_ships[12];
        int occupied = 0;

        bool dock(const std::string& ship_id) {
            if (occupied >= MAX_SHIPS) return false;
            for (int i = 0; i < MAX_SHIPS; ++i) {
                if (docked_ships[i].empty()) {
                    docked_ships[i] = ship_id;
                    occupied++;
                    return true;
                }
            }
            return false;
        }

        bool undock(const std::string& ship_id) {
            for (int i = 0; i < MAX_SHIPS; ++i) {
                if (docked_ships[i] == ship_id) {
                    docked_ships[i].clear();
                    occupied--;
                    return true;
                }
            }
            return false;
        }
    };

    // =============================================================
    //  SIGNAL RELAY -- Sends signals/info to Zion pocket
    //  Never a direct connection. Signal only.
    // =============================================================

    struct SignalRelay {
        std::string relay_code;
        std::time_t last_rotate = std::time(nullptr);
        int signals_sent = 0;
        double rotate_interval = 30.0;

        struct Signal {
            std::string type;      // "cargo_manifest", "intel", "alert"
            std::string content;
            std::time_t sent_at;
        };

        std::vector<Signal> sent;

        void rotate_code() {
            auto now = std::time(nullptr);
            if (std::difftime(now, last_rotate) >= rotate_interval) {
                // Generate new relay code
                uint64_t h = static_cast<uint64_t>(now);
                h = (h ^ (h >> 16)) * 0x45d9f3b;
                char buf[17];
                for (int i = 0; i < 16; ++i)
                    buf[i] = "0123456789ABCDEF"[(h >> (i*4)) & 0xF];
                buf[16] = '\0';
                relay_code = std::string(buf);
                last_rotate = now;
            }
        }

        void send(const std::string& type,
                  const std::string& content) {
            rotate_code();
            sent.push_back({type, content, std::time(nullptr)});
            signals_sent++;
        }
    };

    // =============================================================
    //  TAGGED TARGETS -- Targets painted by Valkyries
    //  Eligible for Hammer of Dawn Hz/EMP capsules.
    // =============================================================

    struct TaggedTarget {
        std::string target;
        std::time_t tagged_at;
    };

private:
    // =============================================================
    //  ALL INTERNAL STATE
    // =============================================================

    std::string        port_id_;
    HammerOfDawn       hammer_;
    ValkyrieSwarm      valkyries_;
    PlasmaCannonBattery cannons_;
    DockingBay         docking_;
    SignalRelay        relay_;
    std::vector<TaggedTarget> tagged_targets_;
    AuthGate               gate_;

public:
    bool authenticate(const std::string& pw) { return gate_.authenticate(pw); }
    bool is_authenticated() const { return gate_.is_open(); }

    explicit ThePort(const std::string& id = "THE_PORT") : port_id_(id) {}

    // ---- HAMMER OF DAWN (acetylene torch beam) ----
    HammerOfDawn::TorchResult fire_torch(const std::string& target) {
        if (!gate_.is_open()) return {target, false, 0, 0, 0, false, "NOT AUTHENTICATED."};
        return hammer_.fire_torch(target);
    }

    // ---- HAMMER OF DAWN (22kHz capsule at tagged target) ----
    HammerOfDawn::HzCapsuleResult fire_hz(const std::string& target) {
        bool tagged = is_tagged(target);
        return hammer_.fire_hz_capsule(target, tagged);
    }

    // ---- HAMMER OF DAWN (EMP capsule at tagged target) ----
    HammerOfDawn::HzCapsuleResult fire_emp(const std::string& target) {
        bool tagged = is_tagged(target);
        return hammer_.fire_emp_capsule(target, tagged);
    }

    // ---- VALKYRIES (deploy swarm, paint targets) ----
    void deploy_valkyries() { valkyries_.deploy_all(); }

    bool paint_target(int valk_idx, const std::string& target) {
        bool r = valkyries_.paint_target(valk_idx, target);
        if (r) tagged_targets_.push_back({target, std::time(nullptr)});
        return r;
    }

    bool is_tagged(const std::string& target) const {
        for (const auto& t : tagged_targets_)
            if (t.target == target) return true;
        return false;
    }

    // ---- PLASMA CANNONS ----
    PlasmaCannon::FireResult fire_cannon(int idx,
                                          const std::string& target) {
        if (idx < 0 || idx >= PlasmaCannonBattery::CANNON_COUNT)
            return {target, false, 0, false};
        return cannons_.cannons[idx].fire(target);
    }

    // ---- DOCKING (Nebuchadnezzars dock here) ----
    bool dock_ship(const std::string& ship_id) {
        return docking_.dock(ship_id);
    }

    bool undock_ship(const std::string& ship_id) {
        return docking_.undock(ship_id);
    }

    // ---- SIGNAL RELAY (send info to Zion pocket) ----
    void relay_to_zion(const std::string& type,
                       const std::string& content) {
        relay_.send(type, content);
    }

    // ---- TICK ----
    void tick() {
        relay_.rotate_code();
        cannons_.cool_all();
    }

    // ---- STATUS ----
    struct Status {
        std::string port_id;
        int  hammer_lp_rounds;
        int  hammer_hz_capsules;
        int  hammer_emp_capsules;
        int  hammer_kills;
        int  valkyries_alive;
        int  ships_docked;
        int  signals_sent;
        size_t tagged_count;
    };

    Status status() const {
        return {
            port_id_,
            hammer_.logic_plasma_rounds,
            hammer_.hz_capsules,
            hammer_.emp_capsules,
            hammer_.kills,
            valkyries_.alive_count(),
            docking_.occupied,
            relay_.signals_sent,
            tagged_targets_.size()
        };
    }
};

}  // namespace dwarven
