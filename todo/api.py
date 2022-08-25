# flask imports
from os import curdir
from flask import request, jsonify, make_response, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
# imports for PyJWT authentication
import jwt
from datetime import datetime, timedelta
from functools import wraps
from . import db
from .models import Category, User, Todo, TodoSchema, CategorySchema

SECRET_KEY = 'a3410e5f349e760123db6e01649311f9dc6866a3cb320081bc08bb0ed48f22c'
api = Blueprint('api', __name__)

# creates Flask object
# app = create_app()
# configuration
# NEVER HARDCODE YOUR CONFIGURATION IN YOUR CODE
# INSTEAD CREATE A .env FILE AND STORE IN IT
# database name

# decorator for verifying the JWT
def token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		token = None
		# jwt is passed in the request header
		if 'x-access-token' in request.headers:
			token = request.headers['x-access-token']
		# return 401 if token is not passed
		if not token:
			return jsonify({'Botschaft' : 'Token fehlt !!'}), 401

		try:
			# decoding the payload to fetch the stored details
			data = jwt.decode(token, SECRET_KEY)
			current_user = User.query.filter_by(username = data['username']).first()
		except:
			return jsonify({
				'Botschaft' : 'Token ist ungültig !!'
			}), 401
		# returns the current logged in users contex to the routes
		return f(current_user, *args, **kwargs)

	return decorated


# Get ALL users todos
@api.route('/api/user_todos', methods =['GET'])
@token_required
def user_todos(current_user):
    todos = Todo.query.filter_by(user=current_user)

    todo_schema = TodoSchema(many=True)

    return todo_schema.dump(todos)

# Get Single Todo
@api.route('/api/user_todos/<int:id>', methods =['GET'])
@token_required
def get_user_todo(current_user, id):
    todo = Todo.query.filter_by(id=id).first()

    todo_schema = TodoSchema()

    return todo_schema.dump(todo)

# create Single Todo
@api.route('/api/user_todos/create', methods =['POST'])
@token_required
def create_user_todo(current_user):
    data = request.json
    date = data.get('date')
    print(data)
    year  = int(date[:4])
    month =  int(date[5:7])
    date = int(date[8:10])

    date =datetime(year,month,date)
    todo = Todo(
        user_id=current_user.id,
        title=data.get('title'),
        category_id=data.get('category'),
        priority=data.get('priority'),
        date=date
    )

    db.session.add(todo)
    db.session.commit()

    todo_schema = TodoSchema()

    return todo_schema.dump(todo)

# update Single Todo
@api.route('/api/user_todos/update/<int:id>', methods =['PUT'])
@token_required
def udpate_user_todo(current_user, id):
    data = request.json

    todo = Todo.query.filter_by(id=id, user=current_user).first()


    if data.get('date'):
        date = data.get('date')
        print(data)
        year  = int(date[:4])
        month =  int(date[5:7])
        date = int(date[8:10])

        date =datetime(year,month,date)
        todo.date = date
    
    if data.get('title'):
        todo.title = data.get('title')
    
    if data.get('category'):
        todo.category = data.get('category')
    
    if data.get('priority'):
        todo.priority = data.get('priority')

    db.session.commit()

    todo_schema = TodoSchema()

    return todo_schema.dump(todo)

# Delete Single Todo
@api.route('/api/user_todos/delete/<int:id>', methods =['DELETE'])
@token_required
def delete_user_todo(current_user, id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return {'Botschaft': f'Aufgabe gelöscht (id={todo.id})'}

# get all user categories
@api.route('/api/user_categories', methods =['GET'])
@token_required
def user_categories(current_user):
    categories = Category.query.filter_by(user=current_user)

    category_schema = CategorySchema(many=True)

    return category_schema.dump(categories)

# create user category
@api.route('/api/user_categories/create', methods =['POST'])
@token_required
def create_user_category(current_user):
    data = request.json
    category = Category(user=current_user, name=data.get('name'), color=data.get('color'))

    db.session.add(category)
    db.session.commit()

    category_schema = CategorySchema()

    return category_schema.dump(category)

# get single user category
@api.route('/api/user_categories/<int:id>', methods =['GET'])
@token_required
def get_user_category(current_user, id):
    category = Category.query.filter_by(id=id, user=current_user).first()

    category_schema = CategorySchema()

    return category_schema.dump(category)

# update single user category
@api.route('/api/user_categories/update/<int:id>', methods =['PUT'])
@token_required
def update_user_category(current_user, id):
    data = request.json
    category = Category.query.filter_by(id=id, user=current_user).first()

    if data.get('name'):
        category.name = data.get('name')
    
    if data.get('color'):
        category.color = data.get('color')

    db.session.commit()

    category_schema = CategorySchema()

    return category_schema.dump(category)

# delete single user category
@api.route('/api/user_categories/delete/<int:id>', methods =['DELETE'])
@token_required
def delete_user_category(current_user, id):
    category = Category.query.filter_by(id=id, user=current_user).first()

    db.session.delete(category)
    db.session.commit()

    return {'Botschaft': f'Kategorie gelöscht (id={category.id})'}

@api.route('/api/login', methods=['POST'])
def login():
    auth = request.json
    print(auth)

    if not auth or not auth.get('username') or not auth.get('password'):
        return make_response('Konnte nicht verifiziert werden', 401, {'WWW-Authenticate' : 'Basic realm ="Benutzer existiert nicht !!"'})

    user = User.query.filter_by(username = auth.get('username')).first()

    if not user:
        return make_response('Konnte nicht verifiziert werden', 401, {'WWW-Authenticate' : 'Basic realm ="Benutzer existiert nicht !!"'})
    
    if check_password_hash(user.password, request.json.get('password')):
        token = jwt.encode({
            'username': user.username,
            'exp': datetime.utcnow() + timedelta(minutes = 30)
        }, SECRET_KEY)
        return make_response(jsonify({'token' : token.decode('UTF-8')}), 201)
    
    return make_response('Konnte nicht verifiziert werden', 401, {'WWW-Authenticate' : 'Wrong Password !!'})

# # signup route
# @api.route('/api/signup', methods =['POST'])
# def signup():
# 	# creates a dictionary of the form data
# 	data = request.form

# 	# gets name, email and password
# 	name, username,  email = data.get('name'), data.get('username'), data.get('email')
# 	password = data.get('password')

# 	# checking for existing user
# 	user = User.query.filter_by(username = username).first()

# 	if not user:
# 		# database ORM object
# 		user = User(name = name, username=username, email = email, password = generate_password_hash(password))
# 		# insert user
# 		db.session.add(user)
# 		db.session.commit()

# 		return make_response('Successfully registered.', 201)
# 	else:
# 		# returns 202 if user already exists
# 		return make_response('User already exists. Please Log in.', 202)

