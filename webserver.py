from flask import Flask, request, jsonify
import netifaces as ni

app = Flask(__name__)

ipaddr = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']

@app.route('/')
def home():
    return "Flask app is running!"

# ... other Flask routes and logic

if __name__ == '__main__':
    from threading import Thread

    # Import Telebot functionality from telebot_script.py
    from tesinput2 import run_telebot

    # Start Telebot in a separate thread
    telebot_thread = Thread(target=run_telebot)
    telebot_thread.start()

    app.run(host=ipaddr, port=5000)  # Run Flask app
