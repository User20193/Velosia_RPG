#include "DisplayManager.hpp"
#include <raylib.h>

namespace Velosia::Engine {

    // Internal state tracking
    static int internalWidth = 800;
    static int internalHeight = 600;

    void DisplayManager::SetInternalResolution(int width, int height) {
        internalWidth = width;
        internalHeight = height;
    }

    void DisplayManager::SetWindowSize(int width, int height) {
        ::SetWindowSize(width, height);
    }

    void DisplayManager::ToggleFullscreen() {
        ::ToggleFullscreen();
    }

    void DisplayManager::SetBorderless(bool borderless) {
        if (borderless) {
            SetWindowState(FLAG_WINDOW_UNDECORATED);
        } else {
            ClearWindowState(FLAG_WINDOW_UNDECORATED);
        }
    }

    int DisplayManager::GetInternalWidth() { return internalWidth; }
    int DisplayManager::GetInternalHeight() { return internalHeight; }
    int DisplayManager::GetWindowWidth() { return GetScreenWidth(); }
    int DisplayManager::GetWindowHeight() { return GetScreenHeight(); }

}
