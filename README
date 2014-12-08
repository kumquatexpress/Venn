Venn
====
Flask app running on mongodb: http://flask.pocoo.org/docs/0.10/

To run the server
$ python server.py
access on http://localhost:5000.

The server will not run if mongodb is not running on your machine.  To get mongodb, 
$ brew install mongodb
To run an instance of mongo at localhost:27017,
$ brew services restart mongodb

Once you have a mongo server running, the app will run and connect to your local database.  Currently it uses a table called "users" and one called "questions", which will be created when you try to insert a new user or a new question.

ORGANIZATION
------------
This app is organized into the following folders:
/venn <-- toplevel folder, root directory
	/data <-- holds example data in the form of json, might hold real data later
	/handlers <-- holds the handlers that provide functions to handle each incoming route
	/templates <-- holds html templates that are used to generate the views

Packages required: (pip install these with $ sudo pip install -r requirements.txt) 
flask
flask-pymongo
code, for debugging

Important files:
server.py <-- runs the flask server, initializes connection to the database

routes.py <-- holds each route, set up as 
@app.route([route name])
def [function_name]([parameters]):
    return [handler_name].[handler_function]()

models.py <-- holds logic having to do with each type of model and manages database i/o

Example - Creating a fake user, setting up a route
==================================================
Suppose we want to make a new user with the name of whatever matches the url after venn.com/[username]

We need to make a new route matching /[username], so we can do that in routes.py
@app.route("/<name>")
def response(name):
	User.insert({"name": name})
	return "hello, %s" % name

<variable> in the route title binds that variable to be used inside of the function as a parameter, in this case
response(name).  name has the value of whatever is in the route, so venn.com/test will now make a new user with name
"test" and then display a page that reads "hello, test".

To extricate the logic of handling these url requests, we can put the function logic from response into a handler.
In main_handler.py,
def make_new_user(name):
	User.insert({"name": name})
	return "hello, %s" % name

And now in routes we can change response to be
@app.route("/<name>")
def response(name):
	return main_handler.make_new_user(name)

This is the same exact thing, but we separated the logic of handling a request from the logic of setting up the url route itself.





