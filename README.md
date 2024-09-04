# Globant_code_challange Big Data Migration PoC
This project is big data migration to a new database system.

## Project Overview

This project is a Proof of Concept (PoC) for migrating large-scale historical data into a new SQL database system. The PoC addresses the following key requirements:

1. **Data Migration:** Move historical data from CSV files to the new SQL database.
2. **REST API Service:** 
   - Handle incoming data, ensuring it conforms to data dictionary rules.
   - Support batch transactions of up to 1000 rows in a single request.
   - Manage data insertion for multiple tables through a unified API.
   - Enforce specific data rules for each table.
3. **Backup and Restore Features:**
   - Backup data for each table and store it in AVRO format in the file system.
   - Restore data from AVRO backups of each table as needed.
4. **Data Reporting:**
   - Provide a report of the number of employees hired in 2021, segmented by job and department and ordered alphabetically by department and job.
   - List departments that hired more employees than the average across all departments in 2021, ordered by the number of employees hired.

## Getting Started

### Prerequisites

Ensure you have Python installed. The project dependencies are listed in the `requirements.txt` file. To install all required packages, run:

```bash
pip install -r requirements.txt
```

### Database Initialization

Before running the application, you need to initialize the database schema. This is done by executing the `db_creation.py` script, which is intended to be run **only once**. This script creates the necessary tables in the database.

To run the script, use:

```bash
python db_creation.py
```

### Database Structure and Relationships
The database is designed to manage employee hiring data and includes the following tables:

#### hired_employees: Stores information about each employee hired.

**Columns:**
id (INTEGER): The unique ID of the employee.
name (STRING): The name and surname of the employee.
datetime (STRING): The hire date and time in ISO format.
department_id (INTEGER): The ID of the department where the employee was hired.
job_id (INTEGER): The ID of the job the employee was hired for.

#### departments: Stores information about departments.

**Columns:**
id (INTEGER): The unique ID of the department.
department (STRING): The name of the department.

#### jobs: Stores information about job positions.

**Columns:**
id (INTEGER): The unique ID of the job.
job (STRING): The name of the job.

#### Database Relationships:
**hired_employees.department_id → departments.id:**
This relationship links each hired employee to a specific department. The department_id in the hired_employees table references the id in the departments table.

**hired_employees.job_id → jobs.id:**
This relationship links each hired employee to a specific job. The job_id in the hired_employees table references the id in the jobs table.


### Project Structure

- **`csv_files/`**: Contains the historical data files in CSV format.
- **`avro_files/`**: Stores the backup files in AVRO format.
- **`api.py`**: The main Flask application file that defines the REST API endpoints.
- **`db_creation.py`**: Script for creating the initial database schema. Run this script only once.
- **`db_backup.py`**: Script for backing up the database.
- **`db_restore_backup.py`**: Script for restore backing up the database. It recives the input parameter avro file name.
- **`db_upload.py`**: Script for uploading 3 tables: jobs, departments, and hire_employees in this order into the database.


### Running the Application

1. **Start the REST API Service:**
   - Run the Flask application using the command:
     ```bash
     python api.py
     ```
    **Not:** Make sure your virtual enviroment is activated. It run with th command:
    ```bash
     source .venv./bin/activate
     ```

2. **Create the Database:**
   - Run the script `db_creation.py` to create the database. Run this script only once. It will create a database.db file into the folder [text](FLASK-API/instance) 

3. **Data Migration:**
   - Run the script `db_upload.py` to load csv data from `csv_files/` into the new SQL database or use the api feature in the first section called 'Upload CSV Files to load in Database', choose all the 3 files, and then click on the "Uploap" buttom.

4. **Access the API Endpoints:**
   - **`/upload`**: Gives information about the upload status. Do not need to open it. Button "Upload" redirect it to this endpoint.
   - **`/backup`**: Gives information about the upload status. Do not need to open it. Button "Backup Now" redirect it to this endpoint.
   - **`/restore-backup`**: Gives information about the upload status. Do not need to open it. Button "Restore backup" redirect it to this endpoint.
   - **`/hired_employees_2021`**: Retrieves the report of employees hired in 2021 expleined in queries section. Do not need to open it. Button "Check the data query 1" redirect it to this endpoint.
   - **`/departments_above_mean`**: Lists departments that hired more employees than the average. Do not need to open it. Button "Check the data query 2" redirect it to this endpoint.

### API Requirements

The required Python packages for running the REST API are specified in the `requirements.txt` file, which includes:

- `flask`
- `flask_restful`
- `flask_sqlalchemy`
- `fastavro`
- `pandas`
- `sqlalchemy`

### API Features

- **Batch Data Insertion:** The API can handle batch inserts of up to 1000 rows per request.
- **Backup and Restore:** Easily back up and restore table data using the provided rest API interface.

### Clarifications

- The CSV files are comma-separated and they are downloaded and located in the `csv_files/` folder.
- The AVRO backup files are located in the `avro_files/` folder.
- The database is managed using SQLAlchemy, with a SQL database backend.
- Data
