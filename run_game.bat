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

:: Get exact Python path to ensure CMake compiles for the same version we use to run the game
for /f "delims=" %%I in ('python -c "import sys; print(sys.executable)"') do set PYTHON_EXE=%%I
echo [INFO] Using Python at: %PYTHON_EXE%

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

:: Detect Compiler and run CMake Configuration
echo [INFO] Configuring CMake...

:: Check if GCC (MinGW) is available
gcc --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [INFO] GCC detected. Using MinGW Makefiles.
    :: -DCMAKE_POLICY_VERSION_MINIMUM=3.5 prevents errors with newer CMake versions when compiling third-party libraries (like Raylib) that have old minimum version requirements.
    cmake .. -G "MinGW Makefiles" -DCMAKE_POLICY_VERSION_MINIMUM=3.5 -DPython3_EXECUTABLE="%PYTHON_EXE%"
) else (
    echo [INFO] GCC not detected. Using default generator.
    cmake .. -DCMAKE_POLICY_VERSION_MINIMUM=3.5 -DPython3_EXECUTABLE="%PYTHON_EXE%"
)

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] CMake configuration failed!
    echo Please ensure you have a C++ Compiler installed and in your PATH ^(e.g., MinGW-w64 or MSVC^).
    pause
    exit /b 1
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
