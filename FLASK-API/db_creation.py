##Import libraies
from api import db, app

## Database creation
with app.app_context():
        db.create_all()
        
## This file is one time execution to create the database