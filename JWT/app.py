from flask import json, render_template, Flask, session, request, jsonify, redirect, url_for
import jwt
from functools import wraps


app = Flask(__name__)
app.config['SECRET_KEY'] = 'f6ce56d2c5c041ba90b010929a293640'

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'Alert!': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'Message': 'Invalid token'}), 403
        return func(*args, **kwargs)
    return decorated


@app.route("/")
def main():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "<p>Hello, authenticated user!</p>"

@app.route("/protected")
@token_required
def protected():
    return "<p>Hello, authenticated user!</p>"

@app.route("/login", methods=['POST'])
def login():
    if request.form['username'] == "admin" and request.form['userpass'] == "admin":
        session['logged_in'] = True
        payload = {
            'username': request.form['username'],
            'userpassword': request.form['userpass']
        }
        token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token})
    else:
        return "nahi ho raha hai!!"

@app.route("/auth", methods=['POST'])
def auth():
    token = request.form['token']
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'])
        return redirect(url_for('protected', token=token))
    except:
        return jsonify({'Message': 'Invalid token'}), 403

if __name__ == "__main__":
    app.run(debug=True)