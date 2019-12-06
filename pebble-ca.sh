#!/bin/sh
set -e
mkdir -p /etc/traefik/certs
cd /etc/traefik/certs
rm -rf localhost
mkdir -p ca localhost
export GOPATH=/opt/go

[ ! -f /opt/go/bin/minica ] && go get github.com/jsha/minica

/opt/go/bin/minica \
    -ca-cert ca/cert.pem \
    -ca-key ca/cert.key \
    -domains localhost,pebble \
    -ip-addresses 127.0.0.1 \
    || true

chmod -R go+r ca localhost
