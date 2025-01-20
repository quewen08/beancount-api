import click
from flask import Flask
from bapp.api.core import api
from bapp.api.query import ns as query_ns
# from bapp.api.repo import ns as repo_ns
from bapp.api.price import ns as price_ns
from bapp.api.transaction import ns as transaction_ns
from bapp.core.storage import storage
from bapp import __version__


@click.command()
@click.option('--port', '-p', default=5000, help='Port to listen on (default: 5000)')
@click.option('-H', '--host', default='localhost', help='Host to bind to (default: localhost)')
@click.option('-d', '--debug', is_flag=True, help='Enable debug mode')
@click.option('--repo/--no-repo', default=False, help='Enable or disable repo namespace')
@click.argument('basedir', type=click.Path(exists=True, resolve_path=True), required=True)
@click.argument('filename', type=click.Path(resolve_path=False), required=True)
@click.version_option(__version__(), prog_name='beancount API')
def main(basedir, filename, port, host, debug, repo):
    try:
        storage.load(basedir, filename)
    except Exception as e:
        click.echo(f"Error loading storage: {e}", err=True)
        return

    app = Flask(__name__)

    api.add_namespace(query_ns)
    # if repo:
    #   api.add_namespace(repo)
    api.add_namespace(price_ns)

    api.init_app(app)

    try:
        app.run(host=host, port=port, debug=debug)
    except Exception as e:
        click.echo(f"Error starting the server: {e}", err=True)


if __name__ == '__main__':
    main()
