from debian:10-slim

RUN apt-get update -y && apt-get install -y \
  unbound python3-unbound python3 python3-pip python3-dnspython
COPY unbound.conf /etc/unbound/unbound.conf
COPY traefik.py /etc/unbound/traefik.py
CMD [ "unbound", "-d", "-p", "-v" ]
