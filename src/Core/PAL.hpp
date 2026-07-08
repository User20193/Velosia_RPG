#pragma once
namespace Velosia::Core {
    class PAL {
    public:
        static void Init();
        static void Shutdown();
        static double GetTime();
    };
}
