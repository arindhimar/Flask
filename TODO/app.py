from flask import Flask, request, jsonify, render_template, redirect, url_for
import psycopg2
import jwt

from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'f6ce56d2c5c041ba90b010929a293640'

# Database connection settings
host = "localhost"
database = "todoApiDb"
user = "postgres"
password = "root"

# Create a connection to the database
def get_db_connection():
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )
    return conn

# Token verification decorator
def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'Alert!': 'Token is missing!'}), 401

        try:
            # Specify the algorithm used during encoding
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'Message': 'Token has expired'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'Message': 'Invalid token'}), 403
        
        return func(*args, **kwargs)
    return decorated


@app.route('/dashboard', methods=['GET'])
@token_required
def dashboard():
    token = request.args.get('token')
    data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    return render_template('index.html', username=data['username'])


# GET all todos
@app.route('/todos', methods=['GET'])
@token_required
def get_all_todos():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM "todoApiTb"')
    rows = cur.fetchall()
    todos = []
    for row in rows:
        todos.append({
            'todoId': row[0],
            'todoTitle': row[1],
            'todoDescription': row[2]
        })
    conn.close()
    return jsonify(todos)

# POST a new todo
@app.route('/todos', methods=['POST'])
@token_required
def create_todo():
    data = request.get_json()
    if 'todoTitle' not in data or 'todoDescription' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO "todoApiTb" ("todoTitle", "todoDescription") VALUES (%s, %s)', (data['todoTitle'], data['todoDescription']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Todo item created successfully'}), 201

# GET a todo by id
@app.route('/todos/<int:todo_id>', methods=['GET'])
@token_required
def get_todo(todo_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM "todoApiTb" WHERE "todoId" = %s', (todo_id,))
    row = cur.fetchone()
    if row is None:
        conn.close()
        return jsonify({'error': 'Todo item not found'}), 404
    todo = {
        'todoId': row[0],
        'todoTitle': row[1],
        'todoDescription': row[2]
    }
    conn.close()
    return jsonify(todo)

# PUT a todo by id
@app.route('/todos/<int:todo_id>', methods=['PUT'])
@token_required
def update_todo(todo_id):
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM "todoApiTb" WHERE "todoId" = %s', (todo_id,))
    row = cur.fetchone()
    if row is None:
        conn.close()
        return jsonify({'error': 'Todo item not found'}), 404
    cur.execute('UPDATE "todoApiTb" SET "todoTitle" = %s, "todoDescription" = %s WHERE "todoId" = %s', (data['todoTitle'], data['todoDescription'], todo_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Todo item updated successfully'})

# DELETE a todo by id
@app.route('/todos/<int:todo_id>', methods=['DELETE'])
@token_required
def delete_todo(todo_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM "todoApiTb" WHERE "todoId" = %s', (todo_id,))
    row = cur.fetchone()
    if row is None:
        conn.close()
        return jsonify({'error': 'Todo item not found'}), 404
    cur.execute('DELETE FROM "todoApiTb" WHERE "todoId" = %s', (todo_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Todo item deleted successfully'}), 200

@app.route('/', methods=['GET'])
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.form
    if data['username'] == "admin" and data['password'] == "admin":
        payload = {'username': data['username']}
        token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
        return redirect(url_for('dashboard', token=token))
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

if __name__ == "__main__":
    app.run(debug=True)