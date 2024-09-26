from flask import Flask, request, jsonify,render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///quiz.db"
db = SQLAlchemy(app)
app.secret_key = 'my_secret_key_1234567890'


class Todo(db.Model):
    todoId = db.Column(db.Integer, primary_key=True)
    todoTitle = db.Column(db.String, nullable=True)
    todoDescription = db.Column(db.String, nullable=False)
    
    def __repr__(self) -> str:
        return f"{self.todoId} - {self.todoTitle} - {self.todoDescription}"

@app.route('/todos', methods=['GET'])
def get_all_todos():
    todos = Todo.query.all()
    return jsonify([{'todoId': todo.todoId, 'todoTitle': todo.todoTitle, 'todoDescription': todo.todoDescription} for todo in todos])

@app.route('/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    new_todo = Todo(todoTitle=data['title'], todoDescription=data['description'])
    db.session.add(new_todo)
    db.session.commit()
    return jsonify({'todoId': new_todo.todoId, 'todoTitle': new_todo.todoTitle, 'todoDescription': new_todo.todoDescription}), 201

@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if todo is None:
        return jsonify({'error': 'Todo item not found'}), 404
    return jsonify({'todoId': todo.todoId, 'todoTitle': todo.todoTitle, 'todoDescription': todo.todoDescription})

@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if todo is None:
        return jsonify({'error': 'Todo item not found'}), 404
    data = request.get_json()
    todo.todoTitle = data['title']
    todo.todoDescription = data['description']
    db.session.commit()
    return jsonify({'todoId': todo.todoId, 'todoTitle': todo.todoTitle, 'todoDescription': todo.todoDescription})

@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if todo is None:
        return jsonify({'error': 'Todo item not found'}), 404
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message': 'Todo item deleted successfully'}), 200

@app.route('/', methods=['GET'])
def home():
    todos = Todo.query.all()
    return render_template('index.html', todos=todos)

if __name__ == "__main__":
    with app.app_context():
        db.create_all() 
    app.run(debug=True)