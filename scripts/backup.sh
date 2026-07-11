#!/bin/bash

mkdir -p backup

cp data/processed/*.csv backup/ 2>/dev/null

echo "Backup completed."
