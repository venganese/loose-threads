#!/usr/bin/env bash
# Fetches everything the About page needs to run its model from YOUR site:
#   vendor/  transformers.js 3.8.1 + ONNX WebAssembly runtime   (~22 MB)
#   models/  all-MiniLM-L6-v2, 8-bit                            (~23 MB)
# Run once from the loose-threads folder:  bash download_model.sh
set -euo pipefail
cd "$(dirname "$0")"

LIB="https://cdn.jsdelivr.net/npm/@huggingface/transformers@3.8.1/dist"
for f in transformers.min.js ort-wasm-simd-threaded.jsep.mjs ort-wasm-simd-threaded.jsep.wasm; do
  echo "↓ vendor/$f"
  curl -fL --create-dirs -o "vendor/$f" "$LIB/$f"
done

MODEL="https://huggingface.co/Xenova/all-MiniLM-L6-v2/resolve/main"
DEST="models/Xenova/all-MiniLM-L6-v2"
for f in config.json tokenizer.json tokenizer_config.json onnx/model_quantized.onnx; do
  echo "↓ $DEST/$f"
  curl -fL --create-dirs -o "$DEST/$f" "$MODEL/$f"
done

echo "Done:"; du -sh vendor models
