# https://www.codegrepper.com/code-examples/python/how+to+run+python+script+in+flask
# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask
from flask_script import Manager # pip install Flask-Script
 
import main

manager = Manager(main)

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)
 
# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/')
# ‘/’ URL is bound with get_twitter_feed() function.
def run_py_file():
	main.main()
	return "The 1500 tweets has downloaded."
 
# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()
    manager.run()
