#pragma once
#include <string>
#include <iostream>

namespace Velosia::Core {
    enum class LogLevel { Info, Warning, Error, Fatal };
    class Logger {
    public:
        static void Init();
        static void Log(LogLevel level, const std::string& message);
        static void Info(const std::string& message) { Log(LogLevel::Info, message); }
        static void Warn(const std::string& message) { Log(LogLevel::Warning, message); }
        static void Error(const std::string& message) { Log(LogLevel::Error, message); }
        static void Fatal(const std::string& message) { Log(LogLevel::Fatal, message); }
    };
}
