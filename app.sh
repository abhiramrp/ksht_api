#! /usr/bin/env bash

docker-compose down
docker-compose up

echo 'Build complete'

docker-compose logs | grep error
