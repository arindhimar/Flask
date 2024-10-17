# controllers/todo_controller.py

from flask import request, jsonify, Blueprint, current_app
from functools import wraps
import jwt
from models.todo import TodoModel

app = Blueprint('app', __name__)
todo_model = TodoModel()

# Token verification decorator
def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        token = auth_header.split(' ')[1] if auth_header else None

        if not token:
            token = request.args.get('token')

        if not token:
            return jsonify({'Alert!': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'Message': 'Token has expired'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'Message': 'Invalid token'}), 403

        return func(*args, **kwargs)
    return decorated

@app.route('/todos', methods=['GET'])
@token_required
def get_all_todos():
    rows = todo_model.fetch_all_todos()
    todos = [{'todoId': row[0], 'todoTitle': row[1], 'todoDescription': row[2]} for row in rows]
    return jsonify(todos)

@app.route('/todos', methods=['POST'])
@token_required
def create_todo():
    data = request.get_json() or request.form
    if 'todoTitle' not in data or 'todoDescription' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    todo_model.create_todo(data['todoTitle'], data['todoDescription'])
    return jsonify({'message': 'Todo item created successfully'}), 201

@app.route('/todos/<int:todo_id>', methods=['GET'])
@token_required
def get_todo(todo_id):
    row = todo_model.fetch_todo_by_id(todo_id)
    if row is None:
        return jsonify({'error': 'Todo item not found'}), 404
    todo = {'todoId': row[0], 'todoTitle': row[1], 'todoDescription': row[2]}
    return jsonify(todo)

@app.route('/todos/<int:todo_id>', methods=['PUT'])
@token_required
def update_todo(todo_id):
    data = request.get_json() or request.form
    if todo_model.fetch_todo_by_id(todo_id) is None:
        return jsonify({'error': 'Todo item not found'}), 404
    todo_model.update_todo(todo_id, data['todoTitle'], data['todoDescription'])
    return jsonify({'message': 'Todo item updated successfully'})

@app.route('/todos/<int:todo_id>', methods=['DELETE'])
@token_required
def delete_todo(todo_id):
    if todo_model.fetch_todo_by_id(todo_id) is None:
        return jsonify({'error': 'Todo item not found'}), 404
    todo_model.delete_todo(todo_id)
    return jsonify({'message': 'Todo item deleted successfully'}), 200
