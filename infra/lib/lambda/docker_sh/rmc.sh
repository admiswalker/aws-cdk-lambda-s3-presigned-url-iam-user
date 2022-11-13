#!/bin/bash

# Usage:
#   CONTAINER_NAME=xxx
#   ./docker_rmc.sh $CONTAINER_NAME

CONTAINER_NAME=$1

CONTAINER_ID=$(docker ps -a | grep $CONTAINER_NAME | awk '{print $1}')
str_len=${#CONTAINER_ID}
if [ $str_len -eq 0 ]; then
    exit 0
fi

docker rm -f $CONTAINER_ID
