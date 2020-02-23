#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o xtrace

exec /usr/local/bin/gunicorn  \
  --chdir /safetynet          \
  --bind 0.0.0.0:5000         \
  --workers 3                 \
  wsgi:app
