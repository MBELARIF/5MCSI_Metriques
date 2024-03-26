from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)    

@app.route('/commits/')
def get_commits():
    # Récupérer les données des commits depuis l'API GitHub
    url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'
    response = requests.get(url)
    commits_data = response.json()

    # Compter les commits par minute
    commits_per_minute = {}
    for commit in commits_data:
        commit_date_string = commit['commit']['author']['date']
        commit_date_object = datetime.strptime(commit_date_string, '%Y-%m-%dT%H:%M:%SZ')
        minute = commit_date_object.minute
        if minute in commits_per_minute:
            commits_per_minute[minute] += 1
        else:
            commits_per_minute[minute] = 1

    # Créer une liste de tuples (minute, nombre de commits) pour le graphique
    data_for_graph = [{'minute': minute, 'commits': count} for minute, count in commits_per_minute.items()]

    return jsonify(data_for_graph)

@app.route("/contact/")
def MaPremiereAPI():
    return render_template("contact.html")

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogram/")
def monhistogram():
    return render_template("histogram.html")

@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
        date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        minutes = date_object.minute
        return jsonify({'minutes': minutes})

@app.route('/')
def hello_world():
    return render_template('hello.html')
  
  
if __name__ == "__main__":
  app.run(debug=True)
