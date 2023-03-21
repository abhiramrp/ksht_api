#! /usr/bin/env bash

chmod +x prestart.sh
source venv/bin/activate
docker-compose down -v
# docker-compose up -d
docker-compose -f docker-compose.yml up -d --build


echo 'Build complete'