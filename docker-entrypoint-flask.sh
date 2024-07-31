#!/bin/sh
set -e

# A positive integer generally in the 2-4 x $(NUM_CORES) range.
WORKER_PROCESSES=${WORKERS:-4}

echo "Starting Magenta with" "${WORKER_PROCESSES}" worker processes.

if [ "${WORKER_PROCESSES}" != "1" ]; then
  WORKER_FLAG="--workers=${WORKER_PROCESSES}"
fi

# Import pyard before starting the app
pyard-import

gunicorn --preload --bind 0.0.0.0:8080 --timeout 5000 --log-level info "${WORKER_FLAG}" app:app
