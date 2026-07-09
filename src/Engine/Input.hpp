#pragma once
#include <raylib.h>

namespace Velosia::Engine {

    class Input {
    public:
        // Expose a few keycodes for Python (mapping directly to Raylib's KEY_*)
        enum class Key {
            W = KEY_W,
            A = KEY_A,
            S = KEY_S,
            D = KEY_D,
            UP = KEY_UP,
            DOWN = KEY_DOWN,
            LEFT = KEY_LEFT,
            RIGHT = KEY_RIGHT,
            SPACE = KEY_SPACE,
            ENTER = KEY_ENTER,
            ESCAPE = KEY_ESCAPE
        };

        static bool IsKeyPressed(Key key) { return ::IsKeyPressed(static_cast<int>(key)); }
        static bool IsKeyDown(Key key) { return ::IsKeyDown(static_cast<int>(key)); }
        static bool IsKeyReleased(Key key) { return ::IsKeyReleased(static_cast<int>(key)); }
        static bool IsKeyUp(Key key) { return ::IsKeyUp(static_cast<int>(key)); }
    };

}
