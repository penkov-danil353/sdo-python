#!/usr/bin/bash

export SDOP_DB_NAME= # db name
export SDOP_DB_USER= # user name
export SDOP_DB_PASS= # user pass

docker volume create db-data
docker volume create trash

docker compose build
docker compose start
