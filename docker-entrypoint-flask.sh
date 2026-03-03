#!/bin/sh
set -e

# A positive integer generally in the 2-4 x $(NUM_CORES) range.
WORKER_PROCESSES=${WORKERS:-4}

echo "Starting py-ard service with" "${WORKER_PROCESSES}" worker processes.

if [ "${WORKER_PROCESSES}" != "1" ]; then
  WORKER_FLAG="--workers=${WORKER_PROCESSES}"
fi

# Import the latest pyard before starting the app
echo "Importing py-ard latest IPD/IMGT version: "
pyard-import

# shellcheck disable=SC2086
gunicorn -c gunicorn_config.py ${WORKER_FLAG} app:app
