# tidak menyiapkan program untuk counter.
from flask import Flask, render_template
from flask.cli import F
import netifaces as ni
import datetime
from temp import get_suhu

app = Flask(__name__)

ipaddr = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
# ipaddr = ni.ifaddresses('wlp3s0')[ni.AF_INET][0]['addr']

# Function to get current time
# def get_current_time():
    # return datetime.datetime.now().strftime("%H:%M")

@app.route('/')
def index():
    return render_template('index.html', temperature=get_suhu(4))
    # return render_template('index.html', temperature=5)

if __name__ == '__main__':
    from threading import Thread

    # Import Telebot functionality from telebot_script.py
    from main import run_telebot

    # Start Telebot in a separate thread
    telebot_thread = Thread(target=run_telebot)
    telebot_thread.start()

    app.run(host=ipaddr, port=5000)  # Run Flask app