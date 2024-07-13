#!/bin/sh
docker-compose \
    --file $HOME/github.com/loicbourgois/downtowhat/backend/docker-compose \
    up \
    --build --force-recreate \
    --exit-code-from dtw_backend \
    dtw_backend
