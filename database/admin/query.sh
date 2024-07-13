#!/bin/sh
psql -v ON_ERROR_STOP=1 \
  postgresql://dtw_local_dev_user:dtw_local_dev_password@localhost:5432/dtw_local_dev \
  -c "\timing" \
  -f /admin/query.sql 
  #\
  #--csv \
  #-o /queries/_default/result.csv
