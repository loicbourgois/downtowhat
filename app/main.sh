#!/bin/sh
set -e
cd /root/github.com/loicbourgois/downtowhat
echo "Starting app"
gunicorn --bind 0.0.0.0:8080 --workers 2 'app.main:app'
