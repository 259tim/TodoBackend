import time
from flask import Flask

app = Flask(__name__)

# because the app is accessed through Expo/React Native you have to host the application on your public network
# the localhost does NOT work. 
# run: "flask run --host=192.168.178.11" <- Please check what your local device's IP is, this depends on your situation
# 'ipconfig' on Windows or `ip address`/`ifconfig` on Linux to check
@app.route('/time')
def get_current_time():
    return {'time': time.time()}