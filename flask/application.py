from flask import Flask
from flask import url_for
from flask import render_template
from datetime import datetime, timedelta
from markupsafe import escape

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello there'

# Fonction pour obtenir les trois jours suivant le jour actuel
def jours_semaine_suivants():
    jours = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
    aujourdhui = datetime.now().weekday()
    jours_suivants = jours[aujourdhui:] + jours[:aujourdhui-1]
    return jours_suivants[:4]

# Route pour afficher la météo
@app.route('/meteo')
def meteo():
    jours_semaine = jours_semaine_suivants()

    return render_template('index.html', jours_semaine=jours_semaine)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)