# Traefik automatic ssl with pebble

This setup will spawn a ready to use Traefik container with automatic ssl generation with the simple ACME server [Pebble](https://github.com/letsencrypt/pebble)

## Setup

1. Install files to `/etc/traefik`.
2. Run `sudo ca-pebble.sh` to generate certificates as administrator.
3. [linux only] Install and start systemd `traefik.service`.
4. You should now have a ready-to-use SSL enabled Traefik proxy.

## Credits

- This setup is heavily inspired and borrowed from [PofMagicfingers](https://github.com/PofMagicfingers/traefik-pebble-stack)
