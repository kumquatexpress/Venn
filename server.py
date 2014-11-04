from routes import app
from flask import Flask

main_app = Flask(__name__)
main_app.register_blueprint(app)

if __name__ == "__main__":
    main_app.run()