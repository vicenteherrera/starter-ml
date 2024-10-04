#!/bin/bash

MODEL="TinyLlama/TinyLlama-1.1B-Chat-v1.0"
MODEL_EXT="*.safetensors"
REVISION="main"

huggingface-cli download \
		"${MODEL}" \
		--revision "${REVISION}" \
		--include "${MODEL_EXT}" "*.json" "tokenizer.model" "*.txt"