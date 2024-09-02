##Import libraies
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

## Cretae app Flask
app=Flask(__name__)

## DB location
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///database.db'
db = SQLAlchemy(app)

## Class Departments table definition
class Departments(db.Model):
    __tablename__ = 'departments'
    id=db.Column(db.Integer, primary_key=True)
    department=db.Column(db.String(20), unique=False, nullable=False)
    department_relationship=db.relationship('HiredEmployees', backref='departments', lazy=True)
    def __repr__(self):
        return f'{self.id}, {self.department}'

## Class Jobs table definition
class Jobs(db.Model):
    __tablename__ = 'jobs'
    id=db.Column(db.Integer, primary_key=True)
    job=db.Column(db.String(20), unique=False, nullable=False)
    job_relationship=db.relationship('HiredEmployees', backref='jobs', lazy=True)

    def __repr__(self):
        return f'{self.id}, {self.job}'

## Class HiredEmployees table definition
class HiredEmployees(db.Model):
    __tablename__ = 'hired_employees'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(80), unique=False, nullable=False)
    ## ISO format: year, month, day, hour, minutes, seconds, and milliseconds. Ex:2021-07-27T16:02:08Z
    datetime=db.Column(db.String(20), unique=False, nullable=False)
    department_id=db.Column(db.String(20), db.ForeignKey(Departments.id), nullable=False)
    job_id=db.Column(db.String(20), db.ForeignKey(Jobs.id), nullable=False)

    def __repr__(self):
        return f"{self.id}, {self.name}"

## Main function 
@app.route('/')
def home():
        return render_template("index.html")

@app.route('/upload', methods=['POST']) 
def upload(): 
    if request.method == 'POST': 
  
        # Get the list of files from webpage 
        files = request.files.getlist("file") 
  
        # Iterate for each file in the files List, and Save them 
        for file in files: 
            file.save(file.filename) 
        return "<h1>Files Uploaded Successfully.!</h1>"

##  Run app
if __name__=='__main__':
    app.run(debug=True)



