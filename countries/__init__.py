from instance.config import DATABASE, SECRET_KEY
import os

from flask import Flask

from . import blog
from . import db

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate




def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.logger.debug('app.instance_path = %s', app.instance_path)
    #app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    db.init_app(app)
    #db = SQLAlchemy()
    #migrate = Migrate(app, db)
    
    

    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')
    app.add_url_rule('/user/add', endpoint='add_user')
    app.add_url_rule('/add-post', endpoint='add_post')


    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/hello")
    def hello():
        return "Hello, World!"




    # register the database commands
   # from countries import db

    #db.init_app(app)

    # apply the blueprints to the app
   # from countries import auth, info

    #app.register_blueprint(auth.bp)
    #app.register_blueprint(info.bp)

    app.add_url_rule("/", endpoint="hello")
   

    return app
