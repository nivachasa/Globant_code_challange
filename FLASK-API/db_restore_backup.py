import fastavro
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from api import Departments, Jobs, HiredEmployees

def avro_to_table(file_name, model):
    # Initialize database session
    engine = create_engine('sqlite:///FLASK-API/instance/database.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    # Read from AVRO file
    with open(file_name, 'rb') as f:
        reader = fastavro.reader(f)
        records = [record for record in reader]

    # Insert each record into the database
    for record in records:
        obj = model(**record)
        session.add(obj)

    # Commit the session to save all records
    session.commit()

    #Close session
    session.close()

avro_to_table('jobs_2024-09-03 18:32:15.984006.avro', Jobs)
avro_to_table('departments_2024-09-03 18:32:15.984006.avro', Departments)
avro_to_table('hired_employees_2024-09-03 18:32:15.984006.avro', HiredEmployees)

