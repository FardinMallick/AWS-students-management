import os

from app import create_app
from app import db

from app.models.student import Student


# =========================
# CREATE FLASK APP
# =========================

app = create_app()


# =========================
# CREATE DATABASE TABLES
# =========================

with app.app_context():

    db.create_all()


# =========================
# RUN APPLICATION
# =========================

if __name__ == "__main__":

    port = int(

        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(

        host="0.0.0.0",

        port=port,

        debug=True
    )
