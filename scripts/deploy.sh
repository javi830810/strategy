#!/bin/bash

cd /root/strategy
git pull

docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
docker rmi $(docker images -aq)

docker-compose up -d