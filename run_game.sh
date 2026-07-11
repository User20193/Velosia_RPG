#!/bin/bash
echo "=========================================="
echo "VELOSIA RPG - Developer Build Script"
echo "=========================================="

mkdir -p build
cd build
cmake ..
make -j$(nproc)
cd ..

echo "Starting Velosia Engine..."
LD_LIBRARY_PATH=./build python3 src/Game/main.py
