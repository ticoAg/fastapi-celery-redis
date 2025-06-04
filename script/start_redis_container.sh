#!/bin/bash

# Define Redis container name and password
CONTAINER_NAME="redis_for_celery"
REDIS_PASSWORD="redis_QPJSSf"

# Check if container already exists (regardless of running state)
if [ "$(docker inspect -f '{{.State.Running}}' $CONTAINER_NAME 2>/dev/null)" = "true" ]; then
    echo "Redis container is already running."
elif [ "$(docker inspect -f '{{.Config.Image}}' $CONTAINER_NAME 2>/dev/null)" = "redis:latest" ]; then
    echo "Redis container exists but is not running. Starting..."
    docker start $CONTAINER_NAME
else
    echo "Creating and starting new Redis container..."
    docker run --name $CONTAINER_NAME -d \
        -p 6379:6379 \
        -e REDIS_PASSWORD="$REDIS_PASSWORD" \
        redis:latest \
        redis-server --requirepass "$REDIS_PASSWORD"
fi

echo "Redis container status: $(docker inspect -f '{{.State.Status}}' $CONTAINER_NAME)"