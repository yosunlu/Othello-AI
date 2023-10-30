class UserSession:
    def __init__(self, user_id, user_name, user_privilege, user_email = None):
        self.user_id = user_id
        self.user_name = user_name
        self.user_privilege = user_privilege
        self.user_email = user_email
        self.user_token = None

    def to_json(self):
        return {
            'user_id': self.user_id,
            'user_name': self.user_name,
            'user_privilege': self.user_privilege,
            'user_email': self.user_email
        }

    def __str__(self):
        return f'UserSession(user_id={self.user_id}, user_name={self.user_name}, user_type={self.user_privilege}, user_email={self.user_email})'

    def __repr__(self):
        return self.__str__()
    
    def setUserToken(self, token):
        self.user_token = token

    def getUserToken(self):
        return self.user_token