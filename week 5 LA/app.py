# import required things here
from flask import Flask, render_template, request , redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.sqlite3"
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()

# create the database here [many-to-many relationship]

class Student(db.Model):
    __tablename__ = "student"
    student_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    roll_number = db.Column(db.String, unique = True , nullable = False)
    first_name = db.Column(db.String, nullable = False)
    last_name = db.Column(db.String)
    # Define relationship to Course through Enrollments
    courses = db.relationship('Course', secondary='enrollments', backref='students')

class Course(db.Model):
    __tablename__ = "course"
    course_id = db.Column(db.Integer, primary_key = True , autoincrement = True)
    course_code = db.Column(db.String, unique = True , nullable = False)
    course_name = db.Column(db.String,nullable = False)
    course_description = db.Column(db.String)

class Enrollments(db.Model):
    __tablename__ = "enrollments"
    enrollment_id = db.Column(db.Integer, primary_key = True , autoincrement = True)
    estudent_id = db.Column(db.Integer, db.ForeignKey("student.student_id"), nullable = False)
    ecourse_id = db.Column(db.Integer, db.ForeignKey("course.course_id"), nullable = False)

@app.route('/')
def index():
    if request.method == 'GET':
        students = Student.query.all()
        if len(students) == 0:
            return render_template('nostudent.html')
        return render_template('index.html' , students = students)

@app.route('/student/create', methods = ['GET', 'POST'])
def addstudent():
    if request.method == 'GET':
        return render_template('addstudent.html')
    else:
        temp = Student.query.filter_by(roll_number = request.form['roll']).first()
        if temp is None:
            stu = Student(roll_number = request.form['roll'],first_name = request.form['f_name'],last_name = request.form['l_name'])
            courses_taken = request.form.getlist('courses')
            for c in courses_taken:
                if c == 'course_1':
                    stu.courses.append(Course.query.filter_by(course_id = 1).first())
                elif c == 'course_2':
                    stu.courses.append(Course.query.filter_by(course_id = 2).first())
                elif c == 'course_3':
                    stu.courses.append(Course.query.filter_by(course_id = 3).first())
                elif c == 'course_4':
                    stu.courses.append(Course.query.filter_by(course_id = 4).first())
            db.session.add(stu)
            db.session.commit()
            return redirect("/")
        else:
            return render_template('rollexists.html')

@app.route("/student/<int:s_id>/update", methods = ["GET","POST"])
def update(s_id):
    if request.method == 'GET':
        student  = Student.query.filter_by(student_id = s_id).one() # one() is used to fetch only one record and if multiple records are there, will throw an error
        return render_template('update.html',student = student)
    else:
        temp = Enrollments.query.filter_by(estudent_id = s_id).first()  # first() is used to fetch only one record
        if temp is not None:
            enrolls = Enrollments.query.filter_by(estudent_id = s_id).all() # nedd all records to delete
            for enroll in enrolls:
                db.session.delete(enroll)
        student_update = Student.query.filter_by(student_id = s_id).one()
        student_update.first_name = request.form["f_name"]
        student_update.last_name = request.form["l_name"]
        courses_taken = request.form.getlist('courses')
        for c in courses_taken:
            if c == 'course_1':
                student_update.courses.append(Course.query.filter_by(course_id = 1).one())
            elif c == 'course_2':
                student_update.courses.append(Course.query.filter_by(course_id = 2).one())
            elif c == 'course_3':
                student_update.courses.append(Course.query.filter_by(course_id = 3).one())
            elif c == 'course_4':
                student_update.courses.append(Course.query.filter_by(course_id = 4).one())
        db.session.commit()
        return redirect("/")

@app.route("/student/<int:s_id>/delete" , methods = ["GET", "POST"])
def delete(s_id):
    temp = Enrollments.query.filter_by(estudent_id = s_id).first()
    if temp  is not None:
        enrolls = Enrollments.query.filter_by(estudent_id = s_id).all()
        for enroll in enrolls:
            db.session.delete(enroll)
    stud = Student.query.filter_by(student_id = s_id).one()
    db.session.delete(stud)
    db.session.commit()
    return redirect("/")

@app.route("/student/<int:s_id>")
def show(s_id):
    student = Student.query.filter_by(student_id = s_id).one()
    return render_template("show.html",student = student)


if __name__ == '__main__' :
    app.run(debug = True, port = 8000)   