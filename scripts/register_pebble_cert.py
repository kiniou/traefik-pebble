#!/usr/bin/env python
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
pebble_cert_nickname = "localhost-pebble"
browsers_functions = {}


def register_browser(fn):
    browsers_functions[fn.__name__] = fn
    return fn


def _get_intermediate_certificate():
    log.debug("fetch intermediate certificate from Pebble")
    response = requests.get("https://localhost:15000/roots/0", verify=False)
    log.debug("request: %s", response.request.url)
    log.debug("response: %s", response)
    log.debug("response data: %s", response.text)
    assert response.status_code == 200,\
        "Could not fetch intermediate certificate from Pebble"
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
    cert_txt = _get_intermediate_certificate()
    log.debug("Register Pebble in Chrome")
    DB_PATH = Path('~/.pki/nssdb').expanduser()
    log.debug("DB_PATH: %s", DB_PATH)
    db_name = 'sql:{}'.format(DB_PATH)
    certutil_cmd = ['/usr/bin/env', 'certutil', '-d', db_name]
    _run(certutil_cmd + ['-D', '-n', pebble_cert_nickname])
    _run(certutil_cmd +
         ['-A', '-n', pebble_cert_nickname, '-t', 'CT,c,c'],
         input=cert_txt.encode())
    _run(certutil_cmd +
         ['-L', '-n', pebble_cert_nickname])


@register_browser
def _register_firefox(**kwargs):
    profile = kwargs.get('profile', 'default')
    log.debug("Register Pebble in Firefox with profile %s", profile)
    log.error("Not implemented")
    pass


@click.command()
@click.option('-d', '--debug/--no-debug', help="Debug logging", default=False, show_default=True)
@click.option('-t', '--target',
              type=click.Choice(['firefox', 'chrome']),
              default='chrome', show_default=True)
@click.option('-p', '--profile', metavar="PROFILE", default="default", show_default=True)
@click.pass_context
def main(ctx, debug, target, profile):
    if debug:
        log.setLevel(logging.DEBUG)
        log.debug("Activating DEBUG logging")

    browser_fn = browsers_functions.get("_register_{}".format(target))
    if browser_fn:
        browser_fn(profile=profile)
    else:
        log.error('Browser %s is not supported', target)


if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter
