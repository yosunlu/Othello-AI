import pytest
import sys
import json
sys.path.append("..")

from database_utils import DatabaseUtils, SessionLocal

@pytest.fixture
def declare_database():
    """
    initialize DatabaseUtils class, so that it acts similar to singleton
    """
    return DatabaseUtils(SessionLocal())

def test_create_user(declare_database):
    """
    positive testcase for create_user method of DatabaseUtils class
    """
    database_utils = declare_database
    create_user_response = database_utils.create_user('sample_userid1','test_user', 'test_password', 'test_privilege')
    assert create_user_response == True

def test_create_user_with_existing_username(declare_database):
    """
    negative testcase for create_user method of DatabaseUtils class
    """
    database_utils = declare_database
    create_user_response = database_utils.create_user('0b96524d-dfb9-45a5-bf16-ed686d9df14f','gino', 'CaptainDuck', 'player')
    assert create_user_response != True

def test_update_password(declare_database):
    """
    positive testcase for update_password method of DatabaseUtils class
    """
    database_utils = declare_database
    update_password_response = database_utils.update_password('test_user', 'CaptainDuck')
    assert update_password_response == True

def test_read_user(declare_database):
    """
    positive testcase for read_user method of DatabaseUtils class
    """
    database_utils = declare_database
    read_user_response = database_utils.read_user('gino')
    print(read_user_response)
    assert read_user_response == json.dumps({"user_id": "0b96524d-dfb9-45a5-bf16-ed686d9df14f", "username": "gino", "user_password": "CaptainDuck", "user_privilege": "player"})

def test_read_user_nonexistent(declare_database):
    """
    testcase for read_user method of DatabaseUtils class when user does not exist
    """
    database_utils = declare_database
    read_user_response = database_utils.read_user('shoufil')
    print(read_user_response)
    assert read_user_response == json.dumps({
                "username": "shoufil",
                "message": "No user found"
            })
    
def test_delete_user(declare_database):
    """
    testcase for delete_user method of DatabaseUtils class
    """
    database_utils = declare_database
    delete_user_response = database_utils.delete_user('test_user')
    assert delete_user_response == True

def test_create_user_session(declare_database):
    """
    positive testcase for create_user_session method of DatabaseUtils class
    """
    database_utils = declare_database
    create_user_session_response = database_utils.create_user_session('sample_session', 'sample_userid1', 'sample_username', 'sample_privilege')
    assert create_user_session_response == True

def test_create_user_session_with_existing_session_id(declare_database):
    """
    negative testcase for create_user_session method of DatabaseUtils class
    """
    database_utils = declare_database
    create_user_session_response = database_utils.create_user_session('sample_session', 'sample_userid1', 'sample_username', 'sample_privilege')
    assert create_user_session_response != True

def test_read_user_session(declare_database):
    """
    positive testcase for read_user_session method of DatabaseUtils class
    """
    database_utils = declare_database
    read_user_session_response = database_utils.read_user_session('sample_session')
    assert read_user_session_response == json.dumps({"session_id": "sample_session", "user_id": "sample_userid1", "username": "sample_username", "user_privilege": "sample_privilege"})

def test_read_user_session_nonexistent(declare_database):
    """
    testcase for read_user_session method of DatabaseUtils class when session does not exist
    """
    database_utils = declare_database
    read_user_session_response = database_utils.read_user_session('sample_session1')
    assert read_user_session_response == json.dumps({
                "session_id": "sample_session1",
                "message": "No session found"
            })
    
def test_delete_user_session(declare_database):
    """
    testcase for delete_user_session method of DatabaseUtils class
    """
    database_utils = declare_database
    delete_user_session_response = database_utils.delete_user_session('sample_session')
    assert delete_user_session_response == True
