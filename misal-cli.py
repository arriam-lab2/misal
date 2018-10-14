#! /usr/bin/env python

import logging
import click
from aiorun import run

from misal.core import Database, parse
from misal.client import Client
from misal.server import Server
from misal.core.users import UserDatabase


# TODO make --port optional in the start command
# TODO try the closest free port instead of throwing an error when an occupied --port is provided start
# TODO add the option to detect a database by name instead of port in the call command
# TODO automatically search for a config by name instead of demanding a config path in the start command
# TODO add password support in the start command

ADDRESS = 'ADDRESS'
PORT = 'PORT'
SSL_CERTFILE = 'SSL_CERTFILE'
SSL_KEYFILE = 'SSL_KEYFILE'
NAME = 'NAME'

logging.basicConfig(format='%(asctime)s %(message)s')


@click.group('cli', context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-a', '--address', required=False, default='localhost', type=str)
@click.option('-p', '--port', required=True, type=int)
@click.option('-sc', '--ssl_certfile', required=False,
              type=click.Path(exists=True, dir_okay=False, resolve_path=True),
              help='An SSL certificate file to authenticate the server,'
              '.pem or .crt formatted.')
@click.option('-sk', '--ssl_keyfile', required=False,
              type=click.Path(exists=True, dir_okay=False, resolve_path=True),
              help='An SSL private key file. Not required for .pem '
              'formatted certificate files')
@click.option('-n', '--name', type=str, required=True)
@click.pass_context
def cli(ctx, address: str, port: int, ssl_certfile: str, 
        ssl_keyfile: str, name: str):
    ctx.obj[ADDRESS] = address
    ctx.obj[PORT] = port
    ctx.obj[SSL_CERTFILE] = ssl_certfile
    ctx.obj[SSL_KEYFILE] = ssl_keyfile
    ctx.obj[NAME] = name


@cli.command('start')
@click.option('-c', '--config', required=True,
              type=click.Path(exists=True, dir_okay=False, resolve_path=True))
@click.pass_context
def start(ctx, config: str):
    with open(config) as lines:
        database = Database(ctx.obj[NAME], *parse(lines))

    user_db = UserDatabase(ctx.obj[NAME])

    # start a logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    server = Server(database, user_db, ctx.obj[PORT], user_db.root, logger,
                    certfile=ctx.obj[SSL_CERTFILE], keyfile=ctx.obj[SSL_KEYFILE])
    run(server.run())


@cli.command('call')
@click.option('-u', '--user', prompt=True,  type=str)
@click.option('--password', prompt=True, hide_input=True, type=str)
@click.argument('message', nargs=-1, type=str)
@click.pass_context
def call(ctx, user, password, message):
    client = Client(ctx.obj[ADDRESS], ctx.obj[PORT], user, password, message,
                    certfile=ctx.obj[SSL_CERTFILE])
    run(client.run())


if __name__ == '__main__':
    cli(obj={})