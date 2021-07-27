import tornado.ioloop
import tornado.web
import json
from images_handler import ImagesHandler
from folders_handler import FoldersHandler
from login_handler import LoginHandler
from training_handler import TrainingHandler

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
