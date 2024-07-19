#!/bin/sh
source $HOME/github.com/loicbourgois/downtowhat_secrets/secrets.env
cd $HOME/github.com/loicbourgois/downtowhat/app
gcloud app deploy --project=$gcp_project \
    --account=$gcp_account
