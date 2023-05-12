#!/usr/bin/bash

export SDOP_DB_NAME= # db name
export SDOP_DB_USER= # user name
export SDOP_DB_PASS= # user pass

mkdir database
mkdir trash

docker compose build .
docker compose up