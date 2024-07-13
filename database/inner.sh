#!/bin/sh
set -e
dtw_DATABASE_USER=dtw_local_dev_user
dtw_DATABASE_DBNAME=dtw_local_dev
dtw_DATABASE_PASSWORD=dtw_local_dev_password
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	CREATE USER dtw_local_dev_user;
	alter user dtw_local_dev_user password 'dtw_local_dev_password';
	CREATE DATABASE dtw_local_dev;
	GRANT ALL PRIVILEGES ON DATABASE dtw_local_dev TO dtw_local_dev_user;
EOSQL
PGPASSWORD=$dtw_DATABASE_PASSWORD psql -v ON_ERROR_STOP=1 \
	--username $dtw_DATABASE_USER \
	--dbname $dtw_DATABASE_DBNAME \
	-c "\timing" \
	-f /migrations/001/02_query.sql
	# \
	#-f /test_1.sql \
	#2>&1 | tee /var/lib/postgresql/logs.txt
