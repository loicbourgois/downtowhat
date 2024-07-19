#!/bin/sh
set -e
cd /root/github.com/loicbourgois/downtowhat
echo "Starting app"
gunicorn --reload $(find app/templates -type f -name '*.html' -exec echo --reload-extra-file {} \;) --bind 0.0.0.0:8080 --workers 1 'app.main:app'
