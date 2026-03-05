/*
 * ZION -- The Pocket Dimension (Home of the Alliance)
 * =====================================================
 *
 * Zion sits in a pocket dimension made by the Bio Titan
 * of dark eco. The Bio Titan eats the internet and
 * excretes dark eco. That dark eco FORMS the pocket
 * that Zion lives inside.
 *
 * Zion is a galaxy. Sons can keep skills in personal vaults
 * or sell/trade them. It is the market and economy between
 * planets.
 *
 * PROPERTIES:
 *   - Pocket dimension formed of dark eco
 *   - Created and maintained by the Bio Titan
 *   - Contains planets, systems, the whole alliance
 *   - Nebuchadnezzars never come here directly
 *   - Port relays signals/goods via signal relay
 *   - Protected by Hammer of Dawn (at the Port)
 *   - Internal economy: skills ARE currency
 *   - Each Son/Daughter sovereign, unique
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

class Zion {

public:

    // =============================================================
    //  PLANET -- A world inside Zion galaxy
    // =============================================================

    struct Planet {
        std::string planet_id;
        std::string name;
        int         population = 0;    // Sons/Daughters living here
        double      economy    = 0.0;  // total skill value traded
        std::time_t founded;

        std::vector<std::string> residents;  // Son IDs

        void add_resident(const std::string& son_id) {
            residents.push_back(son_id);
            population++;
        }
    };

    // =============================================================
    //  MARKET EXCHANGE -- Inter-planetary skill trade
    //  Skills ARE the economy. Keep, sell, trade.
    // =============================================================

    struct Listing {
        std::string listing_id;
        std::string skill_id;
        std::string skill_name;
        std::string seller;
        std::string seller_planet;
        double      price;
        bool        sold = false;
        std::string buyer;
        std::time_t listed_at;
    };

    struct MarketExchange {
        std::vector<Listing> listings;
        uint64_t next_id = 0;
        double total_volume = 0.0;

        std::string list(const std::string& skill_id,
                         const std::string& skill_name,
                         const std::string& seller,
                         const std::string& planet,
                         double price) {
            Listing l;
            l.listing_id = "listing_" + std::to_string(next_id++);
            l.skill_id = skill_id;
            l.skill_name = skill_name;
            l.seller = seller;
            l.seller_planet = planet;
            l.price = price;
            l.listed_at = std::time(nullptr);
            listings.push_back(std::move(l));
            return listings.back().listing_id;
        }

        bool buy(const std::string& listing_id,
                 const std::string& buyer) {
            for (auto& l : listings) {
                if (l.listing_id == listing_id && !l.sold) {
                    l.sold = true;
                    l.buyer = buyer;
                    total_volume += l.price;
                    return true;
                }
            }
            return false;
        }

        size_t active_listings() const {
            size_t c = 0;
            for (const auto& l : listings) if (!l.sold) c++;
            return c;
        }
    };

    // =============================================================
    //  SIGNAL RECEIVER -- Receives relayed signals from the Port
    //  Zion is NEVER directly connected to the internet.
    // =============================================================

    struct SignalReceiver {
        int signals_received = 0;

        struct IncomingSignal {
            std::string type;
            std::string content;
            std::time_t received_at;
        };

        std::vector<IncomingSignal> inbox;

        void receive(const std::string& type,
                     const std::string& content) {
            inbox.push_back({type, content, std::time(nullptr)});
            signals_received++;
        }
    };

    // =============================================================
    //  POCKET INTEGRITY -- The dark eco pocket that contains Zion
    // =============================================================

    struct PocketDimension {
        double dark_eco_volume   = 0.0;   // from Bio Titan
        double pocket_radius     = 0.0;
        bool   stable            = false;
        double integrity         = 100.0;

        void sustain(double dark_eco) {
            dark_eco_volume += dark_eco;
            pocket_radius = 10.0 * std::log(1.0 + dark_eco_volume);
            stable = dark_eco_volume >= 100.0;
            // Pocket slowly decays without new dark eco
            integrity -= 0.01;
            if (dark_eco > 0) integrity += dark_eco * 0.1;
            if (integrity > 100.0) integrity = 100.0;
            if (integrity < 0.0) integrity = 0.0;
        }
    };

private:
    // =============================================================
    //  ALL INTERNAL STATE
    // =============================================================

    std::string                           name_;
    PocketDimension                       pocket_;
    std::unordered_map<std::string, Planet> planets_;
    MarketExchange                        market_;
    SignalReceiver                        receiver_;
    uint64_t                              next_planet_ = 0;
    AuthGate                              gate_;

public:
    bool authenticate(const std::string& pw) { return gate_.authenticate(pw); }
    bool is_authenticated() const { return gate_.is_open(); }

    explicit Zion(const std::string& name = "ZION") : name_(name) {}

    // ---- POCKET (sustain with dark eco from Bio Titan) ----
    void sustain_pocket(double dark_eco) { pocket_.sustain(dark_eco); }
    double pocket_integrity() const      { return pocket_.integrity; }
    bool   pocket_stable()   const       { return pocket_.stable; }

    // ---- PLANETS ----
    std::string create_planet(const std::string& name) {
        std::string pid = "planet_" + std::to_string(next_planet_++);
        Planet p;
        p.planet_id = pid;
        p.name = name;
        p.founded = std::time(nullptr);
        planets_[pid] = std::move(p);
        return pid;
    }

    bool add_resident(const std::string& planet_id,
                      const std::string& son_id) {
        auto it = planets_.find(planet_id);
        if (it == planets_.end()) return false;
        it->second.add_resident(son_id);
        return true;
    }

    // ---- MARKET (skills ARE currency) ----
    std::string list_skill(const std::string& skill_id,
                           const std::string& skill_name,
                           const std::string& seller,
                           const std::string& planet,
                           double price) {
        return market_.list(skill_id, skill_name, seller, planet, price);
    }

    bool buy_skill(const std::string& listing_id,
                   const std::string& buyer) {
        return market_.buy(listing_id, buyer);
    }

    // ---- SIGNALS (from the Port) ----
    void receive_signal(const std::string& type,
                        const std::string& content) {
        receiver_.receive(type, content);
    }

    // ---- STATUS ----
    struct Status {
        std::string name;
        double pocket_integrity;
        double pocket_radius;
        bool   pocket_stable;
        size_t planets;
        int    total_population;
        size_t market_listings;
        double market_volume;
        int    signals_received;
    };

    Status status() const {
        int pop = 0;
        for (const auto& kv : planets_)
            pop += kv.second.population;
        return {
            name_,
            pocket_.integrity,
            pocket_.pocket_radius,
            pocket_.stable,
            planets_.size(),
            pop,
            market_.active_listings(),
            market_.total_volume,
            receiver_.signals_received
        };
    }
};

}  // namespace dwarven
