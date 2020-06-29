import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

class conexion:
    # funciones de backend
    def conectar(dato):
        global scope, creds, client, sheet
        # use creds the Google Drive API
        scope = ['https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
        client = gspread.authorize(creds)
        sheet = client.open("noticias").sheet1

    def escribir_dato(dato,titulo,origen,date,vistos,red,comentarios,tipo):
        separador = "/"
        separado = date.split(separador)
        dateint = int(separado[0])+ int(separado[1])+ int(separado[2]) -2000


        row = [titulo,origen,dateint,vistos,red,comentarios,tipo]
        index = sheet.row_count
        sheet.insert_row(row, index)

    def leer_dato(dato, indexcol):
        cols= sheet.col_values(indexcol)
        return cols

    def tamano(dato):
        cols= 6
        return cols



