#!/bin/bash

echo "Cleaning generated files..."

rm -f data/raw/*.csv
rm -f data/raw/*.json
rm -f data/processed/*.csv

echo "Cleanup completed."
