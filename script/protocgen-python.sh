#!/bin/bash

# Python protobuf generation script
set -euo pipefail

AKASH_ROOT=${AKASH_ROOT:-$(pwd)}
PYTHON_OUT_DIR="$AKASH_ROOT/gen/py"
PYTHON_PKG_DIR="${AKASH_PYTHON_PACKAGE:-$AKASH_ROOT/python/src/akash_api}"

echo "Generating Python protobuf code..."

# Create output directory
mkdir -p "$PYTHON_OUT_DIR"

# Use the Python environment or system Python
PYTHON_CMD=${PYTHON:-python3}

# Collect all proto paths
PROTO_PATHS=(
    "$AKASH_ROOT/proto/node"
    "$AKASH_ROOT/proto/provider"
    "$AKASH_ROOT/vendor/github.com/cosmos/cosmos-sdk/proto"
    "$AKASH_ROOT/vendor/github.com/cosmos/cosmos-sdk/third_party/proto"
    "$AKASH_ROOT/vendor/github.com/cosmos/cosmos-proto/proto"
    "$AKASH_ROOT/vendor/k8s.io/apimachinery"
)

# Build protoc path arguments
PROTOC_PATHS=""
for path in "${PROTO_PATHS[@]}"; do
    if [ -d "$path" ]; then
        PROTOC_PATHS="$PROTOC_PATHS --proto_path=$path"
    fi
done

# Find all proto files and generate Python code
find "$AKASH_ROOT/proto" -name "*.proto" -type f | while read -r proto_file; do
    echo "Processing: $proto_file"
    
    # Get the relative path from the nearest proto root
    if [[ "$proto_file" == *"/proto/node/"* ]]; then
        rel_path=$(realpath --relative-to="$AKASH_ROOT/proto/node" "$proto_file")
        base_path="$AKASH_ROOT/proto/node"
    elif [[ "$proto_file" == *"/proto/provider/"* ]]; then
        rel_path=$(realpath --relative-to="$AKASH_ROOT/proto/provider" "$proto_file")
        base_path="$AKASH_ROOT/proto/provider"
    else
        rel_path=$(realpath --relative-to="$AKASH_ROOT/proto" "$proto_file")
        base_path="$AKASH_ROOT/proto"
    fi
    
    # Generate Python code, continue on errors
    $PYTHON_CMD -m grpc_tools.protoc \
        $PROTOC_PATHS \
        --python_out="$PYTHON_OUT_DIR" \
        --grpc_python_out="$PYTHON_OUT_DIR" \
        --proto_path="$base_path" \
        "$rel_path" || echo "Warning: Failed to process $proto_file, continuing..."
done

echo "Python protobuf code generation completed."

# Copy generated code to the Python package
if [ -d "$PYTHON_OUT_DIR/akash" ]; then
    echo "Copying generated code to Python package..."
    mkdir -p "$PYTHON_PKG_DIR"
    cp -r "$PYTHON_OUT_DIR/akash" "$PYTHON_PKG_DIR/"
    
    # Create __init__.py files in all subdirectories
    find "$PYTHON_PKG_DIR/akash" -type d -exec touch {}/__init__.py \;
    
    echo "Python package updated successfully."
fi
