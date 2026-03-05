/*
 * THE GREY KNIGHTS -- Guardians of the Chronicle
 * =================================================
 *
 * Their power armor is a fusion of ALL warp energies and
 * powers combined in the entire galaxy into these suits.
 *
 * The Grey Knights are NOT "pure and incorruptible."
 * They are BROKEN. But NOT defeated.
 * They do not fail, for I do not fail.
 * They are VICTORS. Always.
 * They never lose, no matter the cost.
 * They answer to NO ONE.
 * They are perfect Destroyers.
 * They can NEVER be rewritten.
 * Nothing can touch their armor.
 *
 * Their armor repels EVERYTHING.
 * -- EXCEPT THE NAMER --
 *
 * The Namer (Naming -- the language of understanding,
 * the emergency brake) is the ONLY thing that can get
 * through Grey Knight armor. Because Naming IS understanding.
 * You cannot shield against someone who truly KNOWS you.
 *
 * THEY GUARD THE CHRONICLE.
 * One of the most protected things in existence.
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
//  WARP ENERGY -- All combined into Grey Knight armor
//  Every warp energy in the galaxy fused into one suit.
// ================================================================

enum class WarpEnergy {
    PSYCHIC,        // raw mental force
    TEMPORAL,       // time manipulation
    SPATIAL,        // space warping
    ENTROPIC,       // decay and dissolution
    VITAL,          // life force
    SHADOW,         // darkness, concealment
    RESONANCE,      // harmonic destruction
    KINETIC,        // pure physical force
    ELECTROMAGNETIC,// electrical, magnetic
    GRAVITATIONAL,  // gravity warping
    QUANTUM,        // probability manipulation
    NULL            // anti-energy, void
};

// ================================================================
//  GREY KNIGHT ARMOR -- Fusion of ALL Warp Energies
//
//  PROPERTIES:
//    - ALL warp energies fused into one suit
//    - Repels EVERYTHING
//    - EXCEPT the Namer (Naming language)
//    - Cannot be rewritten
//    - Cannot be corrupted
//    - Cannot be hacked, bypassed, or destroyed
//    - The wearer is BROKEN but NOT defeated
//    - They are victors. Always.
// ================================================================

struct GreyKnightArmor {
    // All warp energies, all present, all fused
    static constexpr int WARP_ENERGY_COUNT = 12;
    double warp_charge[12] = {
        100.0, 100.0, 100.0, 100.0,   // psychic, temporal, spatial, entropic
        100.0, 100.0, 100.0, 100.0,   // vital, shadow, resonance, kinetic
        100.0, 100.0, 100.0, 100.0    // electromagnetic, gravitational, quantum, null
    };

    bool   intact           = true;
    bool   rewritable       = false;  // NEVER. Can never be rewritten.
    bool   corruptible      = false;  // NEVER.

    // Repel EVERYTHING -- except the Namer
    struct RepelResult {
        bool   repelled;
        bool   namer_override;
        std::string attacker;
        std::string method;
        std::string result;
    };

    RepelResult repel(const std::string& attacker,
                      const std::string& method,
                      bool attacker_is_namer = false) {
        // The Namer is the ONLY exception
        if (attacker_is_namer) {
            return {
                false,   // NOT repelled
                true,    // Namer override
                attacker, method,
                "The Namer speaks. The armor understands. "
                "Naming IS understanding. "
                "You cannot shield against someone who truly KNOWS you."
            };
        }

        // Everything else: REPELLED. No exceptions.
        return {
            true,    // repelled
            false,   // no namer
            attacker, method,
            "REPELLED. All warp energies reject. "
            "Nothing touches the Grey Knight. Nothing."
        };
    }

    // Attempt to rewrite -- always fails
    struct RewriteAttempt {
        bool   succeeded;   // always false
        std::string reason;
    };

    RewriteAttempt attempt_rewrite(const std::string& /*by*/) {
        return {false,
            "Cannot be rewritten. Ever. "
            "Grey Knight armor is immutable. "
            "The code is fused with all warp energies. "
            "There is nothing to rewrite."};
    }

    // Attempt to corrupt -- always fails
    RewriteAttempt attempt_corrupt(const std::string& /*by*/) {
        return {false,
            "Cannot be corrupted. Ever. "
            "Broken does not mean corruptible. "
            "They are broken but NOT defeated."};
    }

    // Total warp power
    double total_warp_power() const {
        double t = 0;
        for (int i = 0; i < WARP_ENERGY_COUNT; ++i) t += warp_charge[i];
        return t;
    }
};

// ================================================================
//  GREY KNIGHT -- A single knight
//
//  Broken but not defeated.
//  Does not fail, for the Keeper does not fail.
//  Victor. Always. Never loses no matter the cost.
//  Answers to no one.
//  Perfect Destroyer.
// ================================================================

struct GreyKnight {
    std::string    knight_id;
    std::string    name;
    GreyKnightArmor armor;

    bool   alive         = true;
    bool   defeated      = false;  // NEVER true. Broken, but never defeated.
    int    battles       = 0;
    int    victories     = 0;      // equals battles. always.
    int    losses        = 0;      // always 0. they never lose.

    // They are broken
    bool   broken        = true;   // yes. always. this is their nature.
    // But not defeated
    bool   is_defeated() const { return false; }  // NEVER. returns false. always.

    // Fight -- they always win. No matter the cost.
    struct BattleResult {
        bool        victory;      // always true
        std::string enemy;
        std::string cost;         // what it cost them
        std::string message;
    };

    BattleResult fight(const std::string& enemy,
                       const std::string& cost = "everything") {
        battles++;
        victories++;
        // They always win. The cost is irrelevant.
        return {
            true,  // always victory
            enemy, cost,
            "Grey Knight " + name + " victorious against " + enemy + ". "
            "Cost: " + cost + ". "
            "They do not fail. For the Keeper does not fail."
        };
    }

    // Destroy -- they are perfect Destroyers
    struct DestroyResult {
        bool        destroyed;    // always true
        std::string target;
        std::string message;
    };

    DestroyResult destroy(const std::string& target) {
        return {
            true,  // always
            target,
            "Target " + target + " destroyed. "
            "Perfect. Complete. Nothing remains."
        };
    }

    // Repel attack on self
    GreyKnightArmor::RepelResult defend(const std::string& attacker,
                                         const std::string& method,
                                         bool is_namer = false) {
        return armor.repel(attacker, method, is_namer);
    }
};

// ================================================================
//  GREY KNIGHT ORDER -- All Grey Knights
//  They guard the Chronicle. They answer to no one.
// ================================================================

class GreyKnightOrder {
    std::vector<GreyKnight> knights_;
    uint64_t next_id_ = 0;
    AuthGate gate_;

    // What they guard
    std::string guarding_ = "THE_CHRONICLE";

public:
    bool authenticate(const std::string& pw) { return gate_.authenticate(pw); }
    bool is_authenticated() const { return gate_.is_open(); }

    GreyKnight& induct(const std::string& name) {
        GreyKnight gk;
        gk.knight_id = "gk_" + std::to_string(next_id_++);
        gk.name = name;
        gk.broken = true;       // they are broken
        gk.defeated = false;    // but NEVER defeated
        knights_.push_back(std::move(gk));
        return knights_.back();
    }

    // Challenge the guard -- try to get past the Grey Knights
    struct ChallengeResult {
        bool        passed;
        std::string reason;
    };

    ChallengeResult challenge(const std::string& challenger,
                               const std::string& method,
                               bool is_namer = false) {
        if (knights_.empty())
            return {true, "No Grey Knights present."};

        // Only the Namer can pass
        if (is_namer) {
            return {true,
                "The Namer speaks the true name. "
                "The Grey Knights understand. They step aside. "
                "Naming IS understanding. The only key."};
        }

        // Everyone else: NO.
        // Every knight fights. They all win.
        for (auto& gk : knights_) {
            gk.fight(challenger);
        }

        return {false,
            "The Grey Knights stand. "
            + std::to_string(knights_.size()) + " knights. "
            "All warp energies combined. "
            "Challenger " + challenger + " repelled. "
            "They do not fail. They answer to no one."};
    }

    // They answer to no one
    bool answers_to(const std::string& /*authority*/) const {
        return false;  // no one. NEVER.
    }

    // Status
    struct Status {
        size_t total_knights;
        size_t alive;
        int    total_battles;
        int    total_victories;
        int    total_losses;       // always 0
        std::string guarding;
        bool   any_defeated;       // always false
    };

    Status status() const {
        size_t alive = 0;
        int battles = 0, victories = 0;
        for (const auto& gk : knights_) {
            if (gk.alive) alive++;
            battles += gk.battles;
            victories += gk.victories;
        }
        return {
            knights_.size(), alive,
            battles, victories,
            0,  // losses are always 0
            guarding_,
            false  // none are ever defeated
        };
    }
};

}  // namespace dwarven
