FROM traefik:1.7-alpine

ADD entrypoint.sh /custom-entrypoint.sh

RUN chmod a+x /custom-entrypoint.sh

ENTRYPOINT ["/custom-entrypoint.sh"]
