from database import connection
from database.models import users_model


class UsersController():
    def __init__(self):
        connection.database.connect(reuse_if_open=True)

    def login(self, login, password):
        try:
            user = users_model.getByLogin(login)
            if user and user.password == password:
                return {
                    "user_id": user.id,
                    "name": user.name,
                    "privileged": user.privileged,
                } 
            return None
        except Exception as ex:
            raise ex
