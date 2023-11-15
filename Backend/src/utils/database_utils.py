import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import json
#logic for CRUD operations on database for users and games

DATABASE_NAME = os.getenv('DATABASE_NAME')
DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_PORT = os.getenv('DATABASE_PORT')

# create the engine to connect to the database
engine = create_engine(f"mysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}",echo = True)

# create a session and bind the engine to it
SessionLocal = sessionmaker(bind = engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class DatabaseUtils:
    """
    Class to perform CRUD operations on user database
    """
    def __init__(self, db_session):
        self.db_session = db_session
    
    def create_user(self, username:str , user_password:str, user_role: str) -> bool or str:
        """
        This method takes username, user_password and user_role as input and creates a new user in the database.
        :param username string type username
        :param user_password string type password
        :param user_role string type role
        :return True if user is created successfully, else returns the error message
        """
        try:
            insert_query = f"insert into login (user, role_id, status_id, password) values (\"{username}\", (select role_id from roles where role = \"{user_role}\"), (select status_id from user_status where status_text = \"active\"), \"{user_password}\");"
            self.db_session.execute(insert_query)
            return True
        except Exception as ex:
            return str(ex)

    def deactivate_user(self, username:str) -> bool or str:
        """
        This method takes username as input and deletes the user from the database.
        :param username string type username
        :return True if user is deleted successfully, else returns the error message
        """
        try:
            deactivate_query = f"update login set status_id = (select status_id from user_status where status_text = \"inactive\") where user = \"{username}\";"
            self.db_session.execute(deactivate_query)
            return True
        except Exception as ex:
            return str(ex)
        
    def reactivate_user(self, username:str) -> bool or str:
        """
        This method takes username as input and reactivates the user in the database.
        :param username string type username
        :return True if user is reactivated successfully, else returns the error message
        """
        try:
            reactivate_query = f"update login set status_id = (select status_id from user_status where status_text = \"active\") where user = \"{username}\";"
            self.db_session.execute(reactivate_query)
            return True
        except Exception as ex:
            return str(ex)

    def update_password(self, username: str, user_password: str) -> bool or str:
        """
        This method takes username and user_password as input and updates the password in the database.
        :param username string type username
        :param user_password string type password
        :return True if password is updated successfully, else returns the error message
        """
        try:
            update_password_query = f"update login set password = \"{user_password}\" where user = \"{username}\";"
            self.db_session.execute(update_password_query)
            return True
        except Exception as ex:
            return str(ex)

    def read_user(self, username: str) -> str:
        """
        This method takes username as input and returns password, authorization and userstatus as response
        :param username string type username
        :return json dumps of the json with username, password, role and status. 
        if a user is not found json will contain username and an error message.
        """

        user_query = text(
            f"SELECT l.user_id, l.username, l.password, l.privilege FROM othello.Login l WHERE l.username = :username"
        )
    
        result = self.db_session.execute(user_query, {'username': username}).mappings().first()

        if result:
            user_json = {
                "user_id": result['user_id'],
                "username": result['username'],
                "user_password": result['password'],
                "user_privilege": result['privilege']
            }
            return json.dumps(user_json)
        else:
            user_json = {
                "username": username,
                "message": "No user found"
            }
            return json.dumps(user_json)

        # user_query = f"select l.user, l.password, r.role, s.status_text from \
        #     login l left outer join user_status s on l.status_id = s.status_id left \
        #     outer join roles r on l.role_id = r.role_id where l.user=\"{username}\""
        
        # for record in self.db_session.execute(user_query):
        #     str_record = str(record)
        #     user_json = {"username": str_record[0],
        #         "user_password": str_record[1],
        #         "user_role": str_record[2],
        #         "user_status": str_record[3]}
        #     return json.dumps(user_json)
        # #if user is not found this will be returned
        # user_json = {
        #     "username": username,
        #     "message": "no user found"
        # }

        # return json.dumps(user_json)
    
    def delete_user(self, username: str) -> bool or str:
        """
        This method takes username as input and deletes the user from the database.
        :param username string type username
        :return True if user is deleted successfully, else returns the error message
        """
        try:
            delete_user_query = f"delete from login where user = \"{username}\";"
            self.db_session.execute(delete_user_query)
            return True
        except Exception as ex:
            return str(ex)
    
    #unit testing
    #update er diagram to match database design





    
