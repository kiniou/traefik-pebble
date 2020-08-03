#!/bin/sh
set -x

# TODO: Move this in its own Dockerfile
apk add bash bind-tools

echo "Registering traefik service"
traefik_ip=""
while [ -z "${traefik_ip}" ]
do
    echo "Trying to resolve traefik domain name..."
    traefik_ip="$(dig +short traefik A)"
    sleep 1
done

cat <<EOF> /etc/consul.d/services.json
{
  "service": {
    "id": "traefik",
    "name": "traefik",
    "address": "${traefik_ip}"
  }
}
EOF

ARGS="-server -data-dir=/var/consul -config-dir=/etc/consul.d"
if [ -n "${CONSUL_ENCRYPT}" ]
then
    ARGS="${ARGS} -encrypt=${CONSUL_ENCRYPT}"
fi

if [ -n "${CONSUL_ADVERTISE}" ]
then
    ARGS="${ARGS} -advertise=${CONSUL_ADVERTISE}"
fi

consul agent ${ARGS} $*
