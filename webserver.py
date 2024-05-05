# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask
# from tesinput2 import start
# import netifaces as ni

# ip = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
# ipaddr = ip

# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)

# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def hello_world():
	# return start()
	return 'Hello World'

# main driver function
if __name__ == '__main__':

	# run() method of Flask class runs the application 
	# on the local development server.

    
	app.run()
