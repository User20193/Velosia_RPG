@echo off
echo ==========================================
echo    VELOSIA RPG - Developer Build Script
echo ==========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python 3 is not installed or not in PATH!
    echo Please install Python 3 from python.org
    pause
    exit /b 1
)

:: Check if CMake is installed
cmake --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] CMake is not installed or not in PATH!
    echo Please install CMake from cmake.org
    pause
    exit /b 1
)

echo [INFO] Tools detected. Starting build process...
echo.

:: Create build directory if it doesn't exist
if not exist "build" mkdir build
cd build

:: Run CMake Configuration
echo [INFO] Configuring CMake...
:: Try configuring default (usually MSVC if installed), otherwise fallback to MinGW Makefiles if GCC is used
cmake ..
if %errorlevel% neq 0 (
    echo [WARN] Default generator failed. Attempting MinGW Makefiles...
    cmake .. -G "MinGW Makefiles"
    if %errorlevel% neq 0 (
        echo.
        echo [ERROR] CMake configuration failed!
        echo Please ensure you have a C++ Compiler installed and in your PATH ^(e.g., MinGW-w64 or MSVC^).
        pause
        exit /b 1
    )
)

:: Build the Engine
echo.
echo [INFO] Compiling C++ Core Engine...
cmake --build . --config Release
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Compilation failed! Check the errors above.
    pause
    exit /b 1
)

:: Run the Game
echo.
echo [INFO] Build successful! Launching Velosia RPG...
cd ..
python src\Game\main.py

echo.
echo [INFO] Game closed.
pause
