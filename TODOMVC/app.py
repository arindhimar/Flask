from flask import Flask, render_template, jsonify, request
from controllers.todo_controller import app as todo_app, token_required
from models.todo import TodoModel

import jwt

app = Flask(__name__)

# Set the secret key for the application
app.config['SECRET_KEY'] = 'f6ce56d2c5c041ba90b010929a293640'

# Register the controller blueprint
app.register_blueprint(todo_app)

# Create an instance of the TodoModel
todo_model = TodoModel()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username == 'admin' and password == 'admin':  
        token = jwt.encode({'username': username}, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token}), 200
    else:
        return jsonify({'message': 'Invalid credentials!'}), 401

@app.route('/dashboard', methods=['GET'])
@token_required
def dashboard():
    rows = todo_model.fetch_all_todos()
    todos = [{'todoId': row[0], 'todoTitle': row[1], 'todoDescription': row[2]} for row in rows]
    return render_template("index.html", todos=todos)

@app.route('/', methods=['GET'])
def home():
    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)
