from flask.ext.script import Manager
from server import main_app

manager = Manager(main_app)

if __name__ == '__main__':
	manager.run()
