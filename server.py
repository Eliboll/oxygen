from flask import Flask, request, g, jsonify
import json
app = Flask(__name__)

JSON_FILE = "historyData.json"

@app.route("/insert")
def hello_world():
    entry = {
        "Trip_Name" : request.args["Trip_Name"],
        "Vehicle" : request.args["Vehicle"],
        "Date" : request.args["Date"],
        "Distance" : float(request.args["Distance"]),
        "CO2" : float(request.args["CO2"])
    }
    with open(JSON_FILE, "r") as json_file:
        data = json.load(json_file)
        json_file.close()
        data["entries"].insert(0,entry)
    with open(JSON_FILE, 'w') as out_file:
        json.dump(data, out_file, indent = 4)
    return {"success" : True}

@app.route("/getJSON")
def getJson():
    with open(JSON_FILE, "r") as json_file:
        data = json.load(json_file)
        json_file.close()
        return data