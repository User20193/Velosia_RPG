#include "ResourceManager.hpp"
#include "../Core/Logger.hpp"

namespace Velosia::Engine {

    ResourceManager::~ResourceManager() {
        ClearTextures();
        ClearFonts();
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

    int ResourceManager::GetTextureWidth(const std::string& id) {
        auto it = textures.find(id);
        if (it != textures.end()) {
            return it->second.width;
        }
        return 0;
    }

    int ResourceManager::GetTextureHeight(const std::string& id) {
        auto it = textures.find(id);
        if (it != textures.end()) {
            return it->second.height;
        }
        return 0;
    }

    void ResourceManager::LoadFontAsset(const std::string& id, const std::string& filepath) {
        if (fonts.find(id) != fonts.end()) return;

        // Load font with Cyrillic support (UTF-8 mapping)
        // Raylib's default LoadFont only maps basic ASCII. For TTF files with Cyrillic,
        // we must use LoadFontEx and provide an array of codepoints.
        // We will load the basic ASCII + Cyrillic block (0x0400 to 0x04FF)

        int codepointCount = 512;
        int* codepoints = new int[codepointCount];
        int idx = 0;

        // Basic Latin (ASCII)
        for (int i = 32; i < 127; i++) codepoints[idx++] = i;
        // Cyrillic
        for (int i = 0x0400; i < 0x04FF; i++) codepoints[idx++] = i;

        // Fill the rest with 0 just in case
        while (idx < codepointCount) codepoints[idx++] = 0;

        Font font = ::LoadFontEx(filepath.c_str(), 64, codepoints, codepointCount);
        delete[] codepoints;

        if (font.texture.id > 0) {
            fonts[id] = font;
            Core::Logger::Info("ResourceManager: Loaded font '" + id + "' with Cyrillic support");
        } else {
            Core::Logger::Error("ResourceManager: Failed to load font '" + id + "'");
        }
    }

    Font* ResourceManager::GetFont(const std::string& id) {
        auto it = fonts.find(id);
        if (it != fonts.end()) return &it->second;
        return nullptr;
    }

    void ResourceManager::ClearFonts() {
        for (auto& pair : fonts) {
            ::UnloadFont(pair.second);
        }
        fonts.clear();
    }

}
