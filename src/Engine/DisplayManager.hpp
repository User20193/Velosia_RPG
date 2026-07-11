#pragma once

namespace Velosia::Engine {

    class DisplayManager {
    public:
        // Set the internal resolution (the canvas size where the game logic actually happens)
        static void SetInternalResolution(int width, int height);

        // Set the external window size
        static void SetWindowSize(int width, int height);

        // Toggle Fullscreen mode
        static void ToggleFullscreen();

        // Toggle Borderless window mode
        static void SetBorderless(bool borderless);

        // Getters
        static int GetInternalWidth();
        static int GetInternalHeight();
        static int GetWindowWidth();
        static int GetWindowHeight();
    };

}
