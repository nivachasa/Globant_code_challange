##Import libraies
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, func, extract, case
from sqlalchemy.orm import sessionmaker
from flask_restful import Api
import os
import pandas as pd
import subprocess

## Cretae app Flask
app=Flask(__name__)

## DB location
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:////workspaces/Globant_code_challange/FLASK-API/instance/database.db'
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

@app.route('/backup', methods=['GET'])
## Create function for backup
def backup():
    if request.method == 'GET':   
        ## Execute db_backup python file
        try:
            app.logger.info('Executing db_backup python file')
            subprocess.run(["python","/workspaces/Globant_code_challange/FLASK-API/db_backup.py"], check = True)
            label="<h1>Tables successfully backup.</h1>"
        except Exception as e:
            app.logger.error(e)
            label ="<h1>Something went worng in the backup.</h1>"

        return label

@app.route('/restore-backup', methods=['POST'])
## Create function for restore a specif avro file backup
def restore_backup():
    if request.method == 'POST':
        avro_file=request.form.get('avro_file_list')
        ## Execute db_restore_backup python file
        try:
            app.logger.info('Executing db_restore_backup python file')
            subprocess.run(["python","/workspaces/Globant_code_challange/FLASK-API/db_restore_backup.py", "'" + avro_file + "'"], check = True)
            label="<h1>Restore backup successfully restored.</h1>"
        except Exception as e:
            app.logger.error(e)
            label="<h1>Something went worng with the db restore backup.</h1>"
        return label

## List all avro files
def list_AVRO_files():
    # Set the directory you want to list files from
    directory = '/workspaces/Globant_code_challange/avro_files'
    # Get the list of .avro files in the directory
    try:
        app.logger.info('Opening avro files')
        files = [f for f in os.listdir(directory) if f.endswith('.avro')]
    except Exception as e:
        app.logger.error(e)
    return files
   
## Create style for tables
table_styles = """
<style>

    h2 {
        text-align: center;
        font-family: Helvetica, Arial, sans-serif;
    }
    table { 
        margin-left: auto;
        margin-right: auto;
    }
    table, th, td {
        border: 1px solid black;
        border-collapse: collapse;
    }
    th, td {
        padding: 5px;
        text-align: center;
        font-family: Helvetica, Arial, sans-serif;
        font-size: 90%;
    }
    table tbody tr:hover {
        background-color: #dddddd;
    }
    .wide {
        width: 90%; 
    }

</style>
"""

@app.route('/hired_employees_2021', methods=['GET'])
## Create function for query 1: Number of employees hired for each job 
## and department in 2021 divided by quarter. The
## table must be ordered alphabetically by department and job.
def hired_employees_2021():
    ## Connect to database
    engine = create_engine('sqlite:////workspaces/Globant_code_challange/FLASK-API/instance/database.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    ## Set cases for each quarter
    case_q1= case(
        (extract('month', HiredEmployees.datetime)=='1', 1), 
        (extract('month', HiredEmployees.datetime)=='2', 1), 
        (extract('month', HiredEmployees.datetime)=='3', 1),  
        else_ =0
    )

    case_q2= case(
        (extract('month', HiredEmployees.datetime)=='4', 1), 
        (extract('month', HiredEmployees.datetime)=='5', 1), 
        (extract('month', HiredEmployees.datetime)=='6', 1),  
        else_ =0
    )

    case_q3= case(
        (extract('month', HiredEmployees.datetime)=='7', 1), 
        (extract('month', HiredEmployees.datetime)=='8', 1), 
        (extract('month', HiredEmployees.datetime)=='9', 1),  
        else_ =0
    )

    case_q4= case(
        (extract('month', HiredEmployees.datetime)=='10', 1), 
        (extract('month', HiredEmployees.datetime)=='11', 1), 
        (extract('month', HiredEmployees.datetime)=='12', 1),  
        else_ =0
    )
    
    ## Create query
    query = session.query(
            Departments.department,
            Jobs.job,
            func.sum(case_q1).label('Q1'),
            func.sum(case_q2).label('Q2'),
            func.sum(case_q3).label('Q3'),
            func.sum(case_q4).label('Q4')
        ).join(Jobs, HiredEmployees.job_id == Jobs.id
        ).join(Departments, HiredEmployees.department_id == Departments.id
        ).filter(extract('year', HiredEmployees.datetime) == 2021
        ).group_by(Departments.department, Jobs.job
        ).order_by(Departments.department, Jobs.job)

    results = query.all()
    
    ## Create array structure for hired_employees_2021 query
    data = [
            {
                'DEPARTMENT': result.department,
                'JOB': result.job,
                'Q1': result.Q1,
                'Q2': result.Q2,
                'Q3': result.Q3,
                'Q4': result.Q4
            }
            for result in results
        ]
    df = pd.DataFrame(data)
    return table_styles + df.to_html(header="true", table_id="table")

@app.route('/departments_above_mean', methods=['GET'])
## Create function for query 2: List of ids, name and number of employees hired of each 
## department that hired more employees than the mean of employees hired in 2021 for all 
## the departments, ordered by the number of employees hired (descending).
def departments_above_mean():
    ## Connect to database
    engine = create_engine('sqlite:////workspaces/Globant_code_challange/FLASK-API/instance/database.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    
    ## Calculate the total number of employees hired per department in 2021
    total_hired_per_department = session.query(
        HiredEmployees.department_id,
        func.count(HiredEmployees.id).label('hired')
    ).filter(extract('year', HiredEmployees.datetime) == 2021
    ).group_by(HiredEmployees.department_id).subquery()

    ## Calculate the mean number of employees hired in 2021
    mean_hired = session.query(
        func.avg(total_hired_per_department.columns.hired)
    ).scalar()
    app.logger.info(f'2021 avg is {mean_hired}')
    ## Filter departments that hired more than the mean
    query = session.query(
        Departments.id,
        Departments.department,
        total_hired_per_department.columns.hired
    ).join(total_hired_per_department, Departments.id == total_hired_per_department.columns.department_id
    ).filter(total_hired_per_department.columns.hired > mean_hired
    ).order_by(total_hired_per_department.columns.hired.desc())
    
    results = query.all()
    
    ## Create array structure for departments_above_mean query
    data = [
        {
            'ID': result.id,
            'DEPARTMENT': result.department,
            'HIRED': result.hired
        }
        for result in results
    ]
    df = pd.DataFrame(data)
    return table_styles + df.to_html(header="true", table_id="table")

@app.route('/upload', methods=['POST']) 
## Create ipload function
def upload(): 
    if request.method == 'POST': 
        # Get the list of files from webpage 
        files = request.files.getlist("file") 
        table_list=['jobs_table', 'departments_table', 'hired_employees_table']
        # Iterate for each file in the files List, and Save them 
        try:
            app.logger.info('Saving csv files')
            for index, file in enumerate(files): 
                if (file.filename)!='':
                    file.save('/workspaces/Globant_code_challange/csv_files/'+table_list[index]+'.csv') 
        except Exception as e:
            app.logger.error(e)
        
        ## Execute db_upload python file
        try:
            app.logger.info('Executing db_upload python file')
            subprocess.run(["python","/workspaces/Globant_code_challange/FLASK-API/db_upload.py"], check = True)
            label="<h1>Files uploaded successfully.!</h1>"
        except Exception as e:
            app.logger.error(e)
            label="<h1>Files cannot be uploaded. Please check data rules and be sure all files are into csv_files folder</h1>"

        return label

@app.route('/')
## Create home function 
def home():
    return render_template("index.html", list_restore=list_AVRO_files())

##  Run app
if __name__=='__main__':
    app.run(debug=True)