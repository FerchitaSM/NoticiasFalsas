from sklearn.feature_extraction.text import CountVectorizer 
import io, base64, os, random
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
#%matplotlib inline
from mypackage.Conexion import conexion
import numpy as geek 

    


class clustering:
    # funciones de backend      
    def myclustering(dato):
        centroides = clustering.entrenamiento()
        clustering.graficas()
        return centroides


    def entrenamiento():
        global kmeans, centroides, df,col_names, myconexion
        num_clusters = 3
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
        kmeans = KMeans (n_clusters = num_clusters).fit(df)
        centroides = kmeans.cluster_centers_
        
        centroides_arr="Los centroides son: \n \t"
        centroides_round =np.around(centroides, decimals=2)
        for index in range(num_clusters):
            centroides_arr = centroides_arr+"Grupo de centroides numero "+str(index+1)+": "+ (geek.array_str(centroides_round[index]))+"\n \t"
        return centroides_arr


    def grafica (columna):

        #plt.scatter (centroides [:, 0], centroides [:, columna], c = 'red', s = 100)
        plt.scatter (df[col_names[0]], df[col_names[columna]], c = kmeans.labels_.astype (int), s = 30)
        plt.ylabel(col_names[columna])
        plt.xlabel(col_names[0])

        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        url= "static/images/plotp"+str(columna)+".txt"
        archivo = open(url, 'w')
        archivo.write(plot_url) 
        archivo.close()
        plt.clf()

    def graficas ():
        tamano= myconexion.tamano()-1
        for col in range(tamano):
           clustering.grafica(col+1)
        
