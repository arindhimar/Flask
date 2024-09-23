import bcrypt

class User:
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
            return True
        return False

    def __repr__(self):
        return f"User('{self.name}', '{self.email}')"