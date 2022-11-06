from flask import Flask, request, g, jsonify
import json
app = Flask(__name__)

JSON_FILE = "historyData.json"

CSV_FILE = "vehicleDataCondensed.csv"

def getEPA(make,model,year):
    csv = open(CSV_FILE, "r")
    for row in csv.readlines():
        columns = row.split(",")
        if year in columns[4]:
            if model in columns[3]:
                if make in columns[2]:
                    csv.close()
                    return columns[0]
    csv.close()
    return 0

@app.route("/insert")
def hello_world():
    entry = {
        "Trip_Name" : request.args["Trip_Name"],
        "Make" : request.args["Make"],
        "Model" : request.args["Model"],
        "Year" : request.args["Year"],
        "Date" : request.args["Date"],
        "Distance" : float(request.args["Distance"]),
        "CO2" : getEPA(request.args["Make"],request.args["Model"],request.args["Year"]) * float(request.args["Distance"])
    }
    with open(JSON_FILE, "r") as json_file:
        data = json.load(json_file)
        json_file.close()
        data["entries"].insert(0,entry)
    with open(JSON_FILE, 'w') as out_file:
        json.dump(data, out_file, indent = 4)
    return {"success" : True,
            "CO2"   : entry["CO2"]}

@app.route("/getJSON")
def getJson():
    with open(JSON_FILE, "r") as json_file:
        data = json.load(json_file)
        json_file.close()
        return data
    
@app.route("/year")
def getyear():
    year = int(request.args["year"])
    csv = open(CSV_FILE, "r")
    make_list = []
    for row in csv.readlines():
        columns = row.split(",")
        if str(year) in columns[4]:
            if columns[2] not in make_list:
                make_list.append(columns[2])
    csv.close()
    return {"makes" : make_list}

@app.route("/yearmake")
def getmodel():
    year = int(request.args["year"])
    make = request.args["make"]
    csv = open(CSV_FILE, "r")
    model_list = []
    for row in csv.readlines():
        columns = row.split(",")
        if str(year) in columns[4]:
            if make in columns[2]:
                if columns[3] not in model_list:
                    model_list.append(columns[3])
    csv.close()
    return {"models" : model_list}

