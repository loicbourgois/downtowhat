#!/bin/sh
echo "Frontend at http://localhost"
docker-compose --file $HOME/github.com/loicbourgois/downtowhat/app/docker-compose.yml up --build
