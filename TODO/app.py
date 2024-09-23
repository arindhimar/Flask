from flask import Flask, render_template,request,redirect,url_for,flash,session
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

@app.route('/')
def mainPage():
    tempData = Todo.query.all()
    return render_template("index.html", tempData=tempData)

@app.route('/addNewData', methods=['GET', 'POST'])
def addData():
    if request.method == "POST":
        tempToDo = Todo(todoTitle=request.form['title'], todoDescription=request.form['description'])
        db.session.add(tempToDo)
        db.session.commit()
        return redirect(url_for('mainPage'))  
    return render_template("index.html")

@app.route('/delete/<int:tempId>')
def delete(tempId):
    tempDeleteData = Todo.query.filter(todoId=tempId).first()
    db.session.commit()
    return redirect(url_for('mainPage'))  
    

@app.route('/getSingleData/<int:tempId>')
def getSingleData(tempId):
    tempGetData = Todo.query.get(tempId)
    if tempGetData is None:
        flash('Todo item not found!')
        return redirect(url_for('mainPage'))
    session['todoId'] = tempId
    return render_template("update_todo.html", tempGetData=tempGetData)

@app.route('/updateData', methods=['POST'])
def updateData():
    todoId = session.get('todoId')
    if todoId is None:
        flash('Todo item not found!')
        return redirect(url_for('mainPage'))
    tempGetData = Todo.query.get(todoId)
    if tempGetData is None:
        flash('Todo item not found!')
        return redirect(url_for('mainPage'))
    tempGetData.todoTitle = request.form['title']
    tempGetData.todoDescription = request.form['description']
    db.session.commit()
    flash('Todo item updated successfully!')
    return redirect(url_for('mainPage'))


if __name__ == "__main__":
    with app.app_context():
        db.create_all() 
    app.run(debug=True)