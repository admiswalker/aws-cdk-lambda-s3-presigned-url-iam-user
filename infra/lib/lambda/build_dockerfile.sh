#!/bin/bash
CONTAINER_NAME=gen-deployment-package
GEN_TARGET=deployment-package.zip

docker build -t $CONTAINER_NAME ./
sh ./docker_sh/cp.sh $CONTAINER_NAME ./home/$GEN_TARGET .
sh ./docker_sh/rmi.sh $CONTAINER_NAME
