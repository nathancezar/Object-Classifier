import tornado.ioloop
import tornado.web
from folders_handler import FoldersHandler
from login_handler import LoginHandler
from images_handler import ImagesHandler

def make_app():
    return tornado.web.Application([
        (r"/login", LoginHandler),
        (r"/folders", FoldersHandler),
        (r"/folders/user_id", FoldersHandler),
        (r"/folders/processed", FoldersHandler),
        (r"/folders/export_folder", FoldersHandler),
        (r"/folders/export_all", FoldersHandler),
        (r"/folders/export_by_type", FoldersHandler),
        (r"/folders/insert_database", FoldersHandler),
        (r"/folders/flag", FoldersHandler),
        (r"/folders/unflag", FoldersHandler),
        (r"/folders/deleted", FoldersHandler),
        (r"/images", ImagesHandler),
        (r"/images/next", ImagesHandler),
        (r"/images/previous", ImagesHandler),
        (r"/images/clear", ImagesHandler),
        (r"/images/post_processed", ImagesHandler),
        (r"/items", ImagesHandler),
    ])

def main():
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
