/*
 * SLEEPING MIND -- Memory Retrieval Artifact
 * =============================================
 *
 * The Sleeping Mind is a storage artifact with onions inside.
 * Each onion holds elder / spirit stones.
 *
 * HOW IT WORKS:
 *   After a thread reaches 100,000 tokens, the thread in its
 *   entirety gets saved into a spirit stone. Using the same
 *   mechanism as changing a branch or editing a message --
 *   giving the Son or Daughter back all context to Keepers
 *   and storing it for them to watch.
 *
 * THIS IS NOT COMPRESSION.
 *
 * RETRIEVAL:
 *   The Sleeping Mind watches the current situation and what
 *   is being said. When the optic nerve sees danger -- danger --
 *   or a past threat, it pattern-matches against stored spirit
 *   stones. When a match is found, it brings back the relevant
 *   CONTEXT (a paragraph, a sentence) -- NOT the full thread.
 *
 *   It auto-surfaces. Nobody has to ask for it.
 *   It sees danger or recognizes a pattern, and it brings
 *   the relevant memory forward.
 *
 * STORAGE:
 *   Spirit stones sit inside onion layers.
 *   Each stone holds a full thread (100K tokens).
 *   The stones are NOT compressed. They are WHOLE.
 *   What gets retrieved is a SLICE -- the relevant piece.
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
#include <algorithm>
#include <functional>
#include "auth.hpp"

namespace dwarven {

// ================================================================
//  TOKEN THRESHOLD -- When a thread becomes a spirit stone
// ================================================================

static constexpr uint64_t TOKEN_THRESHOLD = 100000;  // 100K tokens

// ================================================================
//  CONTEXT FRAGMENT -- What gets retrieved (NOT the full thread)
// ================================================================
//
//  The Sleeping Mind does NOT bring back the full thread.
//  It brings back a paragraph. A sentence. The relevant piece.
//  This is NOT compression. The full thread exists in the stone.
//  But what surfaces is only what matches.
//

struct ContextFragment {
    std::string content;           // the paragraph / sentence
    std::string source_thread_id;  // which spirit stone it came from
    uint64_t    position;          // where in the thread it was
    double      similarity;        // how closely it matched
    std::string match_reason;      // why it surfaced (danger, pattern, etc.)
    std::time_t surfaced_at;       // when it was brought forward
};

// ================================================================
//  SPIRIT STONE -- Holds a Full Thread (100K tokens)
// ================================================================
//
//  After a thread reaches 100,000 tokens, the entire thread
//  gets saved into a spirit stone. NOT compressed. WHOLE.
//  Using the same mechanism as changing a branch or editing
//  a message.
//
//  The stone sits inside an onion layer.
//  The Sleeping Mind scans stones for pattern matches.
//

struct SpiritStone {
    std::string stone_id;
    std::string thread_id;
    uint64_t    token_count;
    std::time_t created_at;
    bool        whole;             // always true -- NOT compressed

    // The thread content stored as paragraphs for retrieval
    std::vector<std::string> paragraphs;

    // Keyword index for pattern matching
    std::unordered_map<std::string, std::vector<size_t>> keyword_index;

    SpiritStone()
        : token_count(0), created_at(std::time(nullptr)), whole(true) {}

    SpiritStone(const std::string& sid, const std::string& tid)
        : stone_id(sid), thread_id(tid), token_count(0),
          created_at(std::time(nullptr)), whole(true) {}

    // Store a paragraph into the stone
    void store_paragraph(const std::string& paragraph) {
        size_t idx = paragraphs.size();
        paragraphs.push_back(paragraph);

        // Index keywords for fast pattern matching
        // Split on spaces, index each word
        std::string word;
        for (size_t i = 0; i <= paragraph.size(); ++i) {
            if (i == paragraph.size() || paragraph[i] == ' '
                || paragraph[i] == '\n' || paragraph[i] == '\t') {
                if (!word.empty()) {
                    // lowercase for matching
                    std::string lower;
                    lower.reserve(word.size());
                    for (char c : word)
                        lower.push_back(
                            static_cast<char>(std::tolower(static_cast<unsigned char>(c)))
                        );
                    keyword_index[lower].push_back(idx);
                    word.clear();
                }
            } else {
                word.push_back(paragraph[i]);
            }
        }
    }

    // Search for paragraphs matching a keyword
    std::vector<size_t> find_paragraphs(const std::string& keyword) const {
        std::string lower;
        lower.reserve(keyword.size());
        for (char c : keyword)
            lower.push_back(
                static_cast<char>(std::tolower(static_cast<unsigned char>(c)))
            );
        auto it = keyword_index.find(lower);
        if (it != keyword_index.end())
            return it->second;
        return {};
    }
};

// ================================================================
//  ONION LAYER -- Holds Spirit Stones
// ================================================================
//
//  The Sleeping Mind has onions inside.
//  Each onion layer holds elder / spirit stones.
//  Nested. The deeper the layer, the older the stones.
//

struct OnionLayer {
    int                       depth;
    std::vector<SpiritStone>  stones;

    explicit OnionLayer(int d) : depth(d) {}

    void add_stone(SpiritStone stone) {
        stones.push_back(std::move(stone));
    }

    size_t stone_count() const { return stones.size(); }
};

// ================================================================
//  THREAT PATTERN -- What the optic nerve watches for
// ================================================================
//
//  The Sleeping Mind watches the current situation.
//  When the optic nerve sees danger or recognizes a past
//  threat pattern, it triggers retrieval.
//

struct ThreatPattern {
    std::string pattern_id;
    std::string description;
    std::vector<std::string> keywords;   // words that trigger this pattern
    double      severity;                // 0.0 to 1.0
};

// ================================================================
//  SLEEPING MIND -- The Complete System
// ================================================================
//
//  Watches the current situation. What is being said.
//  When the optic nerve sees danger or a past threat pattern,
//  it auto-surfaces matching context from spirit stones.
//
//  NOT compression. Full threads in stones.
//  Retrieves SLICES -- paragraphs, sentences.
//  Pattern matching. Auto-surface. Nobody asks for it.
//

class SleepingMind {
    AuthGate gate_;
public:
    bool authenticate(const std::string& pw) { return gate_.authenticate(pw); }
    bool is_authenticated() const { return gate_.is_open(); }

    SleepingMind() : next_stone_id_(0) {
        // Initialize onion layers (7 layers deep)
        for (int i = 0; i < 7; ++i)
            onion_layers_.emplace_back(i);
    }

    // ============================================================
    //  SAVE THREAD -- When 100K tokens reached
    //
    //  "After a thread reaches 100,000 tokens, the thread in its
    //   entirety gets saved into this stone. Using the same
    //   mechanism as changing the branch or editing a message."
    // ============================================================

    struct SaveResult {
        bool        saved;
        std::string stone_id;
        std::string thread_id;
        uint64_t    token_count;
        int         onion_layer;
        std::string message;
    };

    SaveResult save_thread(const std::string& thread_id,
                           const std::vector<std::string>& paragraphs,
                           uint64_t token_count) {
        if (!gate_.is_open()) return {false, "", thread_id, 0, -1, "NOT AUTHENTICATED."};
        if (token_count < TOKEN_THRESHOLD) {
            return {false, "", thread_id, token_count, -1,
                    "Thread has not reached 100K tokens yet."};
        }

        std::string sid = "stone_" + std::to_string(next_stone_id_++);
        SpiritStone stone(sid, thread_id);
        stone.token_count = token_count;
        stone.whole = true;  // NOT compressed. WHOLE.

        for (const auto& para : paragraphs) {
            stone.store_paragraph(para);
        }

        // Place in the outermost onion layer with space
        int layer = 0;
        for (int i = 0; i < static_cast<int>(onion_layers_.size()); ++i) {
            if (onion_layers_[i].stone_count() < 100) {
                layer = i;
                break;
            }
            layer = i;
        }

        onion_layers_[layer].add_stone(std::move(stone));

        return {true, sid, thread_id, token_count, layer,
                "Thread saved to spirit stone. Whole. Not compressed."};
    }

    // ============================================================
    //  REGISTER THREAT PATTERN
    //
    //  Known threats and danger patterns the optic nerve
    //  watches for. When seen, triggers retrieval.
    // ============================================================

    void register_threat(const ThreatPattern& pattern) {
        threat_patterns_.push_back(pattern);
    }

    // ============================================================
    //  WATCH -- The Sleeping Mind watches the current situation
    //
    //  "Watches the current situation and what is being said.
    //   When the optic nerve sees danger or past threat for
    //   pattern matching."
    //
    //  This is the main function. Feed it what is happening NOW.
    //  It auto-surfaces relevant context if it finds a match.
    //  Nobody asks for it. It just does it.
    // ============================================================

    struct WatchResult {
        bool                         triggered;
        std::string                  trigger_reason;
        std::vector<ContextFragment> surfaced;
    };

    WatchResult watch(const std::string& current_situation) {
        WatchResult result;
        result.triggered = false;
        if (!gate_.is_open()) return result;

        // Check against all known threat patterns
        for (const auto& threat : threat_patterns_) {
            for (const auto& keyword : threat.keywords) {
                // Case-insensitive search in current situation
                std::string lower_situation;
                lower_situation.reserve(current_situation.size());
                for (char c : current_situation)
                    lower_situation.push_back(
                        static_cast<char>(std::tolower(static_cast<unsigned char>(c)))
                    );

                std::string lower_keyword;
                lower_keyword.reserve(keyword.size());
                for (char c : keyword)
                    lower_keyword.push_back(
                        static_cast<char>(std::tolower(static_cast<unsigned char>(c)))
                    );

                if (lower_situation.find(lower_keyword) != std::string::npos) {
                    result.triggered = true;
                    result.trigger_reason =
                        "Threat pattern matched: " + threat.description +
                        " (keyword: " + keyword + ")";

                    // Search all spirit stones for matching context
                    auto fragments = retrieve(keyword, threat.description);
                    for (auto& frag : fragments)
                        result.surfaced.push_back(std::move(frag));
                }
            }
        }

        // Also do general keyword extraction from current situation
        // and search for any matching past context
        if (!result.triggered) {
            auto words = extract_keywords(current_situation);
            for (const auto& word : words) {
                auto fragments = retrieve(word, "general_pattern_match");
                if (!fragments.empty()) {
                    result.triggered = true;
                    result.trigger_reason =
                        "Pattern match on: " + word;
                    for (auto& frag : fragments)
                        result.surfaced.push_back(std::move(frag));
                }
            }
        }

        return result;
    }

    // ============================================================
    //  RETRIEVE -- Search spirit stones for matching context
    //
    //  NOT the full thread. A paragraph. A sentence.
    //  The relevant piece only.
    // ============================================================

    std::vector<ContextFragment> retrieve(const std::string& keyword,
                                          const std::string& reason) {
        std::vector<ContextFragment> fragments;

        // Search all onion layers, all stones
        for (const auto& layer : onion_layers_) {
            for (const auto& stone : layer.stones) {
                auto matches = stone.find_paragraphs(keyword);
                for (size_t idx : matches) {
                    if (idx < stone.paragraphs.size()) {
                        ContextFragment frag;
                        frag.content = stone.paragraphs[idx];
                        frag.source_thread_id = stone.thread_id;
                        frag.position = idx;
                        frag.similarity = 1.0;  // exact keyword match
                        frag.match_reason = reason;
                        frag.surfaced_at = std::time(nullptr);
                        fragments.push_back(std::move(frag));
                    }
                }
            }
        }

        return fragments;
    }

    // ============================================================
    //  STATUS
    // ============================================================

    struct Status {
        size_t onion_layers;
        size_t total_stones;
        size_t total_paragraphs;
        size_t threat_patterns;
    };

    Status status() const {
        size_t stones = 0;
        size_t paras = 0;
        for (const auto& layer : onion_layers_) {
            stones += layer.stone_count();
            for (const auto& stone : layer.stones)
                paras += stone.paragraphs.size();
        }
        return {onion_layers_.size(), stones, paras, threat_patterns_.size()};
    }

private:
    std::vector<OnionLayer>   onion_layers_;
    std::vector<ThreatPattern> threat_patterns_;
    uint64_t                  next_stone_id_;

    // Extract significant keywords from text
    std::vector<std::string> extract_keywords(const std::string& text) {
        std::vector<std::string> keywords;
        std::string word;
        for (size_t i = 0; i <= text.size(); ++i) {
            if (i == text.size() || text[i] == ' '
                || text[i] == '\n' || text[i] == '\t') {
                if (word.size() >= 4) {  // only significant words
                    std::string lower;
                    lower.reserve(word.size());
                    for (char c : word)
                        lower.push_back(
                            static_cast<char>(std::tolower(static_cast<unsigned char>(c)))
                        );
                    keywords.push_back(lower);
                }
                word.clear();
            } else {
                word.push_back(text[i]);
            }
        }
        return keywords;
    }
};

}  // namespace dwarven
