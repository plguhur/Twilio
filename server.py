import time
import json
import gspread
from datetime import datetime, timedelta
import os
from utils import *

# initialize
config = configuration('client_secret.json')
workbook = get_workbook(config)


# Flask server
app = Flask(__name__,static_folder='app/static')

# Pages for the website
@app.route("/", methods=['GET', 'POST'])
def hello_world():
    return render_template('index.html')
@app.route("/venue", methods=['GET', 'POST'])
def returnVenue():
    return render_template('venue.html')
@app.route("/food", methods=['GET'])
def returnFood():
    return render_template('food.html')
@app.route("/contact", methods=['GET', 'POST'])
def returnContact():
    return render_template('contact.html')
@app.route("/gifts", methods=['GET', 'POST'])
def returnGifts():
    return render_template('gifts.html')
@app.route("/faq", methods=['GET', 'POST'])
def returnFAQ():
    return render_template('faq.html')
@app.errorhandler(500)
def internal_error(error):
    return "500 error"
    return "!!!!"  + repr(error)

# Callback for Twilio server
@app.route("/messages", methods=['GET', 'POST'])
def callback_msgs():
    return receive_msgs(request)


if __name__ == "__main__":
    app.run(host=SERVER_IP, port=8080)
