from app import db


class Student(db.Model):

    __tablename__ = "students"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    student_id = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    first_name = db.Column(
        db.String(50),
        nullable=False
    )

    last_name = db.Column(
        db.String(50),
        nullable=False
    )

    gender = db.Column(
        db.String(10)
    )

    email = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    phone = db.Column(
        db.String(15)
    )

    course = db.Column(
        db.String(100)
    )

    department = db.Column(
        db.String(100)
    )

    year_of_study = db.Column(
        db.String(20)
    )

    admission_date = db.Column(
        db.Date
    )

    is_deleted = db.Column(
        db.Boolean,
        default=False
    )