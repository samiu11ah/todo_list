from todo import create_app
from todo.models import db
db.create_all(app=create_app())