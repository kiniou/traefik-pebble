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

# Just exit if network does already exists
docker network ls --format="{{.Name}}" | grep -E "^${NETWORK_NAME}$" \
    && exit 0

# Create a fresh new network
docker network create \
       --attachable \
       --ipv6 \
       --subnet="172.18.0.0/16" \
       --subnet="fcdd:1::/48" \
       -o 'com.docker.network.bridge.name'="${NETWORK_NAME}" \
       "${NETWORK_NAME}"
