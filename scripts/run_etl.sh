#!/bin/bash

echo "========================================="
echo "Starting Customer ETL Environment"
echo "========================================="

docker compose up -d

echo ""
echo "Docker containers started."

echo ""
echo "Open Airflow:"
echo "http://localhost:8080"

echo ""
echo "Trigger the DAG: customer_etl_pipeline"
