#!/bin/bash

# Usage:
#   CONTAINER_NAME=xxx
#   ./docker_sh/sleep_until_server_starts.sh $CONTAINER_NAME

CONTAINER_NAME=$1
TMP_DIR=tmp_for_check_the_docker_deamon_running

mkdir -p ./$TMP_DIR
echo 'FROM scratch' >> ./$TMP_DIR/Dockerfile

while :
do
    echo 'waiting for docker daemon to be ready...'

    str=$(docker exec -it $CONTAINER_NAME docker build ./$TMP_DIR 2> /dev/null)
    str_len=${#str}
    if [ $str_len == 0 ]; then
	sleep 0.5
    elif [[ $str =~ 'not connect to the Docker daemon' ]]; then
	sleep 0.5
    else
        break
    fi
done

rm -rf ./$TMP_DIR
exit 0
