#include "Logger.hpp"

namespace Velosia::Core {
    void Logger::Init() { std::cout << "[Velosia Engine] Logger Initialized." << std::endl; }
    void Logger::Log(LogLevel level, const std::string& message) {
        switch (level) {
            case LogLevel::Info: std::cout << "[INFO]: " << message << std::endl; break;
            case LogLevel::Warning: std::cout << "[WARN]: " << message << std::endl; break;
            case LogLevel::Error: std::cerr << "[ERROR]: " << message << std::endl; break;
            case LogLevel::Fatal: std::cerr << "[FATAL]: " << message << std::endl; break;
        }
    }
}
