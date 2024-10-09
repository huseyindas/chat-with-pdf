#!/bin/bash

if [[ $1 == "build" ]]; then
    COMMAND="up --build -d"
else
    COMMAND="up -d"
fi

if docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi > /dev/null 2>&1; then
    echo "GPU detected. Running docker-compose with GPU support."
    docker-compose -f docker-compose.yml -f docker-compose.gpu.yml $COMMAND
else
    echo "No GPU detected. Running docker-compose with CPU."
    docker-compose -f docker-compose.yml $COMMAND
fi
