#!/usr/bin/env bash
set -e

if [[ $# == 0 ]]; then
  /bin/bash
elif [[ $1 == "run-prod" ]]; then
  shift
  dockerize -timeout 120s -wait tcp://"${POSTGRES_HOST:-}":"${POSTGRES_PORT:-info}" && \
  dockerize -timeout 120s -wait tcp://"${MONGO_HOST:-}":"${MONGO_PORT:-27017}" && \
  python -m gunicorn WTW_app.app:app --log-level "${LOG_LEVEL:-info}" \
    --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind "${APP_HOST:-0.0.0.0}":"${APP_PORT:-5001}" \
    --access-logfile "-" "${@}"
elif [[ $1 == "run-dev" ]]; then
  shift
  dockerize -timeout 120s -wait tcp://"${POSTGRES_HOST:-}":"${POSTGRES_PORT:-info}" && \
  dockerize -timeout 120s -wait tcp://"${MONGO_HOST:-}":"${MONGO_PORT:-27017}" && \
  python -m uvicorn WTW_app.app:app --log-level "${LOG_LEVEL:-info}" \
    --host "${APP_HOST:-0.0.0.0}" --port "${APP_PORT:-5001}" --reload "${@}"
elif [[ $1 == "run-test" ]]; then
  shift
  source docker/entrypoints/run_tests.sh "$@"
else
  exec "$@"
fi
