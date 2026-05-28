from app import db


class Result(db.Model):

    __tablename__ = "results"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id")
    )

    subject = db.Column(
        db.String(100),
        nullable=False
    )

    marks = db.Column(
        db.Integer,
        nullable=False
    )

    grade = db.Column(
        db.String(5)
    )

    exam_type = db.Column(
        db.String(50)
    )