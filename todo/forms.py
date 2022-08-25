from flask_wtf import FlaskForm
from wtforms import StringField, SelectField





class TodoForm(FlaskForm):
    priorities = [
        ('0', 'ohne'),
        ('1', 'Niedrig'),
        ('2', 'Mittel'),
        ('3', 'hoch'),
    ]
    title = StringField("Todo")
    priority = SelectField('Priority', choices=priorities)
    # category = SelectField("Category")

    # def __init__(self):
    #     super(TodoForm, self).__init__()
    #     self.category.choices = [(c.id, f'{c.name} - color: {c.color}') for c in Category.query.filter_by(user=current_user)]

class CategoryForm(FlaskForm):
    name = StringField("Category Name")

