## Import libraies
import sqlite3
import pandas as pd
from sqlalchemy import create_engine, select, Table, MetaData
from api import db, app, Departments, Jobs, HiredEmployees

## Connect to database
engine=create_engine('sqlite:///FLASK-API/instance/database.db')

## Variables declaration
tablenames=['jobs_table', 'departments_table', 'hired_employees_table']

## Load df to db function
def load_data(df, index, file_name):
    try:    
        if index == 0:
            name=Jobs.__table__.columns.keys()
            df.columns=name
            df.to_sql(con=engine, name=Jobs.__tablename__, if_exists='append', index=False)
        elif index == 1:
            name=Departments.__table__.columns.keys()
            df.columns=name
            df.to_sql(con=engine, name=Departments.__tablename__, if_exists='append', index=False)
        elif index == 2:
            name=HiredEmployees.__table__.columns.keys()
            df.columns=name
            df.to_sql(con=engine, name=HiredEmployees.__tablename__, if_exists='append', index=False)
    except Exception as fnf_error:
        print(fnf_error)
        print(f"Explanation: We cannot load the '{file_name}.csv' in the database")
    
def read_file(file_name): 
    with open(file_name) as file:
        df = pd.read_csv(file, sep=",", header=None)
        if(df.empty): 
            print ('CSV file is empty') 
        else: 
            print ('CSV file is not empty') 
        print(df.head())
    return df

## Read csv files function
def csv_files(tablenames):
    for index, file in enumerate(tablenames):
        file_name=f"{file}.csv"
        print(file_name)
        try:
            df=read_file(file_name)
            load_data(df, index, file_name)  
        except FileNotFoundError as fnf_error:
            print(fnf_error)
            print(f"Explanation: We cannot find the '{file_name}.csv' file")

csv_files(tablenames)


