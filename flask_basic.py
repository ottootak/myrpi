from flask import Flask, redirect, url_for, render_template, request
from subprocess import Popen
app = Flask(__name__)
import db_commands

#vylepsit adresy souboru

@app.route("/", methods=["GET"])
def index():
    pressed = ""

    if request.args:
        if 'rf_button' in request.args:
            pressed = request.args['rf_button']
            cmd="TS_SOCKET=/tmp/taskrf tsp python3 /home/pi/myrpi/RF/rf_send.py {}".format(pressed)
            Popen(cmd, shell=True)
        if 'wifi_button' in request.args:
            cmd="TS_SOCKET=/tmp/taskwifi tsp wakeonlan 90:2B:34:62:59:85"
            Popen(cmd, shell=True)
        return redirect(url_for("index"))
    return render_template("index.html", last_pressed=pressed)

@app.route("/api/controls")
def controls():
    if request.args:
        if 'rf_button' in request.args:
            pressed = request.args['rf_button']
            cmd="TS_SOCKET=/tmp/taskrf tsp python3 /home/pi/myrpi/RF/rf_send.py {}".format(pressed)
            Popen(cmd, shell=True)
        if 'wifi_button' in request.args:
            cmd="TS_SOCKET=/tmp/taskwifi tsp wakeonlan 90:2B:34:62:59:85"
            Popen(cmd, shell=True)
    return "controls"

@app.route("/api/getdata")
def getdata():
    if request.args:
        if 'temperature' in request.args:
            data = db_commands.select_last_temperature()
    return "ID: {}, teplota: {}°C, vlhkost: {}%, datum: {}, zarizeni: {}, baterie: {}".format(*data)
        

if __name__ == "__main__":
    app.run(host='192.168.20.17', port=8080, debug=False)
