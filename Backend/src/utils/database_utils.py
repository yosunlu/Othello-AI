import os
from sqlalchemy import create_engine
import json
#logic for CRUD operations on database for users and games

DATABASE_NAME = os.getenv('DATABASE_NAME')
DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_PORT = os.getenv('DATABASE_PORT')

class UserDB:
    def __init__(self):
        engine = create_engine(f"mysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_NAME}:{DATABASE_PORT}/{DATABASE_NAME}",echo = True)
        self.conn = engine.connect()

    def create_user():
        pass

    def delete_user():
        pass

    def update_user():
        pass

    def read_user(self, user_name):
        """
        This method takes user_name as input and returns password, authorization and userstatus as response
        :param user_name string type username
        :return json dumps of the json with username, password, role and status. 
        if a user is not found json will contain username and an error message.
        """
        
        user_query = f"select l.user, l.password, r.role, s.status_text from \
            login l left outer join user_status s on l.status_id = s.status_id left \
            outer join roles r on l.role_id = r.role_id where l.user=\"{user_name}\""
        
        for record in self.conn.execute(user_query):
            str_record = str(record)
            user_json = {"user_name": str_record[0],
                "user_password": str_record[1],
                "user_role": str_record[2],
                "user_status": str_record[3]}
            return json.dumps(user_json)
        #if user is not found this will be returned
        user_json = {
            "user_name": user_name,
            "message": "no user found"
        }
        return json.dumps(user_json)





    
