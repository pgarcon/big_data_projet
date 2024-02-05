
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
from sklearn.preprocessing import MinMaxScaler
import json


app = Flask(__name__)

prediction = Prediction()
db = Mongodb(port="27019", database="meteo", collection="meteo")

@app.route('/')
def index():
    return 'Welcome on La Billy Station, the station that you need !'


def normalizeData(df1, df2, df3, df4):

    data = pd.concat([df1.set_index('dh_utc'), df2.set_index('dh_utc'), df3.set_index('dh_utc'), df4.set_index('dh_utc')], 
                     axis=1, 
                     keys=['avg_temperature', 'avg_pressure', 'avg_humidity', 'rain'],
                     sort=False)

    data = data.reset_index()
    print("#### data : \n", data)

    data = data.drop(columns=['dh_utc'])
    
    scaler = MinMaxScaler()
    df_normalized = pd.DataFrame(scaler.fit_transform(data), columns=data.columns)

    print("df_normalized : \n ", df_normalized)

    return df_normalized

def getData():
    prediction.chargeModel()

    list_23 = []
    list_22 = []
    list_21 = []
    list_20 = []

    list_result = []

    db.connexion()
    df_pred = db.get30jours()
    df_avg_temp_2023, df_avg_press_2023, df_avg_hum_2023, df_avg_rain_2023 = db.getDataPerMonth(2023)
    df_avg_temp_2022, df_avg_press_2022, df_avg_hum_2022, df_avg_rain_2022 = db.getDataPerMonth(2022)
    df_avg_temp_2021, df_avg_press_2021, df_avg_hum_2021, df_avg_rain_2021 = db.getDataPerMonth(2021)
    df_avg_temp_2020, df_avg_press_2020, df_avg_hum_2020, df_avg_rain_2020 = db.getDataPerMonth(2020)
    db.close_connection()

    print("df_avg_temp_2020", df_avg_temp_2020)

    labels = df_avg_temp_2023['dh_utc'].astype(str).values.tolist()

    df_2020 = normalizeData(df_avg_temp_2020, df_avg_press_2020, df_avg_hum_2020, df_avg_rain_2020)
    df_2021 = normalizeData(df_avg_temp_2021, df_avg_press_2021, df_avg_hum_2021, df_avg_rain_2021)
    df_2022 = normalizeData(df_avg_temp_2022, df_avg_press_2022, df_avg_hum_2022, df_avg_rain_2022)
    df_2023 = normalizeData(df_avg_temp_2023, df_avg_press_2023, df_avg_hum_2023, df_avg_rain_2023)

    list_20.append(df_2020['avg_temperature'].astype(float).values.tolist())
    list_20.append(df_2020['avg_pressure'].astype(float).values.tolist())
    list_20.append(df_2020['avg_humidity'].astype(float).values.tolist())
    list_20.append(df_2020['rain'].astype(float).values.tolist())

    list_21.append(df_2021['avg_temperature'].astype(float).values.tolist())
    list_21.append(df_2021['avg_pressure'].astype(float).values.tolist())
    list_21.append(df_2021['avg_humidity'].astype(float).values.tolist())
    list_21.append(df_2021['rain'].astype(float).values.tolist())

    list_22.append(df_2022['avg_temperature'].astype(float).values.tolist())
    list_22.append(df_2022['avg_pressure'].astype(float).values.tolist())
    list_22.append(df_2022['avg_humidity'].astype(float).values.tolist())
    list_22.append(df_2022['rain'].astype(float).values.tolist())

    list_23.append(df_2023['avg_temperature'].astype(float).values.tolist())
    list_23.append(df_2023['avg_pressure'].astype(float).values.tolist())
    list_23.append(df_2023['avg_humidity'].astype(float).values.tolist())
    list_23.append(df_2023['rain'].astype(float).values.tolist())


    list_result.append(list_20)
    list_result.append(list_21)
    list_result.append(list_22)
    list_result.append(list_23)


    
    return prediction.predict(df_pred), labels, list_result

# Fonction pour obtenir les trois jours suivant le jour actuel
def jours_semaine_suivants():
    jours = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
    aujourdhui = datetime.now().weekday()
    jours_suivants = jours[aujourdhui:] + jours[:aujourdhui-1]
    return jours_suivants[:4]


jours_semaine = jours_semaine_suivants()
prediction, labels, liste = getData()

values = []

values.append(liste[0])
values.append(liste[1])
values.append(liste[2])
values.append(liste[3])

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