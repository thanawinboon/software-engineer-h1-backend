#!/bin/bash

docker run -d -p 5432:5432 \
    --env POSTGRES_USER=postgres \
    --env POSTGRES_PASSWORD=postgres \
    --env POSTGRES_DB=postgres \
    --name backend \
    -v backend-db-vol:/var/lib/postgresql/data \
    postgres:12.2-alpine
