##Import libraies
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort
import pandas as pd
import fastavro
import os

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
        return f"{self.id}, {self.name}"

job_args=reqparse.RequestParser()
dep_args=reqparse.RequestParser()
h_e_args=reqparse.RequestParser()

job_args.add_argument('*id', type=int, required=True, help='Job id cannot be empty')
job_args.add_argument('job', type=str, required=True, help='Job name cannot be empty')
dep_args.add_argument('*id', type=int, required=True, help='Department id cannot be empty')
dep_args.add_argument('department', type=str, required=True, help='Department name cannot be empty')

## Backup function
# class BackupDB(Resource):
#     def get(self):
#         # Query the database
#         jobs = Jobs.query.all()
#         #departments = Departments.query.all()
#         return jobs#, departments
#         # hired_employees = HiredEmployees.query.all()

#         # # Convert to DataFrames
#         # jobs_df = pd.DataFrame([(j.id, j.job) for j in jobs], columns=['id', 'title'])
#         # departments_df = pd.DataFrame([(d.id, d.department) for d in departments], columns=['id', 'name'])
#         # hired_employees_df = pd.DataFrame([(he.id, he.name, he.datetime, he.job_id, he.department_id) for he in hired_employees], columns=['id', 'name', 'datetime', 'job_id', 'department_id'])

#         # print(jobs_df.head())
#         # print(departments_df.head())
#         # print(hired_employees_df.head())
        
#         # # Define the schema
#         # schema = {
#         #     'doc': 'Database backup',
#         #     'name': 'Database',
#         #     'namespace': 'your.namespace',
#         #     'type': 'record',
#         #     'fields': [
#         #         {'name': 'jobs', 'type': {'type': 'array', 'items': {
#         #             'name': 'Job',
#         #             'type': 'record',
#         #             'fields': [
#         #                 {'name': 'id', 'type': 'int'},
#         #                 {'name': 'title', 'type': 'string'}
#         #             ]
#         #         }}},
#         #         {'name': 'departments', 'type': {'type': 'array', 'items': {
#         #             'name': 'Department',
#         #             'type': 'record',
#         #             'fields': [
#         #                 {'name': 'id', 'type': 'int'},
#         #                 {'name': 'name', 'type': 'string'}
#         #             ]
#         #         }}},
#         #         {'name': 'hired_employees', 'type': {'type': 'array', 'items': {
#         #             'name': 'HiredEmployee',
#         #             'type': 'record',
#         #             'fields': [
#         #                 {'name': 'id', 'type': 'int'},
#         #                 {'name': 'name', 'type': 'string'},
#         #                 {'name': 'datetime', 'type': 'string'},
#         #                 {'name': 'job_id', 'type': 'int'},
#         #                 {'name': 'department_id', 'type': 'int'}
#         #             ]
#         #         }}}
#         #     ]
#         # }

#         # # Combine data into a single dictionary
#         # data = {
#         #     'jobs': jobs_df.to_dict('records'),
#         #     'departments': departments_df.to_dict('records'),
#         #     'hired_employees': hired_employees_df.to_dict('records')
#         # }

#         # # Write to AVRO file
#         # with open('backup.avro', 'wb') as out:
#         #     fastavro.writer(out, schema, [data])
        
#         # return jsonify({"message": "Backup created successfully!"})

# api.add_resource(BackupDB, '/backup')

class JobClass(Resource):
    def get(self):
        jobs= Jobs.query.all()
        return jobs

api.add_resource(JobClass, '/api/users/')

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