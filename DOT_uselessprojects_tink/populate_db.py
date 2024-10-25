from app import app, db  # Import app and db directly from app.py
from models import Course

# Create tables and populate the database
with app.app_context():
    db.create_all()  # Create tables

    # Add sample courses
    courses = [
        Course(title="Mastering Laziness", description="A guide to achieving maximum relaxation and minimum effort."),
        Course(title="Procrastination 101", description="An introductory course on putting things off efficiently."),
        Course(title="The Art of Idling", description="Learn the secrets of effective lounging and slow living."),
        Course(title="The Science of Doing Nothing", description="Explore why sometimes doing nothing is best.")
    ]

    # Add courses to the session and commit
    db.session.bulk_save_objects(courses)
    db.session.commit()
    print("Database has been populated with initial courses!")
