from flask import Flask, request, jsonify,render_template
import psycopg2

app = Flask(__name__)

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

# GET all todos
@app.route('/todos', methods=['GET'])
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
    return render_template('index.html', todos=todos)

if __name__ == "__main__":
    app.run(debug=True)