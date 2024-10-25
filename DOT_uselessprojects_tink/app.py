from flask import Flask, render_template, request, redirect, url_for
from db import db  # Import db from db.py
from models import Course, Enrollment

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the app
db.init_app(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/courses')
def courses():
    all_courses = Course.query.all()
    return render_template('course.html', courses=all_courses)

# Enroll route which redirects to the lectures page after successful enrollment
@app.route('/enroll', methods=['POST'])
def enroll():
    name = request.form.get('name')
    email = request.form.get('email')
    course_id = request.form.get('course_id')
    
    enrollment = Enrollment(name=name, email=email, course_id=course_id)
    db.session.add(enrollment)
    db.session.commit()
    
    # Redirect to the lecture page after enrollment
    return redirect(url_for('lecture', course_id=course_id))

# Lecture page to show content after enrolling
@app.route('/lecture/<int:course_id>')
def lecture(course_id):
    course = Course.query.get(course_id)
    
    if not course:
        return "Course not found", 404

    return render_template('lecture.html', course=course)

# Quiz route (for later implementation)
@app.route('/quiz/<int:course_id>')
def quiz(course_id):
    course = Course.query.get(course_id)
    
    if not course:
        return "Course not found", 404

    return render_template('quiz.html', course=course)

# Route for generating a certificate (to be linked after quiz)
@app.route('/certificate/<int:course_id>')
def certificate(course_id):
    course = Course.query.get(course_id)
    
    if not course:
        return "Course not found", 404

    return render_template('certificate.html', course=course)

if __name__ == '__main__':
    app.run(debug=True)
