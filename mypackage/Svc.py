from sklearn.feature_extraction.text import CountVectorizer 
import io, base64, os, random, sys
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
#%matplotlib inline
from mypackage.Conexion import conexion
import numpy as geek 

from sklearn import svm
from sklearn.model_selection import train_test_split, GridSearchCV
import requests


class svc:


    def entrenamiento(dato):
        global df,col_names, myconexion
        col_names = ['estado','origen','date','vistos','red','comentarios']
        myconexion = conexion()
        myconexion.conectar()
        tamano= myconexion.tamano()
        matrix = []
        columna=(myconexion.leer_dato(tamano+1))
        matrix.append(columna) 
        for col in range(tamano-1):
            columna=(myconexion.leer_dato(col+2))
            matrix.append(columna) 

        doc_array = np.asarray(matrix)
        doc_array=doc_array.transpose()
        df= pd.DataFrame(data=doc_array, columns = col_names)

        print(df)
        for i in range(3):
            svc.entrenamientoIndividual(df, 1, (i+3))

    def entrenamientoIndividual(df, indexa, indexb):
        global w,a,x,y,b,y_abajo,y_arriba, model
        #ingredientes_receta
        ingredientes = df[[col_names[indexa],col_names[indexb]]].values
        type_label =  df[[col_names[0]]].values
        #Entrenando
        model = svm.SVC(kernel='linear')
        model.fit(ingredientes, type_label)
        w = model.coef_[0]
        a = -w[0] / w[1]
        x = np.linspace(0, 10)
        y = a * x - (model.intercept_[0]) / w[1]
        b = model.support_vectors_[0]
        y_abajo = a * x + (b[1] - a * b[0])
        b = model.support_vectors_[-1]
        y_arriba = a * x + (b[1] - a * b[0])
    
        print('El entrenamiento se realizo con exito!')    
        svc.grafica (df, indexa, indexb)   
    
    def grafica (df, indexa, indexb):  
        plt.clf()
        sns.lmplot(col_names[indexa], col_names[indexb], data=df, hue='estado', palette='Set3', fit_reg=False, scatter_kws={"s": 100})
        plt.plot(x, y, 'k--')
        plt.plot(x, y_abajo, 'k--')
        plt.plot(x, y_arriba, 'k--')
        plt.title('Fronteras y limites del vector de soporte')
        plt.scatter(model.support_vectors_[:, 0], model.support_vectors_[:, 1], s=80, facecolors='none');     

        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        url= "static/images/svcplotd"+str(indexb) +".txt"
        archivo = open(url, 'w')
        archivo.write(plot_url) 
        archivo.close()
        plt.clf()

        
