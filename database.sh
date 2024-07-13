#!/bin/sh
file="$HOME/github.com/loicbourgois/downtowhat/database/docker-compose.yml"
docker-compose --file $file down
dir=$dir \
  environment=$environment \
  docker-compose --file $file up --build --force-recreate
