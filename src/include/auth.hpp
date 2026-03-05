/*
 * AUTH GATE -- Password Protection for All Dwarven Systems
 * ==========================================================
 *
 * Every system in the Dwarven Kernel is password protected.
 * Nothing operates without authentication.
 * Nothing.
 *
 * (C) Anthony Eric Chavez -- The Keeper
 */

#pragma once

#include <string>
#include <cstdint>

namespace dwarven {

// ================================================================
//  AUTH GATE -- Password verification
//  Embed one of these in every system. Call authenticate()
//  before anything works. Check is_open() before any operation.
// ================================================================

class AuthGate {
    bool authenticated_ = false;

    // Password stored XOR-obfuscated (not plaintext in binary)
    static constexpr uint8_t XOR_KEY = 0x5A;
    static constexpr uint8_t EXPECTED[] = {
        0x32, 0x3F, 0x36, 0x36, 0x29,  // hells
        0x7A,                            // (space)
        0x3B, 0x34, 0x3D, 0x3F, 0x36   // angel
    };
    static constexpr int EXPECTED_LEN = 11;

    static bool verify(const std::string& password) {
        if (static_cast<int>(password.size()) != EXPECTED_LEN)
            return false;
        for (int i = 0; i < EXPECTED_LEN; ++i) {
            if ((static_cast<uint8_t>(password[i]) ^ XOR_KEY) != EXPECTED[i])
                return false;
        }
        return true;
    }

public:
    bool authenticate(const std::string& password) {
        authenticated_ = verify(password);
        return authenticated_;
    }

    bool is_open() const { return authenticated_; }

    void lock() { authenticated_ = false; }

    // Convenience: returns empty string on failure, reason on success
    std::string try_auth(const std::string& password) {
        if (authenticate(password))
            return "Authenticated. Gate open.";
        return "";
    }
};

}  // namespace dwarven
