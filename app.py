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
    
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    
class BorrowTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    book_code = db.Column(db.String(20), nullable=False)  # Specific physical book code, like B001, B002
    borrow_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime)

    student = db.relationship('Student', backref='borrowed_books')
    book = db.relationship('Book', backref='borrowed_by')

    # Relationships (optional but useful)
    student = db.relationship('Student', backref=db.backref('issued_books', lazy=True))
    book = db.relationship('Book', backref=db.backref('issued_books', lazy=True))

# edit the fields as required 
with app.app_context():
    db.create_all()

with app.app_context():
        pin_number = "23596-cm-080"
        name = "John Doe"

        # Auto-extract details
        joining_year, college_code, branch = parse_pin(pin_number)

        # Create student object
        new_student = Student(
            pin_number=pin_number,
            name=name,
            branch=branch,
            college_code=college_code,
            joining_year=joining_year
        )
        book = Book(
    title="Software Engineering",
    author="Sommerville",
    total_copies=30)
        
        db.session.add(new_student)
        db.session.commit()
    


with app.app_context():
    students = Student.query.all()
    for student in students:
        print(student.name, student.pin_number)