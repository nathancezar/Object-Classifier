import json
import traceback
from base_handler import BaseHandler
from database.controllers.users_controller import UsersController


class LoginHandler(BaseHandler):
    def post(self):
        try:
            request = json.loads(self.request.body)
            usersController = UsersController()
            user = usersController.login(request["login"], request["password"])
            if user is not None:
                self.set_status(200)
                self.write(user)
            else:
                self.set_status(401)
        except Exception as ex:
            traceback.print_exc()
            print(ex)
            self.set_status(500)
