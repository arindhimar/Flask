import psycopg2

host = "localhost"
database = "todoApiDb"
user = "postgres"
password = "root"

class TodoModel:
    def __init__(self):
        self.conn = self.get_db_connection()

    def get_db_connection(self):
        return psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )

    def fetch_all_todos(self):
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM "todoApiTb"')
        todos = cur.fetchall()
        cur.close()
        return todos

    def fetch_todo_by_id(self, todo_id):
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM "todoApiTb" WHERE "todoId" = %s', (todo_id,))
        todo = cur.fetchone()
        cur.close()
        return todo

    def create_todo(self, title, description):
        cur = self.conn.cursor()
        cur.execute('INSERT INTO "todoApiTb" ("todoTitle", "todoDescription") VALUES (%s, %s)', (title, description))
        self.conn.commit()
        cur.close()

    def update_todo(self, todo_id, title, description):
        cur = self.conn.cursor()
        cur.execute('UPDATE "todoApiTb" SET "todoTitle" = %s, "todoDescription" = %s WHERE "todoId" = %s', (title, description, todo_id))
        self.conn.commit()
        cur.close()

    def delete_todo(self, todo_id):
        cur = self.conn.cursor()
        cur.execute('DELETE FROM "todoApiTb" WHERE "todoId" = %s', (todo_id,))
        self.conn.commit()
        cur.close()

    def close_connection(self):
        self.conn.close()
