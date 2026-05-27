import os

from datetime import date

from werkzeug.utils import secure_filename

from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session

from app import db

from app.models.student import Student
from app.models.attendance import Attendance


main = Blueprint("main", __name__)


# =========================
# IMAGE UPLOAD CONFIG
# =========================

UPLOAD_FOLDER = "app/static/uploads"

ALLOWED_EXTENSIONS = {

    "png",
    "jpg",
    "jpeg",
    "gif"
}


# =========================
# CHECK FILE EXTENSION
# =========================

def allowed_file(filename):

    return (

        "." in filename

        and

        filename.rsplit(
            ".",
            1
        )[1].lower() in ALLOWED_EXTENSIONS
    )


# =========================
# LOGIN
# =========================

@main.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        if username == "admin" and password == "admin123":

            session["user"] = username

            return redirect(
                url_for("main.dashboard")
            )

    return render_template(
        "login.html"
    )


# =========================
# LOGOUT
# =========================

@main.route("/logout")
def logout():

    session.pop("user", None)

    return redirect(
        url_for("main.login")
    )


# =========================
# DASHBOARD
# =========================

@main.route("/")
def dashboard():

    if "user" not in session:

        return redirect(
            url_for("main.login")
        )

    students_count = Student.query.filter_by(
        is_deleted=False
    ).count()

    male_students = Student.query.filter_by(
        gender="Male",
        is_deleted=False
    ).count()

    female_students = Student.query.filter_by(
        gender="Female",
        is_deleted=False
    ).count()

    departments = db.session.query(
        Student.department
    ).distinct().count()

    recent_students = Student.query.filter_by(
        is_deleted=False
    ).order_by(
        Student.id.desc()
    ).limit(5)

    return render_template(

        "dashboard.html",

        students_count=students_count,

        male_students=male_students,

        female_students=female_students,

        departments=departments,

        recent_students=recent_students
    )


# =========================
# STUDENTS PAGE
# =========================

@main.route(
    "/students",
    methods=["GET", "POST"]
)
def students():

    if "user" not in session:

        return redirect(
            url_for("main.login")
        )

    # =========================
    # ADD STUDENT
    # =========================

    if request.method == "POST":

        image = request.files.get(
            "profile_image"
        )

        filename = ""

        if image and image.filename != "":

            if allowed_file(image.filename):

                filename = secure_filename(
                    image.filename
                )

                image.save(

                    os.path.join(
                        UPLOAD_FOLDER,
                        filename
                    )
                )

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

            admission_date=request.form["admission_date"],

            profile_image=filename
        )

        db.session.add(student)

        db.session.commit()

        return redirect(
            url_for("main.students")
        )

    # =========================
    # SEARCH
    # =========================

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


# =========================
# EDIT STUDENT
# =========================

@main.route(
    "/edit/<int:id>",
    methods=["GET", "POST"]
)
def edit_student(id):

    if "user" not in session:

        return redirect(
            url_for("main.login")
        )

    student = Student.query.get_or_404(id)

    if request.method == "POST":

        student.student_id = request.form["student_id"]

        student.first_name = request.form["first_name"]

        student.last_name = request.form["last_name"]

        student.gender = request.form["gender"]

        student.email = request.form["email"]

        student.phone = request.form["phone"]

        student.course = request.form["course"]

        student.department = request.form["department"]

        student.year_of_study = request.form["year_of_study"]

        student.admission_date = request.form["admission_date"]

        # =========================
        # UPDATE IMAGE
        # =========================

        image = request.files.get(
            "profile_image"
        )

        if image and image.filename != "":

            if allowed_file(image.filename):

                filename = secure_filename(
                    image.filename
                )

                image.save(

                    os.path.join(
                        UPLOAD_FOLDER,
                        filename
                    )
                )

                student.profile_image = filename

        db.session.commit()

        return redirect(

            url_for(
                "main.student_profile",
                id=student.id
            )
        )

    return render_template(

        "edit_student.html",

        student=student
    )


# =========================
# STUDENT PROFILE
# =========================

@main.route("/student/<int:id>")
def student_profile(id):

    if "user" not in session:

        return redirect(
            url_for("main.login")
        )

    student = Student.query.get_or_404(id)

    return render_template(

        "student_profile.html",

        student=student
    )


# =========================
# ATTENDANCE PAGE
# =========================

@main.route("/attendance")
def attendance():

    if "user" not in session:

        return redirect(
            url_for("main.login")
        )

    students = Student.query.filter_by(
        is_deleted=False
    ).all()

    attendance_data = Attendance.query.order_by(
        Attendance.id.desc()
    ).all()

    return render_template(

        "attendance.html",

        students=students,

        attendance_data=attendance_data
    )


# =========================
# MARK ATTENDANCE
# =========================

@main.route(
    "/mark-attendance/<int:id>/<status>"
)
def mark_attendance(id, status):

    if "user" not in session:

        return redirect(
            url_for("main.login")
        )

    attendance = Attendance(

        student_id=id,

        attendance_date=date.today(),

        status=status
    )

    db.session.add(attendance)

    db.session.commit()

    return redirect(
        url_for("main.attendance")
    )


# =========================
# MOVE TO TRASH
# =========================

@main.route(
    "/delete/<int:id>",
    methods=["POST"]
)
def delete_student(id):

    if "user" not in session:

        return redirect(
            url_for("main.login")
        )

    student = Student.query.get_or_404(id)

    student.is_deleted = True

    db.session.commit()

    return redirect(
        url_for("main.students")
    )


# =========================
# TRASH PAGE
# =========================

@main.route("/trash")
def trash():

    if "user" not in session:

        return redirect(
            url_for("main.login")
        )

    students = Student.query.filter_by(
        is_deleted=True
    ).all()

    return render_template(

        "trash.html",

        students=students
    )


# =========================
# RESTORE STUDENT
# =========================

@main.route("/restore/<int:id>")
def restore_student(id):

    if "user" not in session:

        return redirect(
            url_for("main.login")
        )

    student = Student.query.get_or_404(id)

    student.is_deleted = False

    db.session.commit()

    return redirect(
        url_for("main.trash")
    )


# =========================
# PERMANENT DELETE
# =========================

@main.route("/permanent-delete/<int:id>")
def permanent_delete(id):

    if "user" not in session:

        return redirect(
            url_for("main.login")
        )

    student = Student.query.get_or_404(id)

    db.session.delete(student)

    db.session.commit()

    return redirect(
        url_for("main.trash")
    )