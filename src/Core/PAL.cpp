#include "PAL.hpp"
#include "Logger.hpp"
#include <chrono>

namespace Velosia::Core {
    void PAL::Init() { Logger::Info("PAL (Platform Abstraction Layer) Initialized."); }
    void PAL::Shutdown() { Logger::Info("PAL Shutdown."); }
    double PAL::GetTime() {
        auto now = std::chrono::high_resolution_clock::now();
        return std::chrono::duration<double>(now.time_since_epoch()).count();
    }
}
