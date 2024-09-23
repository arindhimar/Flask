from flask import Flask, request, jsonify,render_template
import bcrypt
from flask_sqlalchemy import SQLAlchemy
from models import models



#configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///quiz.db"
db = SQLAlchemy(app)
app.secret_key = 'my_secret_key_1234567890'



#models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = self._hash_password(password)

    def _hash_password(self, password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password

    def authenticate(self, password):
        if bcrypt.checkpw(password.encode('utf-8'), self.password):
            return True
        return False

    def __repr__(self):
        return f"User('{self.name}', '{self.email}')"
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = self._hash_password(password)
        self.is_authenticated = False

    def _hash_password(self, password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password

    def authenticate(self, password):
        if bcrypt.checkpw(password.encode('utf-8'), self.password):
            self.is_authenticated = True
            print(password.encode('utf-8'))
            
            return True
        return False

    def __repr__(self):
        return f"User('{self.name}', '{self.email}')"
    












#routes
@app.route('/register-user', methods=['POST'])
def register_user():
    data = request.get_json()
    name = data['name']
    email = data['email']
    password = data['password']

    user = User(name, email, password)
    
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully!'})



@app.route('/login-user', methods=['POST'])
def login_user():
    data = request.get_json()
    
    email = data['email']
    password = data['password']

    # Check if the user exists
    user = User.query.filter_by(email=email).first()
    if user is None:
        return jsonify({'message': 'User not found!'}), 404

    # Check if the password is correct
    if not user.authenticate(password):
        return jsonify({'message': 'Invalid password!'}), 401

    # Login successful, return a success message
    return jsonify({'message': 'successfull','id':user.id}), 200




@app.route('/')
def showLogin():
    return render_template('index.html')

@app.route('/register')
def showRegister():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)