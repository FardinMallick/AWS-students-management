from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# =========================
# DATABASE OBJECT
# =========================

db = SQLAlchemy()


# =========================
# CREATE FLASK APP
# =========================

def create_app():

    app = Flask(__name__)

    # =========================
    # SECRET KEY
    # =========================

    app.secret_key = "fardin_secret_key"

    # =========================
    # UPLOAD FOLDER
    # =========================

    app.config[
        "UPLOAD_FOLDER"
    ] = "app/static/uploads"

    # =========================
    # SQLITE DATABASE
    # =========================

    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "sqlite:///database.db"

    app.config[
        "SQLALCHEMY_TRACK_MODIFICATIONS"
    ] = False

    # =========================
    # INITIALIZE DATABASE
    # =========================

    db.init_app(app)

    # =========================
    # IMPORT ROUTES
    # =========================

    from app.routes.main_routes import main

    # =========================
    # REGISTER BLUEPRINT
    # =========================

    app.register_blueprint(main)

    # =========================
    # CREATE DATABASE TABLES
    # =========================

    with app.app_context():

        db.create_all()

    return app
