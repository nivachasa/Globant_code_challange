##Import libraies
from flask import Flask
from flask_sqlalchemy from flask_sqlalchemy

## Cretae app Flask
app=Flask(__name__)

## DB location
app.config['SQL_DATABASE']= 'sqlite:///database.db'
db = SQLAklchemy(app)

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
    department_id=db.Column(db.String(20), db.ForeignKey(departments.id), nullable=False)
    job_id=db.Column(db.String(20), db.ForeignKey(jobs.id), nullable=False)

    def __repr__(self):
        return f"{self.id}, {self.name}"

## Main function 
@app.route('/')
def home():
        return '<h1>Code Challange</h1>'

##  Run app
if __name__=='__main__':
    app.run(debug=True)



