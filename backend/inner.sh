#!/bin/bash
set -e
echo "# Formatting"
python -m black $HOME/github.com/loicbourgois/downtowhat
# echo "# Linting"
# pylint --jobs=0 \
#     --rcfile $HOME/github.com/loicbourgois/downtowhat/pylintrc \
#     $HOME/github.com/loicbourgois/downtowhat/backend
echo "# Run"
cd $HOME/github.com/loicbourgois/downtowhat
python -m backend.main
