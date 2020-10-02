""" Flask Application Factory """
from flask import Flask
from app.blueprints import sample_bp


def create_app(environment: str = None) -> Flask:
    """
    Creates the application factory and returns an instance to be used by a server like gunicorn or flask's default
    :param environment: Application deployment environment.
        - Production
        - Testing
        - Deployment (Default)
    :return: Flask instance
    """
    app = Flask(__name__, instance_relative_config=True)

    app.config['CORS_HEADER'] = 'Content-Type'

    # overrides environment, if provided, otherwise tries to use FLASK_ENV
    if environment:
        app.config['ENV'] = environment

    # Load configuration based on export FLASK_ENV = ' '
    if app.config['ENV'] == 'production':
        app.config.from_object('app.config.ProductionConfig')
    elif app.config['ENV'] == 'testing':
        app.config.from_object('app.config.TestingConfig')
    else:
        app.config.from_object('app.config.DevelopmentConfig')

    # Register blueprints
    app.register_blueprint(sample_bp.routes.bp, url_prefix='/')

    return app
