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
from app.models.result import Result
from app.models.course import Course


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

            admission_date=date.fromisoformat(
                request.form["admission_date"]
            ),

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


# =========================
# STUDENT ID CARD
# =========================

@main.route("/id-card/<int:id>")
def id_card(id):

    if "user" not in session:

        return redirect(
            url_for("main.login")
        )

    student = Student.query.get_or_404(id)

    return render_template(

        "id_card.html",

        student=student
    )


# =========================
# RESULTS PAGE
# =========================

@main.route(
    "/results",
    methods=["GET", "POST"]
)
def results():

    if "user" not in session:

        return redirect(
            url_for("main.login")
        )

    # =========================
    # ADD RESULT
    # =========================

    if request.method == "POST":

        marks = int(
            request.form["marks"]
        )

        # =========================
        # GRADE SYSTEM
        # =========================

        if marks >= 90:

            grade = "A+"

        elif marks >= 80:

            grade = "A"

        elif marks >= 70:

            grade = "B"

        elif marks >= 60:

            grade = "C"

        elif marks >= 50:

            grade = "D"

        else:

            grade = "F"

        result = Result(

            student_id=request.form["student_id"],

            subject=request.form["subject"],

            marks=marks,

            grade=grade,

            exam_type=request.form["exam_type"]
        )

        db.session.add(result)

        db.session.commit()

        return redirect(
            url_for("main.results")
        )

    # =========================
    # FETCH DATA
    # =========================

    results = Result.query.all()

    students = Student.query.filter_by(
        is_deleted=False
    ).all()

    return render_template(

        "results.html",

        results=results,

        students=students
    )


# =========================
# REPORT CARD
# =========================

@main.route("/report-card/<int:id>")
def report_card(id):

    if "user" not in session:

        return redirect(
            url_for("main.login")
        )

    # =========================
    # GET STUDENT
    # =========================

    student = Student.query.get_or_404(id)

    # =========================
    # GET RESULTS
    # =========================

    results = Result.query.filter_by(
        student_id=id
    ).all()

    # =========================
    # TOTAL MARKS
    # =========================

    total_marks = sum(

        result.marks

        for result in results
    )

    # =========================
    # TOTAL SUBJECTS
    # =========================

    total_subjects = len(results)

    # =========================
    # PERCENTAGE
    # =========================

    if total_subjects > 0:

        percentage = round(

            total_marks / total_subjects,

            2
        )

    else:

        percentage = 0

    # =========================
    # FINAL GRADE
    # =========================

    if percentage >= 90:

        final_grade = "A+"

    elif percentage >= 80:

        final_grade = "A"

    elif percentage >= 70:

        final_grade = "B"

    elif percentage >= 60:

        final_grade = "C"

    elif percentage >= 50:

        final_grade = "D"

    else:

        final_grade = "F"

    return render_template(

        "report_card.html",

        student=student,

        results=results,

        total_marks=total_marks,

        percentage=percentage,

        final_grade=final_grade
    )
# =========================
# ANALYTICS PAGE
# =========================

@main.route("/analytics")
def analytics():

    if "user" not in session:

        return redirect(
            url_for("main.login")
        )

    # Total Students

    total_students = Student.query.filter_by(
        is_deleted=False
    ).count()

    # Male Students

    male_students = Student.query.filter_by(
        gender="Male",
        is_deleted=False
    ).count()

    # Female Students

    female_students = Student.query.filter_by(
        gender="Female",
        is_deleted=False
    ).count()

    # Departments

    departments = db.session.query(
        Student.department
    ).distinct().count()

    # Total Results

    total_results = Result.query.count()

    return render_template(

        "analytics.html",

        total_students=total_students,

        male_students=male_students,

        female_students=female_students,

        departments=departments,

        total_results=total_results
    )

# =========================
# COURSES PAGE
# =========================

@main.route(
    "/courses",
    methods=["GET", "POST"]
)
def courses():

    if "user" not in session:

        return redirect(
            url_for("main.login")
        )

    if request.method == "POST":

        course = Course(

            course_name=request.form["course_name"],

            course_code=request.form["course_code"],

            duration=request.form["duration"],

            department=request.form["department"],

            instructor=request.form["instructor"]
        )

        db.session.add(course)

        db.session.commit()

        return redirect(
            url_for("main.courses")
        )

    courses = Course.query.all()

    return render_template(

        "courses.html",

        courses=courses
    )