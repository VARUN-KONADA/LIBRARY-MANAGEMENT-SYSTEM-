from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

def parse_pin(pin_number):
    parts = pin_number.split('-')
    if len(parts) != 3:
        raise ValueError("Invalid pin format. Expected format: YYCollegeCode-Branch-Pin")

    year_prefix = parts[0][:2]
    year = int('20' + year_prefix)  # Convert '23' → 2023
    college_code = parts[0][2:]     # e.g., '596'
    branch = parts[1].upper()       # e.g., 'CM'

    return year, college_code, branch
    
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pin_number = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    branch = db.Column(db.String(10), nullable=False)
    college_code = db.Column(db.String(10), nullable=False)
    joining_year = db.Column(db.Integer, nullable=False)

"""class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)  # Unique book code
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    total_copies = db.Column(db.Integer, nullable=False)
    available_copies = db.Column(db.Integer, nullable=False)

class IssuedBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    issue_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=True)  # None if not yet returned

    # Relationships (optional but useful)
    student = db.relationship('Student', backref=db.backref('issued_books', lazy=True))
    book = db.relationship('Book', backref=db.backref('issued_books', lazy=True))
"""
# edit the fields as required 
with app.app_context():
    db.create_all()

with app.app_context():
    existing_student = Student.query.filter_by(pin_number="23596-cm-070").first()
    if not existing_student:
        new_student = Student(
            pin_number="23596-cm-070",
            name="John Doe",
            branch="CM",
            college_code="596",
            joining_year=2023
        )
        db.session.add(new_student)
        db.session.commit()
        print("New student added.")
    else:
        print("Student already exists, skipping insert.")

with app.app_context():
    students = Student.query.all()
    for student in students:
        print(student.name, student.pin_number)