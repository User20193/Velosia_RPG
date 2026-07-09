#pragma once

#include <raylib.h>
#include <string>
#include <unordered_map>
#include <memory>

namespace Velosia::Engine {

    class ResourceManager {
    public:
        static ResourceManager& GetInstance() {
            static ResourceManager instance;
            return instance;
        }

        // Load a texture into VRAM if not already loaded, and return its string ID
        void LoadTexture(const std::string& id, const std::string& filepath);

        // Retrieve a loaded texture pointer (returns nullptr if not found)
        Texture2D* GetTexture(const std::string& id);

        // Unload a specific texture
        void UnloadTexture(const std::string& id);

        // Unload all textures (useful for changing scenes/levels)
        void ClearTextures();

    private:
        ResourceManager() = default;

        std::unordered_map<std::string, Texture2D> textures;

    public:
        // Must be public so Pybind11 can clean it up (though it's a singleton)
        ~ResourceManager();
    };

}
