## Import libraies
from sqlalchemy import create_engine, func, extract, case
from sqlalchemy.orm import sessionmaker
from api import db, app, Departments, Jobs, HiredEmployees
from flask import jsonify

## Connect to database
engine = create_engine('sqlite:///FLASK-API/instance/database.db')
Session = sessionmaker(bind=engine)
session = Session()


## Set cases 
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

## Create function for query 1: Number of employees hired for each job 
## and department in 2021 divided by quarter. The
## table must be ordered alphabetically by department and job.
def hired_employees_2021():
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
    print(results)
    # Users.set_results(results)
    data = [
            {
                'department': result.department,
                'job': result.job,
                'Q1': result.Q1,
                'Q2': result.Q2,
                'Q3': result.Q3,
                'Q4': result.Q4
            }
            for result in results
        ]
    print(data)
    
    return data


## Create function for query 2: List of ids, name and number of employees hired of each 
## department that hired more employees than the mean of employees hired in 2021 for all 
## the departments, ordered by the number of employees hired (descending).
def departments_above_mean():
    # Step 1: Calculate the total number of employees hired per department in 2021
    total_hired_per_department = session.query(
        HiredEmployees.department_id,
        func.count(HiredEmployees.id).label('hired')
    ).filter(extract('year', HiredEmployees.datetime) == 2021
    ).group_by(HiredEmployees.department_id).subquery()

    # Step 2: Calculate the mean number of employees hired in 2021
    mean_hired = session.query(
        func.avg(total_hired_per_department.columns.hired)
    ).scalar()
    print(f'2021 avg is {mean_hired}')
    # Step 3: Filter departments that hired more than the mean
    query = session.query(
        Departments.id,
        Departments.department,
        total_hired_per_department.columns.hired
    ).join(total_hired_per_department, Departments.id == total_hired_per_department.columns.department_id
    ).filter(total_hired_per_department.columns.hired > mean_hired
    ).order_by(total_hired_per_department.columns.hired.desc())
    
    # total_hired_per_department.

    results = query.all()
    print(results)
    # data = [
    #     {
    #         'id': result.id,
    #         'department': result.department,
    #         'hired': result.hired
    #     }
    #     for result in results
    # ]
    # return jsonify(data)
    
hired_employees_2021()
# departments_above_mean()



