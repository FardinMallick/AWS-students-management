from app import create_app
from app import db

from app.models.student import Student


# Create Flask App

app = create_app()


# Create Database Tables

with app.app_context():

    db.create_all()


# Run Application

if __name__ == "__main__":

    app.run(
        debug=True
    )

