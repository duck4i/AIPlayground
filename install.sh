#!/bin/bash

# Default CUDA is disabled
USE_CUDA=0

# Parse command line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --cuda) USE_CUDA=1 ;;
        *) echo "Unknown parameter: $1"; exit 1 ;;
    esac
    shift
done

if [ "$(uname)" == "Darwin" ]; then
    echo "Running on macOS with metal"
    CMAKE_ARGS="-DLLAMA_METAL=on" pip3 install llama-cpp-python --upgrade --force-reinstall
elif [ "$(uname)" = "Linux" ]; then
    if [ "$USE_CUDA" -eq 1 ]; then
        echo "Running on Linux with CUDA enabled"
        CMAKE_ARGS="-DGGML_CUDA=on" pip3 install llama-cpp-python
    else
        echo "Running on Linux without CUDA"
        pip3 install llama-cpp-python
    fi
else
    echo "Running on other platforms..."
    pip3 install llama-cpp-python
fi

pip3 install -r requirements.txt