#include "Memory.hpp"
#include "Logger.hpp"
#include <cstdlib>

namespace Velosia::Core {
    void Memory::Init() { Logger::Info("Memory Manager Initialized."); }
    void* Memory::Allocate(size_t size) { return std::malloc(size); }
    void Memory::Free(void* ptr) { std::free(ptr); }
    void Memory::Shutdown() { Logger::Info("Memory Manager Shutdown."); }
}
