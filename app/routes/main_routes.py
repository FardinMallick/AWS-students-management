from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

from app import db
from app.models.student import Student


main = Blueprint("main", __name__)


# Dashboard

@main.route("/")
def dashboard():

    students_count = Student.query.filter_by(
        is_deleted=False
    ).count()

    recent_students = Student.query.filter_by(
        is_deleted=False
    ).order_by(
        Student.id.desc()
    ).limit(5)

    return render_template(
        "dashboard.html",
        students_count=students_count,
        recent_students=recent_students
    )


# Students Page

@main.route("/students", methods=["GET", "POST"])
def students():

    if request.method == "POST":

        student = Student(

            student_id=request.form["student_id"],

            first_name=request.form["first_name"],

            last_name=request.form["last_name"],

            gender=request.form["gender"],

            email=request.form["email"],

            phone=request.form["phone"],

            course=request.form["course"],

            department=request.form["department"],

            year_of_study=request.form["year_of_study"],

            admission_date=request.form["admission_date"]

        )

        db.session.add(student)

        db.session.commit()

        return redirect(
            url_for("main.students")
        )

    search = request.args.get("search")

    if search:

        students = Student.query.filter(

            Student.first_name.contains(search),

            Student.is_deleted == False

        ).all()

    else:

        students = Student.query.filter_by(
            is_deleted=False
        ).all()

    return render_template(
        "students.html",
        students=students
    )


# Move To Trash

@main.route("/delete/<int:id>", methods=["POST"])
def delete_student(id):

    student = Student.query.get_or_404(id)

    student.is_deleted = True

    db.session.commit()

    return redirect(
        url_for("main.students")
    )


# Trash Page

@main.route("/trash")
def trash():

    students = Student.query.filter_by(
        is_deleted=True
    ).all()

    return render_template(
        "trash.html",
        students=students
    )


# Restore Student

@main.route("/restore/<int:id>")
def restore_student(id):

    student = Student.query.get_or_404(id)

    student.is_deleted = False

    db.session.commit()

    return redirect(
        url_for("main.trash")
    )


# Permanent Delete

@main.route("/permanent-delete/<int:id>")
def permanent_delete(id):

    student = Student.query.get_or_404(id)

    db.session.delete(student)

    db.session.commit()

    return redirect(
        url_for("main.trash")
    )