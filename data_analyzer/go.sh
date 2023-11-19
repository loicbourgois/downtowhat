#!/bin/sh
set -e
docker compose \
  --file $HOME/github.com/loicbourgois/downtowhat/data_analyzer/docker-compose \
  up \
  --renew-anon-volumes --build --force-recreate --remove-orphans
