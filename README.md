# Globant_code_challange
This project is big data migration to a new database system.

1. It is a FLask REST API with python made to upload the inputs CSV files (1 up to 1000 rows) for the Big Data migration. 

--- Create folder as virtual environmoent
python -m venv .venv
---- Activate environmoent
source .venv/Scrips/activate

--Install flask and flask_restful and flask_sqlalchemy
pip install flask
pip install flask_restful
pip install flask_sqlalchemy
pip install fastavro
pip install pandas

--Create a requirements file
pip freeze > requirements.txt
