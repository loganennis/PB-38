import os

from flask import Flask
from . import serve

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    # default configuration
    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    if test_config is None:
        # overrides default configuration if config.py exists
        app.config.from_pyfile('config.py', silent=True)
    else:
        # test_config can be passed and used instead of instance config
        app.config.from_mapping(test_config)

    # if we need app.instance_path
    # try:
    #     os.makedirs(app.instance_path)
    # except OSError:
    #     pass

    serve.init_app(app)
    
    app.register_blueprint(serve.bp)

    return app