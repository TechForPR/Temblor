import pandas as pd
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import re
import os
import httplib2

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = 'creds/secreto_cliente.json'
APPLICATION_NAME = 'Temblor'

def get_credentials():
    """Gets valid user credentials from storage.
    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.
    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(
        credential_dir,
        'sheets.googleapis.com-python-quickstart.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def get_Data_temblor():
    """Shows basic usage of the Sheets API.
    Creates a Sheets API service object and prints the names and majors of
    students in a sample spreadsheet:
    https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets',
                              'v4',
                              http=http,
                              discoveryServiceUrl=discoveryUrl)
    # Acopio de Ayuda Optima
    # Para descargar otras páginas cambiar el nombre en el campo range
    result = service.spreadsheets().values().get(
        spreadsheetId='1C7qvWM0o3u5pdFJhnvQosK_3l-VGyZWTZ0JvOtOgPp0',
        range='4/10 Acopio CDMX!A7:z96').execute()
    values = result.get('values', [])
    if not values:
        print('No data found.')
    else:
        return values


def insert_Data_temblor(datos):
    """Shows basic usage of the Sheets API.
    Creates a Sheets API service object and prints the names and majors of
    students in a sample spreadsheet:
    https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets',
                              'v4',
                              http=http,
                              discoveryServiceUrl=discoveryUrl)
    result = service.spreadsheets().values().get(
        spreadsheetId='1wLHf5ITtTsfErWoPHwhu7Vfy-96eQKKxZO2AmZbP9XY',
        range='Datos!A1:H10000').execute()
    values = result.get('values', [])
    if not values:
        print('No data found.')
    else:
        print(values)


def estructura_sheet(listas):
    columnas = listas[0]
    info = pd.DataFrame()
    for lista in listas:
        dicc_aux = {}
        for col in range(len(lista)):
            dicc_aux[columnas[col]] = lista[col]
        info = info.append(dicc_aux, ignore_index=True)
    return info

if __name__ == '__main__':

    data = get_Data_temblor()
    unificando = estructura_sheet(data)

    Descripcion = unificando['DESCRIPCIÓN'].tolist()
    Del_Ent = unificando['DELEGACIÓN'].tolist()
    Colonia = unificando['COLONIA '].tolist()
    Referencia = unificando['Lugar de REFERENCIA'].tolist()
    Direccion = unificando['DIRECCIÓN'].tolist()
    Hora_Atencion = unificando['HORARIOS DE ATENCIÓN'].tolist()
    Transporte = unificando['REQ TRANSPORTE PARA MOVER VÍVERES A OTRO LUGAR'].tolist()
    Viveres = unificando['Mandan víveres hacia '].tolist()
    Salidas = unificando['Horarios de salidas'].tolist()
    Necesitan = unificando['NECESITAN'].tolist()
    Ex_Viveres = unificando['OFRECEN VÍVERES A QUIEN LO NECESITEN LOCALMENTE O PARA TRANSPORTAR'].tolist()
    Fechas = unificando['FECHAS 19s'].tolist()
    s19 = unificando['s19 POR FAVOR NO MODIFICAR'].tolist()
    latitud = unificando['LAT '].tolist()
    longitud = unificando['LONG '].tolist()


    unif = pd.DataFrame ({
    'Descripcion':Descripcion,
    'Delegacion/Entidad Federativa':Del_Ent,
    'Colonia':Colonia,
    'Lugar de Referencia':Referencia,
    'Direccion':Direccion,
    'Horarios de atencion ':Hora_Atencion,
    'Requiere transporte para mover viveres a otro lugar':Transporte,
    'Mandan viveres hacia':Viveres,
    'Horarios de salida': Salidas,
    'Necesitan':Necesitan,
    'Exceso de viveres':Ex_Viveres,
    'Fechas':Fechas,
    's19': s19,
    'Latitud': latitud,
    'Longitud': longitud,
    })

    unif_l = unif[unif.s19.isnull() == False]

    unif_l = unif_l[unif.s19.isnull() == False]
    del unif_l['s19']
    unif_l = unif_l.iloc[1:]

    unif_l.to_csv('acopio_ayuda_optima.csv')
