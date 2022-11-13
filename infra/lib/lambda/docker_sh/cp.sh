#!/bin/bash

# Usage:
#   CONTAINER_NAME=xxx
#   ./docker_cp.sh $CONTAINER_NAME ./[copy from the container dir] ./[copy to the host dir]

CONTAINER_NAME=$1
docker run -d $CONTAINER_NAME:latest
CONTAINER_ID=$(docker ps | grep $CONTAINER_NAME | awk '{print $1}')
docker cp $CONTAINER_ID:$2 $3
docker rm -f $CONTAINER_ID
