from flask import Flask, render_template, request, redirect, url_for, send_file
from db import db  # Import db from db.py
from models import Course, Enrollment
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os

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

@app.route('/enroll', methods=['POST'])
def enroll():
    name = request.form.get('name')
    email = request.form.get('email')
    course_id = request.form.get('course_id')
    
    enrollment = Enrollment(name=name, email=email, course_id=course_id)
    db.session.add(enrollment)
    db.session.commit()
    return redirect(url_for('lecture', course_id=course_id))

@app.route('/lecture/<int:course_id>')
def lecture(course_id):
    course = Course.query.get(course_id)
    
    if not course:
        return "Course not found", 404

    return render_template('lecture.html', course=course)

@app.route('/quiz/<int:course_id>')
def quiz(course_id):
    course = Course.query.get(course_id)
    
    if not course:
        return "Course not found", 404

    return render_template('quiz.html', course=course)

@app.route('/certificate/<int:course_id>')
@app.route('/certificate/<int:course_id>')
def certificate(course_id):
    course = Course.query.get_or_404(course_id)

    # Construct the absolute path for the certificate template
    certificate_template = os.path.join(app.root_path, 'static', 'certificate_template.png')
    print(f"Certificate template path: {certificate_template}")  # Add this line
    font_path = os.path.join(app.root_path, 'static', 'fonts', 'arial.ttf')

    # The rest of your existing code...

    font_path = os.path.join(app.root_path, 'static', 'fonts', 'arial.ttf')

    try:
        with Image.open(certificate_template) as img:
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype(font_path, 40)  # Adjust size as needed

            # Define text and draw positions
            text_color = (0, 0, 0)  # Black color for text
            text_position = (250, 200)  # Position for "Congratulations!"
            course_position = (250, 300)  # Position for course title

            draw.text(text_position, "Congratulations!", fill=text_color, font=font)
            draw.text(course_position, f"You have completed {course.title}", fill=text_color, font=font)

            img_io = BytesIO()
            img.save(img_io, 'PNG')
            img_io.seek(0)

        return send_file(img_io, mimetype='image/png', as_attachment=True, download_name="certificate.png")

    except IOError as e:
        return f"An error occurred when processing the certificate: {e}", 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)
