#!/bin/sh
set -e
# Removing letsencrypt generated cache
rm /var/run/acme.json || true
exec /entrypoint.sh "$@"
