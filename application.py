from book_library_api import create_app


application = create_app('production')

# if __name__ == '__main__':
#    application.run()
# this for aws, need application.py to start app