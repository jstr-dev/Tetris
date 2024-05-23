class User:
    def __init__(self):
        self.id = None
        self.username = None
        self.email = None

    def login(self, password):
        pass 

    def logout(self):
        pass

    def register(self):
        pass

    def is_authenticated(self):
        return self.id is not None 
