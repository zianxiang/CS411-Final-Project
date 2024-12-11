#!/bin/bash

# Variables
IMAGE_NAME = "weather_dashboard"
CONTAINER_TAG = "0.1.0"
HOST_PORT = 5000
CONTAINER_PORT = 5000
VOLUME_PATH = "./data"   # Adjusting this to the desired host path for persistent storage
BUILD = true  # Setting this to true if you want to build the image

# Checking if we need to build thae Docker image
if [ "$BUILD" = true ]; then
  echo "Building Docker image..."
  docker build -t ${IMAGE_NAME}:${CONTAINER_TAG} .
else
  echo "Skipping Docker image build..."
fi

# Checking if the volume directory exists; if not, to create 
if [ ! -d "${VOLUME_PATH}" ]; then
  echo "Creating volume directory at ${VOLUME_PATH}..."
  mkdir -p ${VOLUME_PATH}
fi

# Running the Docker container with the necessary ports and volume mappings!
echo "Running Docker container..."
docker run -d \
  --name ${IMAGE_NAME}_container \
  --env-file .env \
  -p ${HOST_PORT}:${CONTAINER_PORT} \
  -v ${VOLUME_PATH}:/app/data \
  ${IMAGE_NAME}:${CONTAINER_TAG}

echo "Docker container is running on port ${HOST_PORT}."
