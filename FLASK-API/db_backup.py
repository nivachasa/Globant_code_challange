import fastavro
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from api import Departments, Jobs, HiredEmployees, app
import datetime

## Create current_time variable
current_time = datetime.datetime.now()

## Create function to make full db avro backup
def table_to_avro(table_name, model, file_name):
    ## Initialize database session
    engine = create_engine('sqlite:////workspaces/Globant_code_challange/FLASK-API/instance/database.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    ## Query all data from the table
    data = session.query(model).all()

    ## Define the AVRO schema
    schema = {
        'doc': f'{table_name} data',
        'name': table_name,
        'namespace': 'my.avro.namespace',
        'type': 'record',
        'fields': [
            {'name': column.name, 'type': 'int' if column.type.python_type == int else 'string'}
            for column in model.__table__.columns
        ]
    }

    ## Convert SQLAlchemy objecurrent_times to dicurrent_timeionaries
    records = [{column.name: getattr(row, column.name) for column in model.__table__.columns} for row in data]

    ## Write to AVRO file
    with open('/workspaces/Globant_code_challange/avro_files/' + file_name, 'wb') as out:
        fastavro.writer(out, schema, records)
        print('avro file ' + file_name +' successfully created')

    session.close()
 
table_to_avro('jobs', Jobs, f'jobs_{current_time}.avro')
table_to_avro('departments', Departments, f'departments_{current_time}.avro')
table_to_avro('hired_employees', HiredEmployees, f'hired_employees_{current_time}.avro')
