FROM traefik:alpine

ADD entrypoint.sh /custom-entrypoint.sh

RUN chmod a+x /custom-entrypoint.sh

ENTRYPOINT ["/custom-entrypoint.sh"]
