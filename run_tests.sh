#!/bin/bash

if [ -f .env.pytest ]; then
    export $(grep -v '^#' .env.pytest | xargs)
else
    echo ".env.pytest file not found."
    exit 1
fi

pytest