from app import app, db
import sqlalchemy 
import sqlalchemy.orm 
from app.models import User, Post 

@app.shell_context_processor
def make_shell_context():
    return {'sa': sqlalchemy, 'so': sqlalchemy.orm, 'db': db, 'User': User, 'Post': Post}

