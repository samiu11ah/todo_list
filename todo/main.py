from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Todo, Category
from .forms import TodoForm, CategoryForm
from sqlalchemy import asc, desc
from datetime import datetime
from . import db

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == "POST":
        title = request.form.get('title')
        category_id = request.form.get('category')
        priority = request.form.get('priority')
        date = request.form.get('date')
        year  = int(date[:4])
        month =  int(date[5:7])
        date = int(date[8:10])
        
        date =datetime(year,month,date)

        todo = Todo(title=title, category_id=category_id, priority=priority, user_id=current_user.id, date=date)
        db.session.add(todo)
        db.session.commit()
        flash(f"{todo} erstellt...")
        return redirect(url_for('main.index'))
    
    sort_by = request.args.get('sort_by')
    descending = request.args.get('descending')


    form = TodoForm()
    todos = Todo.query.filter_by(user=current_user)

    if sort_by == 'date':
        todos = Todo.query.order_by(asc(Todo.date)).filter_by(user=current_user)
        if descending == 'yes':
            todos = Todo.query.order_by(desc(Todo.date)).filter_by(user=current_user)
            print('order by date, descending')
            

    if sort_by == 'priority':
        todos = Todo.query.order_by(asc(Todo.priority)).filter_by(user=current_user)
        if descending == 'yes':
            todos = Todo.query.order_by(desc(Todo.priority)).filter_by(user=current_user)
            print('order by priority, descending')
    
    
    choices = Category.query.filter_by(user=current_user)

    return render_template('main/index.html', form=form, todos=todos, choices=choices, sort_by=sort_by, descending=descending, existing_todo=[])

# UPDATE TODO
@main.route('/todos/<int:todo_id>', methods=['GET', 'POST'])
@login_required
def update_todo(todo_id):
    existing_todo = Todo.query.get(todo_id)

    if request.method == "POST":
        existing_todo.title = request.form.get('title')
        existing_todo.category_id = request.form.get('category')
        existing_todo.priority = request.form.get('priority')
        date = request.form.get('date')
        year  = int(date[:4])
        month =  int(date[5:7])
        date = int(date[8:10])

        existing_todo.date =datetime(year,month,date)

        db.session.commit()
        flash(f"{existing_todo} Aktualisiert...")
        return redirect(url_for('main.index'))
    
    sort_by = request.args.get('sort_by')
    descending = request.args.get('descending')


    form = TodoForm()
    todos = Todo.query.filter_by(user=current_user)

    if sort_by == 'title':
        todos = Todo.query.order_by(asc(Todo.title)).filter_by(user=current_user)
        if descending == 'yes':
            todos = Todo.query.order_by(desc(Todo.title)).filter_by(user=current_user)
            print('order by title, descending')
            

    if sort_by == 'priority':
        todos = Todo.query.order_by(asc(Todo.priority)).filter_by(user=current_user)
        if descending == 'yes':
            todos = Todo.query.order_by(desc(Todo.priority)).filter_by(user=current_user)
            print('order by priority, descending')
    
    
    choices = Category.query.filter_by(user=current_user)

    return render_template('main/index.html', form=form, todos=todos, choices=choices, sort_by=sort_by, descending=descending, existing_todo=existing_todo)


@main.route('/delete/<int:todo_id>')
@login_required
def delete_todo(todo_id):
    todo = Todo.query.get(todo_id)
    print(todo)
    
    if todo.user_id == current_user.id:
        db.session.delete(todo)
        db.session.commit()
        flash('Aufgabe gelöscht...')
    else:
        flash('Etwas ist schief gelaufen..')
    return redirect(url_for('main.index'))

@main.route('/toggle_status/<int:todo_id>')
@login_required
def toggle_status(todo_id):
    todo = Todo.query.get(todo_id)
    
    if todo.user_id == current_user.id:
        todo.completed = not todo.completed
        db.session.commit()
    else:
        flash('Etwas ist schief gelaufen..')
    return redirect(url_for('main.index'))

# Categories CRUD ---
@main.route('/categories', methods=['GET', 'POST'])
@login_required
def categories():
    form = CategoryForm()

    if request.method == 'POST':
        name = request.form.get('name')
        color = request.form.get('color')


        category = Category(name=name, color=color, user=current_user)

        db.session.add(category)
        db.session.commit()
        flash(f"{category} created...")

    categories = Category.query.filter_by(user_id=current_user.id)
    return render_template('main/categories.html', form = form, categories=categories)

@main.route('/categories/<int:category_id>/todos')
@login_required
def category_todos(category_id):
    category = Category.query.get(category_id)
    if not category.user_id == current_user.id:
        return redirect(url_for('main.index'))
    
    todos = Todo.query.filter_by(category_id=category.id)
    return render_template('main/category_todos.html', todos=todos, category=category)


@main.route('/delete_category/<int:category_id>')
@login_required
def delete_category(category_id):
    category = Category.query.get(category_id)
    # print(category)

    # check if same user is deleting ?
    if category.user_id == current_user.id:
        todos = Todo.query.filter_by(category=category)
        for todo in todos:
            db.session.delete(todo)
        db.session.delete(category)
        db.session.commit()
        flash('Gelöschte Kategorie und all ihre Todos ...')
    else:
        flash('Etwas ist schief gelaufen..')
    return redirect(url_for('main.categories'))

