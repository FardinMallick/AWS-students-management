from app import db


class Course(db.Model):

    __tablename__ = "courses"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    course_name = db.Column(
        db.String(100),
        nullable=False
    )

    course_code = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    duration = db.Column(
        db.String(50)
    )

    department = db.Column(
        db.String(100)
    )

    instructor = db.Column(
        db.String(100)
    )