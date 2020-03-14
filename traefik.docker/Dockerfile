FROM traefik:2.2

ADD entrypoint.sh /custom-entrypoint.sh

RUN chmod a+x /custom-entrypoint.sh

ENTRYPOINT ["/custom-entrypoint.sh"]

CMD ["traefik"]
