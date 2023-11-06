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
    """
    Class to perform CRUD operations on user database
    """
    def __init__(self):
        engine = create_engine(f"mysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_NAME}:{DATABASE_PORT}/{DATABASE_NAME}",echo = True)
        self.conn = engine.connect()
    
    def create_user(self, user_name:str , user_password:str, user_role: str) -> bool or str:
        """
        This method takes user_name, user_password and user_role as input and creates a new user in the database.
        :param user_name string type username
        :param user_password string type password
        :param user_role string type role
        :return True if user is created successfully, else returns the error message
        """
        try:
            insert_query = f"insert into login (user, role_id, status_id, password) values (\"{user_name}\", (select role_id from roles where role = \"{user_role}\"), (select status_id from user_status where status_text = \"active\"), \"{user_password}\");"
            self.conn.execute(insert_query)
            return True
        except Exception as ex:
            return str(ex)

    def deactivate_user(self, user_name:str) -> bool or str:
        """
        This method takes user_name as input and deletes the user from the database.
        :param user_name string type username
        :return True if user is deleted successfully, else returns the error message
        """
        try:
            deactivate_query = f"update login set status_id = (select status_id from user_status where status_text = \"inactive\") where user = \"{user_name}\";"
            self.conn.execute(deactivate_query)
            return True
        except Exception as ex:
            return str(ex)
        
    def reactivate_user(self, user_name:str) -> bool or str:
        """
        This method takes user_name as input and reactivates the user in the database.
        :param user_name string type username
        :return True if user is reactivated successfully, else returns the error message
        """
        try:
            reactivate_query = f"update login set status_id = (select status_id from user_status where status_text = \"active\") where user = \"{user_name}\";"
            self.conn.execute(reactivate_query)
            return True
        except Exception as ex:
            return str(ex)

    def update_password(self, user_name: str, user_password: str) -> bool or str:
        """
        This method takes user_name and user_password as input and updates the password in the database.
        :param user_name string type username
        :param user_password string type password
        :return True if password is updated successfully, else returns the error message
        """
        try:
            update_password_query = f"update login set password = \"{user_password}\" where user = \"{user_name}\";"
            self.conn.execute(update_password_query)
            return True
        except Exception as ex:
            return str(ex)

    def read_user(self, user_name->str) -> str:
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
    
    def delete_user(self, user_name: str) -> bool or str:
        """
        This method takes user_name as input and deletes the user from the database.
        :param user_name string type username
        :return True if user is deleted successfully, else returns the error message
        """
        try:
            delete_user_query = f"delete from login where user = \"{user_name}\";"
            self.conn.execute(delete_user_query)
            return True
        except Exception as ex:
            return str(ex)
    
    #unit testing
    #update er diagram to match database design





    
