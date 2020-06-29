import pandas as pd
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer 
from mypackage.Conexion import conexion


class prediccion:

    # funciones de backend
    def base_datos(dato):
        global text_data, y 
        myconexion = conexion()
        myconexion.conectar()
        x_list =myconexion.leer_dato(1)
        text_data = np.asarray(x_list)
        y_list=myconexion.leer_dato(7)
        y = np.asarray(y_list)


    def preparacion(dato):
        global names, x, y
        count_vector=CountVectorizer()
        count_vector.fit(text_data)
        names=count_vector.get_feature_names()
        doc_array=count_vector.transform(text_data).toarray()
        #x
        count = CountVectorizer()
        bag_of_words = count.fit_transform(text_data)
        x=bag_of_words.toarray()

        #frequency_matrix
        frequency_matrix=pd.DataFrame(data=doc_array,columns=names)
        
    def entrenamiento(dato):
        global model
        clf=MultinomialNB(alpha=1.0, class_prior=None, fit_prior=True)
        #Entrenamiento del Modelo
        model=clf.fit(x,y)
        
    def nuevo_texto(dato, titulo):
        #Nuevo texto
        new_data=np.array([titulo])
        count_vector=CountVectorizer()
        count_vector.fit(text_data)
        new_names=count_vector.get_feature_names()
        new_doc_array =count_vector.transform(new_data).toarray()
        #predecirmos en que clase (0 o 1) va a pertenecer dicho documento
        prediccion=model.predict(new_doc_array)
        pred = str(prediccion[0])
        return pred
