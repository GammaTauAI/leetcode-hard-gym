#!/bin/bash

# run_build.sh

python3 build.py \
    --langs python3 rust  \
    --log_level INFO \
    --output_dir ./build \
#    --extract_test_cases \
#    --remove_examples \
