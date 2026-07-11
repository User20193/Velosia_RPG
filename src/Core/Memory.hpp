#pragma once
#include <cstddef>
namespace Velosia::Core {
    class Memory {
    public:
        static void Init();
        static void* Allocate(size_t size);
        static void Free(void* ptr);
        static void Shutdown();
    };
}
