## Import libraies
import sqlite3
import re
import pandas as pd
from sqlalchemy import create_engine, select, Table, MetaData
from api import db, app, Departments, Jobs, HiredEmployees

## Connect to database
engine=create_engine('sqlite:///FLASK-API/instance/database.db')

## Variables declaration
tablenames=['jobs_table', 'departments_table', 'hired_employees_table']

# Data Dictionary
jobs_dict = {
    "id": {"type": "int", "required": True, "unique": True},
    "job": {"type": "string", "required": True}
}

depts_dict = {
    "id": {"type": "int", "required": True, "unique": True},
    "department": {"type": "string", "required": True}
}

empls_dict = {
    "id": {"type": "int", "required": True, "unique": True},
    "name": {"type": "string", "required": True},
    "datetime": {"type": "string", "required": True, "format": "iso8601"},
    "job_id": {"type": "string", "required": True, "foreign_key": "jobs.id"},
    "department_id": {"type": "string", "required": True, "foreign_key": "departments.id"}
}

iso8601_regex = re.compile(
    r'(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})Z'
)

## Validation and cleaning data from df
def validate_and_clean_data(df, data_dict):
    for col, rules in data_dict.items():
        # Drop rows if a required column is missing
        if rules["required"] and col not in df.columns:
            df[col] = None  # Fill with None to apply validation later

        # # Validate the data type of each column
        # if col in df.columns:
        #     if rules["type"] == "string" and not pd.api.types.is_string_dtype(df[col]):
        #         df = df.drop(df[~df[col].apply(lambda x: isinstance(x, str))].index)
        #     if rules["type"] == "int" and not pd.api.types.is_integer_dtype(df[col]):
        #         df = df.drop(df[~df[col].apply(lambda x: isinstance(x, int))].index)

        #     # Check for ISO 8601 format if specified
        #     if "format" in rules and rules["format"] == "iso8601":
        #         df = df.drop(df[~df[col].apply(lambda x: iso8601_regex.match(x) is not None)].index)

            # # Check for valid foreign key reference
            # if "foreign_key" in rules:
            #     foreign_table, foreign_column = rules["foreign_key"].split('.')
            #     foreign_ids = db.session.query(getattr(eval(foreign_table.capitalize()), foreign_column)).all()
            #     foreign_ids = [id[0] for id in foreign_ids]
            #     df = df.drop(df[~df[col].isin(foreign_ids)].index)
            
            # # Check for valid foreign key reference
            # if "foreign_key" in rules:
            #     foreign_table, foreign_column = rules["foreign_key"].split('.')
            #     foreign_ids = db.session.query(getattr(eval(foreign_table.capitalize()), foreign_column)).all()
            #     foreign_ids = [id[0] for id in foreign_ids]
            #     df = df.drop(df[~df[col].isin(foreign_ids)].index)
    nan_values_count = df.isnull().sum()
    print(f'It will be drop: {nan_values_count} rows that contain NaN values')
    # Drop rows with any remaining None values (indicating missing required columns)
    df = df.dropna()
    return df

## Load df to db function
def load_data(df, index, file_name):
    try:    
        if index == 0:
            name=Jobs.__table__.columns.keys()
            df.columns=name
            print(df.shape[0])
            df = validate_and_clean_data(df, jobs_dict)
            print(df.shape[0])
            df.to_sql(con=engine, name=Jobs.__tablename__, if_exists='append', index=False)
        elif index == 1:
            name=Departments.__table__.columns.keys()
            df.columns=name
            print(df.shape[0])
            df = validate_and_clean_data(df, depts_dict)
            print(df.shape[0])
            df.to_sql(con=engine, name=Departments.__tablename__, if_exists='append', index=False)
        elif index == 2:
            name=HiredEmployees.__table__.columns.keys()
            df.columns=name
            print(df.shape[0])
            df = validate_and_clean_data(df, empls_dict)
            print(df.shape[0])
            df.to_sql(con=engine, name=HiredEmployees.__tablename__, if_exists='append', index=False)
    except Exception as fnf_error:
        print(fnf_error)
        print(f"Explanation: We cannot load the '{file_name}' in the database")

## Read and check empty file
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

if __name__ == "__main__":
    csv_files(tablenames)


