#include "ResourceManager.hpp"
#include "../Core/Logger.hpp"

namespace Velosia::Engine {

    ResourceManager::~ResourceManager() {
        ClearTextures();
    }

    void ResourceManager::LoadTexture(const std::string& id, const std::string& filepath) {
        if (textures.find(id) != textures.end()) {
            Core::Logger::Warn("ResourceManager: Texture ID '" + id + "' is already loaded.");
            return;
        }

        Texture2D texture = ::LoadTexture(filepath.c_str());

        // Raylib returns ID > 0 if successful
        if (texture.id > 0) {
            textures[id] = texture;
            Core::Logger::Info("ResourceManager: Loaded texture '" + id + "' from " + filepath);
        } else {
            Core::Logger::Error("ResourceManager: Failed to load texture '" + id + "' from " + filepath);
        }
    }

    Texture2D* ResourceManager::GetTexture(const std::string& id) {
        auto it = textures.find(id);
        if (it != textures.end()) {
            return &it->second;
        }
        Core::Logger::Error("ResourceManager: Texture ID '" + id + "' not found.");
        return nullptr;
    }

    void ResourceManager::UnloadTexture(const std::string& id) {
        auto it = textures.find(id);
        if (it != textures.end()) {
            ::UnloadTexture(it->second);
            textures.erase(it);
            Core::Logger::Info("ResourceManager: Unloaded texture '" + id + "'");
        }
    }

    void ResourceManager::ClearTextures() {
        for (auto& pair : textures) {
            ::UnloadTexture(pair.second);
        }
        textures.clear();
        Core::Logger::Info("ResourceManager: Cleared all textures.");
    }

}
