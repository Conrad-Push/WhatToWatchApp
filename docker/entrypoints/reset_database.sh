#!/usr/bin/env bash

PGPASSWORD=${POSTGRES_PASSWORD} psql -h ${POSTGRES_HOST} -p ${POSTGRES_PORT} -U ${POSTGRES_USERNAME} -d ${POSTGRES_NAME} -c \
"SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = '${POSTGRES_NAME}' AND pid <> pg_backend_pid();"

PGPASSWORD=${POSTGRES_PASSWORD} psql -h ${POSTGRES_HOST} -p ${POSTGRES_PORT} -U ${POSTGRES_USERNAME} -d postgres -c \
"DROP DATABASE IF EXISTS ${POSTGRES_NAME}"
PGPASSWORD=${POSTGRES_PASSWORD} psql -h ${POSTGRES_HOST} -p ${POSTGRES_PORT} -U ${POSTGRES_USERNAME} -d postgres -c \
"CREATE DATABASE ${POSTGRES_NAME};"
