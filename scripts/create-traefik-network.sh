#!/bin/sh
set -e

loadenv() {
    if [ -f .env ]; then
        while read -r a; do
            export "${a?}"
        done < .env
    fi
}

loadenv

NETWORK_NAME="${NETWORK_NAME:-traefik}"

# Remove network if it exists
docker network ls --format="{{.Name}}" | grep -E "^${NETWORK_NAME}$" \
    && docker network rm "${NETWORK_NAME}"

# Create a fresh new network
docker network create \
       --attachable \
       -o 'com.docker.network.bridge.name'="${NETWORK_NAME}" \
       "${NETWORK_NAME}"
