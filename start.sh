#!/usr/bin/bash

export SDOP_DB_NAME= # db name
export SDOP_DB_USER= # user name
export SDOP_DB_PASS= # user pass

if [ ! -d "database" ]; then
  mkdir database
fi
if [ ! -d "trash" ]; then
  mkdir trash
fi

docker compose build
docker compose up
