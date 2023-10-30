
apiBaseServiceUrl = "/othelloml_api"

class Login(object):
    apiLoginUrl = apiBaseServiceUrl + "/login"
    apiResetPasswordUrl = apiBaseServiceUrl + "/reset_password"

class Logout(object):
    apiLogoutUrl = apiBaseServiceUrl + "/logout"

class PVP(object):
    pvpSessionUrl = apiBaseServiceUrl + "/ws/pvp-session/{pvp_session_id}"
    getPvpGameSessionsUrl = apiBaseServiceUrl + "/get-pvp-sessions"

class Signup(object):
    apiSignupUrl = apiBaseServiceUrl + "/signup"

class User(object):
    apiGetUserUrl = apiBaseServiceUrl + "/user"
    apiGetUsersUrl = apiBaseServiceUrl + "/users"
    apiUpdateUserUrl = apiBaseServiceUrl + "/update_user"
    apiDeleteUserUrl = apiBaseServiceUrl + "/delete_user"
    apiAdminSettingsUrl = apiBaseServiceUrl + "/admin_settings"

class DatabaseTables(object):
    test_table = 'test_table'

class UserPrivileges(object):
    admin = "admin"
    player = "player"