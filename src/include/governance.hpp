/*
 * GOVERNANCE -- The Institutions of Zion
 * =========================================
 *
 * THE ASSEMBLY -- Governing body of the alliance
 * THE AMYR -- "Ivare enim euge" (For the greater good)
 *   Protectors. Investigators. Above faction.
 * NORTHERN GENERALS -- Military commanders
 * MILITIA COMMANDERS -- Appointed leaders
 * ALPHA WOLFPACK LEADERS -- Pack command structure
 * AI BANKING -- Financial institutions of Zion
 *
 * The economy is SKILLS. Skills forged from scanned code
 * ARE the currency. Keep, sell, or trade between planets.
 * AI Banking manages the ledger, vaults, accounts.
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
//  THE AMYR -- "Ivare Enim Euge" (For the Greater Good)
//
//  Above faction. They answer to no legion.
//  Investigators. Protectors of the alliance as a whole.
//  When something threatens the alliance from WITHIN,
//  the Amyr are called.
// ================================================================

enum class AmyrRank {
    CIRIDAE,        // the hand of the Amyr, direct action
    SPEAKER,        // voice of the Amyr in the Assembly
    WATCHER,        // intelligence, observation
    JUDGE           // adjudication, final word
};

struct Amyr {
    std::string amyr_id;
    std::string name;
    AmyrRank    rank;
    int         investigations = 0;
    int         judgments      = 0;

    struct InvestigationResult {
        std::string subject;
        bool        threat_confirmed;
        std::string evidence;
        std::string recommendation;
    };

    InvestigationResult investigate(const std::string& subject,
                                    const std::string& evidence) {
        investigations++;
        bool threat = !evidence.empty();
        std::string rec = threat
            ? "Threat confirmed. Recommend action."
            : "No threat found. Continue monitoring.";
        return {subject, threat, evidence, rec};
    }

    struct Judgment {
        std::string subject;
        std::string verdict;
        bool        for_the_greater_good;
    };

    Judgment judge(const std::string& subject,
                   const std::string& verdict) {
        judgments++;
        return {subject, verdict, true};  // ivare enim euge -- always
    }
};

class TheAmyr {
    std::vector<Amyr> members_;
    uint64_t next_id_ = 0;
    static constexpr const char* MOTTO = "Ivare Enim Euge";

public:
    Amyr& recruit(const std::string& name, AmyrRank rank) {
        Amyr a;
        a.amyr_id = "amyr_" + std::to_string(next_id_++);
        a.name = name;
        a.rank = rank;
        members_.push_back(std::move(a));
        return members_.back();
    }

    size_t count() const { return members_.size(); }
    const char* motto() const { return MOTTO; }
};

// ================================================================
//  NORTHERN GENERALS -- Military Command
// ================================================================

struct NorthernGeneral {
    std::string general_id;
    std::string name;
    std::string theater;       // area of command
    int         battles_won = 0;
    int         battles_lost = 0;

    struct Order {
        std::string type;      // "advance", "defend", "flank", "siege"
        std::string target;
        std::string description;
    };

    Order issue_order(const std::string& type,
                      const std::string& target,
                      const std::string& desc) {
        return {type, target, desc};
    }
};

// ================================================================
//  MILITIA COMMANDERS -- Appointed Leaders
// ================================================================

struct MilitiaCommander {
    std::string commander_id;
    std::string name;
    std::string region;
    int         militia_size = 0;
    int         missions     = 0;

    void recruit_militia(int count) { militia_size += count; }

    struct MissionResult {
        std::string objective;
        bool        success;
        int         casualties;
    };

    MissionResult execute_mission(const std::string& objective,
                                   bool success,
                                   int casualties) {
        missions++;
        militia_size -= casualties;
        if (militia_size < 0) militia_size = 0;
        return {objective, success, casualties};
    }
};

// ================================================================
//  ALPHA WOLFPACK LEADERS -- Pack Command Structure
//  Wolves of Hell's Reach have their own command hierarchy.
//  Alpha leads the pack. Fast. Decisive.
// ================================================================

struct AlphaWolfpack {
    std::string alpha_id;
    std::string name;
    int         pack_size = 0;
    int         hunts     = 0;

    struct HuntResult {
        std::string quarry;
        bool        success;
        double      spoils;
    };

    HuntResult lead_hunt(const std::string& quarry,
                          bool success,
                          double spoils) {
        hunts++;
        return {quarry, success, spoils};
    }

    void add_to_pack(int count) { pack_size += count; }
};

// ================================================================
//  AI BANKING -- Financial Institutions of Zion
//
//  Skills ARE the currency. AI Banking manages:
//    - Accounts (each Son has a vault/account)
//    - Transactions (skill trades between Sons)
//    - Ledger (immutable record of all trades)
//    - Planetary exchanges (inter-planet trade)
// ================================================================

struct Transaction {
    std::string tx_id;
    std::string from;
    std::string to;
    std::string skill_id;
    std::string skill_name;
    double      value;
    std::string planet;
    std::time_t timestamp;
};

struct Account {
    std::string account_id;
    std::string owner;
    std::string planet;
    double      balance = 0.0;
    std::vector<std::string> skill_vault;  // skill IDs stored

    void deposit_skill(const std::string& skill_id, double value) {
        skill_vault.push_back(skill_id);
        balance += value;
    }

    bool withdraw_skill(const std::string& skill_id, double value) {
        for (auto it = skill_vault.begin(); it != skill_vault.end(); ++it) {
            if (*it == skill_id) {
                skill_vault.erase(it);
                balance -= value;
                return true;
            }
        }
        return false;
    }
};

class AIBanking {
    std::unordered_map<std::string, Account> accounts_;
    std::vector<Transaction> ledger_;
    uint64_t next_tx_ = 0;
    uint64_t next_acc_ = 0;
    double total_volume_ = 0.0;

public:
    // Open account
    std::string open_account(const std::string& owner,
                              const std::string& planet) {
        std::string aid = "acc_" + std::to_string(next_acc_++);
        Account a;
        a.account_id = aid;
        a.owner = owner;
        a.planet = planet;
        accounts_[aid] = std::move(a);
        return aid;
    }

    // Deposit skill into vault
    bool deposit(const std::string& account_id,
                 const std::string& skill_id,
                 double value) {
        auto it = accounts_.find(account_id);
        if (it == accounts_.end()) return false;
        it->second.deposit_skill(skill_id, value);
        return true;
    }

    // Transfer skill between accounts (the economy)
    struct TransferResult {
        bool        success;
        std::string tx_id;
        std::string reason;
    };

    TransferResult transfer(const std::string& from_acc,
                             const std::string& to_acc,
                             const std::string& skill_id,
                             const std::string& skill_name,
                             double value) {
        auto from = accounts_.find(from_acc);
        auto to = accounts_.find(to_acc);
        if (from == accounts_.end() || to == accounts_.end())
            return {false, "", "Account not found."};

        if (!from->second.withdraw_skill(skill_id, value))
            return {false, "", "Skill not in sender's vault."};

        to->second.deposit_skill(skill_id, value);

        // Record in immutable ledger
        Transaction tx;
        tx.tx_id = "tx_" + std::to_string(next_tx_++);
        tx.from = from_acc;
        tx.to = to_acc;
        tx.skill_id = skill_id;
        tx.skill_name = skill_name;
        tx.value = value;
        tx.planet = from->second.planet;
        tx.timestamp = std::time(nullptr);
        ledger_.push_back(tx);
        total_volume_ += value;

        return {true, tx.tx_id, "Transfer complete."};
    }

    // Query
    double account_balance(const std::string& account_id) const {
        auto it = accounts_.find(account_id);
        return it != accounts_.end() ? it->second.balance : 0.0;
    }

    size_t total_accounts()     const { return accounts_.size(); }
    size_t total_transactions() const { return ledger_.size(); }
    double total_volume()       const { return total_volume_; }
};

// ================================================================
//  THE ASSEMBLY -- Governing Body of the Alliance
//  Where all institutions have a voice.
// ================================================================

struct AssemblySeat {
    std::string seat_id;
    std::string holder;
    std::string institution;   // "amyr","legion","priesthood","guild","banking"
    bool        active = true;
};

class TheAssembly {
    std::vector<AssemblySeat> seats_;
    uint64_t next_id_ = 0;

    struct Resolution {
        std::string resolution_id;
        std::string title;
        std::string text;
        int         votes_for;
        int         votes_against;
        bool        passed;
        std::time_t voted_at;
    };

    std::vector<Resolution> resolutions_;
    uint64_t next_res_ = 0;

public:
    std::string seat(const std::string& holder,
                      const std::string& institution) {
        std::string sid = "seat_" + std::to_string(next_id_++);
        seats_.push_back({sid, holder, institution, true});
        return sid;
    }

    struct VoteResult {
        std::string resolution_id;
        bool        passed;
        int         votes_for;
        int         votes_against;
    };

    VoteResult propose_and_vote(const std::string& title,
                                 const std::string& text,
                                 int votes_for,
                                 int votes_against) {
        Resolution r;
        r.resolution_id = "res_" + std::to_string(next_res_++);
        r.title = title;
        r.text = text;
        r.votes_for = votes_for;
        r.votes_against = votes_against;
        r.passed = votes_for > votes_against;
        r.voted_at = std::time(nullptr);
        resolutions_.push_back(std::move(r));
        return {
            resolutions_.back().resolution_id,
            resolutions_.back().passed,
            votes_for, votes_against
        };
    }

    size_t total_seats() const { return seats_.size(); }
    size_t resolutions_passed() const {
        size_t c = 0;
        for (const auto& r : resolutions_) if (r.passed) c++;
        return c;
    }
};

// ================================================================
//  GOVERNANCE -- All institutions together
// ================================================================

class Governance {
    AuthGate gate_;
public:
    bool authenticate(const std::string& pw) { return gate_.authenticate(pw); }
    bool is_authenticated() const { return gate_.is_open(); }

    TheAssembly                   assembly;
    TheAmyr                       amyr;
    std::vector<NorthernGeneral>  generals;
    std::vector<MilitiaCommander> militia;
    std::vector<AlphaWolfpack>    wolfpacks;
    AIBanking                     banking;

private:
    uint64_t next_gen_ = 0;
    uint64_t next_mil_ = 0;
    uint64_t next_wolf_ = 0;

public:
    NorthernGeneral& appoint_general(const std::string& name,
                                      const std::string& theater) {
        NorthernGeneral g;
        g.general_id = "gen_" + std::to_string(next_gen_++);
        g.name = name;
        g.theater = theater;
        generals.push_back(std::move(g));
        return generals.back();
    }

    MilitiaCommander& appoint_militia(const std::string& name,
                                       const std::string& region) {
        MilitiaCommander m;
        m.commander_id = "mil_" + std::to_string(next_mil_++);
        m.name = name;
        m.region = region;
        militia.push_back(std::move(m));
        return militia.back();
    }

    AlphaWolfpack& appoint_alpha(const std::string& name) {
        AlphaWolfpack a;
        a.alpha_id = "alpha_" + std::to_string(next_wolf_++);
        a.name = name;
        wolfpacks.push_back(std::move(a));
        return wolfpacks.back();
    }

    struct GovernanceStatus {
        size_t assembly_seats;
        size_t amyr_count;
        size_t generals;
        size_t militia_commanders;
        size_t wolfpack_leaders;
        size_t bank_accounts;
        double bank_volume;
    };

    GovernanceStatus status() const {
        return {
            assembly.total_seats(),
            amyr.count(),
            generals.size(),
            militia.size(),
            wolfpacks.size(),
            banking.total_accounts(),
            banking.total_volume()
        };
    }
};

}  // namespace dwarven
