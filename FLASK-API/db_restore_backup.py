import fastavro
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, delete
from api import Departments, Jobs, HiredEmployees
import sys

## Set variables
avro_file_input=sys.argv[1]
table_name=avro_file_input[0]

def avro_to_table(file_name, model):
    ## Initialize database session
    engine = create_engine('sqlite:////workspaces/Globant_code_challange/FLASK-API/instance/database.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    print (session.query(model.id).count())
    ## Delete bd
    session.execute(delete(model))
    print (session.query(model.id).count())

    ## Read from AVRO file
    with open('/workspaces/Globant_code_challange/avro_files/'+file_name, 'rb') as f:
        reader = fastavro.reader(f)
        records = [record for record in reader]

    ## Insert each record into the database
    for record in records:
        obj = model(**record)
        session.add(obj)
    print (session.query(model.id).count())

    ## Commit the session to save all records
    session.commit()

    ## Close session
    session.close()

print('Restore file: ' + avro_file_input)
print(table_name)
if table_name == 'j':
    print('Restore model: ' + 'Jobs')
    avro_to_table(avro_file_input, Jobs)
elif table_name == 'd':
    print('Restore model: ' + 'Departments')
    avro_to_table(avro_file_input, Departments)
elif table_name == 'h':
    print('Restore model: ' + 'HiredEmployees')
    avro_to_table(avro_file_input, HiredEmployees)

