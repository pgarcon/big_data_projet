
import sys
import os

current_folder = os.path.dirname(os.path.abspath(__file__))
parent_folder = os.path.join(current_folder, '..')
sys.path.append(parent_folder)


from flask import Flask
from flask import url_for
from flask import render_template
from datetime import datetime, timedelta
from markupsafe import escape
from model.IA.model import Prediction
from model.mongo.mongodb import Mongodb
import pandas as pd
import json


app = Flask(__name__)

prediction = Prediction()
db = Mongodb(port="27019", database="meteo", collection="meteo")

@app.route('/')
def index():
    return 'Hello there'

def getData():
    prediction.chargeModel()

    db.connexion()
    df_pred = db.get30jours()
    df_avg_temp_2023 = db.getDataPerMonth(2023)
    df_avg_temp_2022 = db.getDataPerMonth(2022)
    db.close_connection()
    
    return prediction.predict(df_pred), df_avg_temp_2023, df_avg_temp_2022

# Fonction pour obtenir les trois jours suivant le jour actuel
def jours_semaine_suivants():
    jours = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
    aujourdhui = datetime.now().weekday()
    jours_suivants = jours[aujourdhui:] + jours[:aujourdhui-1]
    return jours_suivants[:4]


jours_semaine = jours_semaine_suivants()
prediction, avg_temp_2023, avg_temp_2022 = getData()

values = []
labels = avg_temp_2023['dh_utc'].astype(str).values.tolist()
values.append(avg_temp_2023['avg_temperature'].astype(float).values.tolist())
values.append(avg_temp_2022['avg_temperature'].astype(float).values.tolist())

# Route pour afficher la météo
@app.route('/meteo')
def meteo():
    return render_template('index.html', 
                           jours_semaine=jours_semaine, 
                           prediction=prediction, 
                           labels = labels,
                           values = values)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)