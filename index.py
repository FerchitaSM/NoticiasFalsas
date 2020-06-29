import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer 

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from flask import Flask, render_template, request, redirect, url_for, flash

from mypackage.Prediccion import prediccion
from mypackage.Conexion import conexion
from mypackage.Clustering import clustering
from mypackage.Svc import svc



def mysvc():
    mysvc = svc()
    mysvc.entrenamiento()

def myclustering():
    myclustering = clustering()
    centroides = myclustering.myclustering()
    return centroides

def prediccion_titulo(titulo):
    myprediccion = prediccion()
    myprediccion.base_datos()
    myprediccion.preparacion()
    myprediccion.entrenamiento()
    prediccion_new = myprediccion.nuevo_texto(titulo) 

    return prediccion_new

def guardar_nuevo_dato(titulo,origen,date,vistos,red,comentarios,tipo):
    myconexion = conexion()
    myconexion.conectar()
    myconexion.escribir_dato(titulo,origen,date,vistos,red,comentarios,tipo)
   

app = Flask(__name__)

@app.route('/')
def Detector():
    return render_template('detector.html')

@app.route('/noticia', methods=['POST'])
def Noticia():
    titulo = ""
    origen=""
    date=""
    if request.method == 'POST':
        titulo = request.form['titulo']
        origen = request.form['origen']
        date = request.form['date']
        vistos = request.form['vistos']
        red = request.form['red']
        comentarios = request.form['comentarios']
        prediccion_new = prediccion_titulo(titulo)
        guardar_nuevo_dato(titulo,origen,date,vistos,red,comentarios,prediccion_new)
        flash(prediccion_new)
    return redirect(url_for('Detector'))

@app.route('/clustering')
def Clustering():
    centroides= myclustering()
    flash(centroides)
    return render_template('clustering.html')

@app.route('/svm')
def Svc():
    mysvc()
    return render_template('svc.html')

@app.route('/about')
def About():
    return render_template('about.html')

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = True
    app.run(port = 3000)




from flask import send_file, current_app as app

@app.route('/show/static-pdf/')
def show_static_pdf():
    with open('/path/of/file.pdf', 'rb') as static_file:
        return send_file(static_file, attachment_filename='file.pdf')



