import tornado.ioloop
import tornado.web
from folders_handler import FoldersHandler
from login_handler import LoginHandler

def make_app():
    return tornado.web.Application([
        (r"/login", LoginHandler),
        (r"/folders", FoldersHandler),
    ])

def main():
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
