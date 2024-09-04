##Import libraies
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, fields, marshal_with

## Cretae app Flask
app=Flask(__name__)

## DB location
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///database.db'
db = SQLAlchemy(app)

## API as API restful
api= Api(app)

## Class Departments table definition
class Departments(db.Model):
    __tablename__ = 'departments'
    id=db.Column(db.Integer, primary_key=True)
    department=db.Column(db.String(80), unique=False, nullable=False)
    department_relationship=db.relationship('HiredEmployees', backref='departments', lazy=True)
    def __repr__(self):
        return f'{self.id}, {self.department}'

## Class Jobs table definition
class Jobs(db.Model):
    __tablename__ = 'jobs'
    id=db.Column(db.Integer, primary_key=True)
    job=db.Column(db.String(80), unique=False, nullable=False)
    job_relationship=db.relationship('HiredEmployees', backref='jobs', lazy=True)
    
    def __repr__(self):
        return f'{self.id}, {self.job}'

## Class HiredEmployees table definition
class HiredEmployees(db.Model):
    __tablename__ = 'hired_employees'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(80), unique=False,nullable=False)
    ## ISO format: year, month, day, hour, minutes, seconds, and milliseconds. Ex:2021-07-27T16:02:08Z
    datetime=db.Column(db.String(80), unique=False, nullable=False)
    department_id=db.Column(db.Integer, db.ForeignKey(Departments.id), nullable=False)
    job_id=db.Column(db.Integer, db.ForeignKey(Jobs.id), nullable=False)

    def __repr__(self):
        return f"{self.id}, {self.name}, {self.datetime} {self.department_id},{self.job_id}"

job_args=reqparse.RequestParser()
# dep_args=reqparse.RequestParser()
h_e_args=reqparse.RequestParser()

# job_args.add_argument('*id', type=int, required=True, help='Job id cannot be empty')
# job_args.add_argument('job', type=str, required=True, help='Job name cannot be empty')
# dep_args.add_argument('*id', type=int, required=True, help='Department id cannot be empty')
# dep_args.add_argument('department', type=str, required=True, help='Department name cannot be empty')

jobsFields ={
    'id':fields.Integer,
    'job':fields.String,
}

# departmentsFields ={
#     'id':fields.Integer,
#     'department':fields.String,
# }

hiredEmployeesFields ={
    'id':fields.Integer,
    'name':fields.String,
    'datetime':fields.String,
    'department_id':fields.Integer,
    'jobs_id':fields.Integer,
}

# Jobs table Backup function
class BackupJobs(Resource):
    @marshal_with(jobsFields)
    def get(self):
        jobs_query = Jobs.query.all()
        return jobs_query

# # Departments table Backup function
# class BackupDepartments(Resource):
#     @marshal_with(departmentsFields)
#     def get(self):
#         departments_query = Departments.query.all()
#         return departments_query

# Hired Employees table Backup function
class BackupHiredEmployees(Resource):
    @marshal_with(hiredEmployeesFields)
    def get(self):
        hired_employees_query = HiredEmployees.query.all()
        return jsonify(hired_employees_query)

api.add_resource(BackupJobs, '/backup/jobs')
# api.add_resource(BackupDepartments, '/backup/departments')
api.add_resource(BackupHiredEmployees, '/backup/hired-employees')

## Main function 
@app.route('/')
def home():
    return render_template("index.html")

## Upload function
@app.route('/upload', methods=['POST']) 
def upload(): 
    if request.method == 'POST': 
        # Get the list of files from webpage 
        files = request.files.getlist("file") 
        table_list=['jobs_table', 'departments_table', 'hired_employees_table']
        # Iterate for each file in the files List, and Save them 
        for index, file in enumerate(files): 
            if (file.filename)!='':
                file.save(table_list[index]+'.csv') 
        return "<h1>Files Uploaded Successfully.!</h1>"

##  Run app
if __name__=='__main__':
    app.run(debug=True)