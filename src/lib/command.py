from __future__ import absolute_import

import click
from .common import *
from .indicator import main as indicator_main
from .server import main as server_main


def main():
    """
    Command main function
    """
    cli(obj={})


@click.group(context_settings={'help_option_names': ['-h', '--help']})
@click.version_option(APP_VERSION, '-v', '--version')
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, debug):
    """
    DictHub - Project documentation with dict and sentence.
    """
    ctx.obj['DEBUG'] = debug
    if debug is True:
        logger.setLevel(logging.INFO)


@cli.command()
@click.option('-s', '--start', is_flag=True, default=True, help='start the indicator')
@click.option('-b', '--background', is_flag=True, help='start the indicator in background')
def indicator(start, background):
    """
    Startup indicator
    """
    if background is True:
        indicator_main()
    elif start is True:
        from gi.repository import Gio
        fname = os.path.join(AUTOSTART_DIR, DESKTOP_FILENAME)
        Gio.DesktopAppInfo.new_from_filename(fname).launch_uris(None)


@cli.command()
@click.option('-s', '--start', is_flag=True, default=True, help='start web server')
@click.option('-x', '--stop', is_flag=True, help='stop web server')
@click.option('-r', '--reload', is_flag=True, help='reload web server')
@click.option('-b', '--background', is_flag=True, help='run web server in background')
@click.option('-p', '--port', default=WEB_PORT_DEFAULT, help='run web server in background')
def server(start, stop, reload, background, port):
    """
    Web server start | stop | reload
    """
    cmd = ''
    if background is True:
        server_main(port)
    elif stop is True:
        cmd = 'systemctl stop %s' % SERVICE_FILENAME
    elif reload is True:
        cmd = 'systemctl reload %s' % SERVICE_FILENAME
    elif start is True:
        cmd = 'systemctl start %s' % SERVICE_FILENAME
    shell_exec(cmd)


if __name__ == '__main__':
    main()
