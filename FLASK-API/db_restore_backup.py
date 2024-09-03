import fastavro
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

def avro_to_table(file_name, model):
    # Initialize database session
    engine = create_engine('sqlite:///mydatabase.db')
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

    session.close()

avro_to_table('table_one.avro', TableOne)
avro_to_table('table_two.avro', TableTwo)
avro_to_table('table_three.avro', TableThree)

