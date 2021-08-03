import tornado.web
from database import connection

class BaseHandler(tornado.web.RequestHandler):
    """
        Aggregates code that is common to all custom handlers.
    """

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, Content-Type")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, OPTIONS')

    def prepare(self):
        """
            Always called when a request initiates.
        """
        connection.database.connect()

    def on_finish(self):
        """
            Always called when a request finishes.
        """
        if not connection.database.is_closed():
            connection.database.close()

    def options(self):
        """
            Placeholder for OPTIONS support.
        """
        pass
