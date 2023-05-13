#!/usr/bin/bash

export SDOP_DB_NAME=sdo # db name
export SDOP_DB_USER=sdo_python # user name
export SDOP_DB_PASS=sidecuter # user pass

docker compose build
docker compose up
