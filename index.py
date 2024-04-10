import os
import requests
from waitress import serve
from flask import Flask, request, render_template

app = Flask(__name__)

# access_token = os.environ["SNIPE_IT_ACCESS_TOKEN"]
access_token = open("SNIPE_IT_ACCESS_TOKEN.txt", "r").readline()
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": "Bearer " + access_token
}

@app.route("/", methods = ["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("home.html", data = None)
    
    data = find_hardware(request.form["search_criteria"])
    
    return render_template("home.html", data = data)

@app.route("/hardware")
def all_hardwares():
    url = "http://rtod.library.brocku.ca:3051/api/v1/hardware?limit=15&offset=0&sort=created_at&order=desc"
    data = requests.get(url, headers = headers).json()

    return data

@app.route("/hardware/<search>")
def find_hardware(search):
    url = "http://rtod.library.brocku.ca:3051/api/v1/hardware/?limit=15&offset=0&sort=created_at&order=desc&search={0}"
    data = requests.get(url.format(search), headers=headers).json()

    filtered_data = []
    for row in data["rows"]:
        if search and search in row["name"]:
            filtered_data.append(row)
    
    data["searched_with"] = search
    data["rows"] = filtered_data

    return data

if __name__ == "__main__":
    port = 8080
    print("Running on {0}".format(port))
    serve(app, host="127.0.0.1", port=port)