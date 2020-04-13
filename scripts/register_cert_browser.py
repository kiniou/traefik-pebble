#!/usr/bin/env python3
import requests
import click
import daiquiri
import logging
from pathlib import Path
from subprocess import run, PIPE
import io
daiquiri.setup()
log = logging.getLogger(__name__)
log_requests = logging.getLogger()
log_requests.setLevel(logging.DEBUG)
cert_nickname = "local-dev"
browsers_functions = {}


def register_browser(fn):
    browsers_functions[fn.__name__] = fn
    return fn


def _get_pebble_certificate():
    log.debug("fetch intermediate certificate from Pebble")
    response = requests.get("https://localhost:15000/roots/0", verify=False)
    log.debug("request: %s", response.request.url)
    log.debug("response: %s", response)
    log.debug("response data: %s", response.text)
    assert response.status_code == 200,\
        "Could not fetch intermediate certificate from Pebble"
    with open('pebble.crt', 'w') as certfile:
        certfile.write(response.text)
    return response.text


def _run(*args, **kwargs):
    """Just wrap subprocess.run() with debug and sane defaults"""
    kwargs.update({
        'stdout': PIPE,
        'stderr': PIPE,
    })

    result = run(*args, **kwargs)
    log.debug("%s", result)
    log.debug("code: %s", result.returncode)
    log.debug("stdout: %s", result.stdout.decode())
    log.debug("stderr: %s", result.stderr.decode())
    return result


@register_browser
def _register_chrome(**kwargs):
    cert_path_arg = kwargs.get('cert_path')
    log.debug(cert_path_arg)
    if cert_path_arg:
        cert_path = Path(cert_path_arg)
        with cert_path.open() as f:
            cert_txt = f.read()
    else:
        cert_txt = _get_pebble_certificate()
    log.debug("Register Certificate in Chrome")
    DB_PATH = Path('~/.pki/nssdb').expanduser()
    log.debug("DB_PATH: %s", DB_PATH)
    db_name = 'sql:{}'.format(DB_PATH)
    certutil_cmd = ['/usr/bin/env', 'certutil', '-d', db_name]
    _run(certutil_cmd + ['-D', '-n', cert_nickname])
    _run(certutil_cmd +
         ['-A', '-n', cert_nickname, '-t', 'CT,c,c'],
         input=cert_txt.encode())
    _run(certutil_cmd +
         ['-L', '-n', cert_nickname])


@register_browser
def _register_firefox(**kwargs):
    profile = kwargs.get('profile', 'default')
    log.debug("Register Pebble in Firefox with profile %s", profile)
    log.error("Not implemented")
    pass


@click.command()
@click.option('-d', '--debug/--no-debug', help="Debug logging",
              default=False, show_default=True)
@click.option('-t', '--target',
              type=click.Choice(['firefox', 'chrome']),
              default='chrome', show_default=True)
@click.option('-p', '--profile', metavar="PROFILE",
              default="default", show_default=True)
@click.option('-c', '--cert-path', metavar="CERTIFICATE_PATH")
@click.pass_context
def main(ctx, debug, target, profile, cert_path):
    if debug:
        log.setLevel(logging.DEBUG)
        log.debug("Activating DEBUG logging")

    browser_fn = browsers_functions.get("_register_{}".format(target))
    if browser_fn:
        browser_fn(profile=profile, cert_path=cert_path)
    else:
        log.error('Browser %s is not supported', target)


if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter
