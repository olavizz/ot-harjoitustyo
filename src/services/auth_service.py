from repositories.auth_repository import auth_repository


class AuthService:
    def get_login_user_id(self, username, password):
        user_id = auth_repository.get_user_id(username, password)
        return user_id

    def _check_user(self, username, password):
        user = auth_repository.check_user(username, password)

        if user:
            return True
        else:
            return False

    def register_user(self, username, password):
        if auth_repository.username_exists(username):
            print("user already in database")
            return False
        success = auth_repository.register_user(username, password)
        if success:
            print("user added")
            return True
        else:
            print("failed to register user")
            return False


auth_service = AuthService()
