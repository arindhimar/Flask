import bcrypt

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
    
