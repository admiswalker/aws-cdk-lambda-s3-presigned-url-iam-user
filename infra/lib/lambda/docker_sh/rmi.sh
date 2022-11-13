#!/bin/bash

# Usage:
#   CONTAINER_NAME=xxx
#   ./docker_rmi.sh $CONTAINER_NAME

CONTAINER_NAME=$1
IMAGE_ID_str=$(docker inspect --format="{{.Id}}" $CONTAINER_NAME 2> /dev/null ) # sha256:80a2138b2d88c11a2e556b162d6a42d720aeabc9bc512122b66d6edc86d05037
IMAGE_ID_str=$(echo `echo "$IMAGE_ID_str" | tr ':' ' '`)          # sha256 80a2138b2d88c11a2e556b162d6a42d720aeabc9bc512122b66d6edc86d05037

for s in $IMAGE_ID_str; do
    IMAGE_ID=$(echo $s) # get last item
done
str_len=${#IMAGE_ID}
if [ $str_len -eq 0 ]; then
    exit 0
fi

docker rmi $IMAGE_ID
