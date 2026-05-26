from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# Database Object

db = SQLAlchemy()


# Create Flask App

def create_app():

    app = Flask(__name__)

    # Secret Key

    app.secret_key = "fardin_secret_key"

    # MySQL Database Configuration

    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "mysql+pymysql://root:fardin0102@localhost/student_management"

    app.config[
        "SQLALCHEMY_TRACK_MODIFICATIONS"
    ] = False


    # Initialize Database

    db.init_app(app)


    # Import Routes

    from app.routes.main_routes import main


    # Register Blueprint

    app.register_blueprint(main)


    return app

