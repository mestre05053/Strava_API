
import datetime
import json
import os
import webbrowser
import requests
import re
import time

# Singleton que carga de fichero json los secret
from strava_django.entities.config import cfg_item

code = None

class Auth:
    '''
    La clase AUTH define las funciones y variables necesarias para autenticar contra la API de STRAVA.
    Lo hace mediante OAUTH, se le envia a la API un solicitud el ID de la aplicacion para que esta te devuelve u
    un CODE para obtener acceso a los datos de un atleta, la API te devuelve un CODE que debes intercambiar por
    un TOKEN.  
    '''
    __auth_file = 'f_token.json'
    __client_id = cfg_item('client_id')
    __client_secret = cfg_item('client_secret')
    __url_app_verificacion = cfg_item('url_app_verificacion')

    def __init__(self):
        self.__data = None
        
    def get_token(self):
        '''
        Esta funcion verifica si exite ya el fichero con los token, sino existe llama a la funcion que los crea
        igualmente verifica si el token expiro, si expiro lo vuelve a solicitar.        
        '''
        if not os.path.isfile(Auth.__auth_file):
            print('no esta el f_token')
            self.__generate_token()
        else:
            self.__load_token_from_file()
            if not self.__data.get('token', ''):
                self.__generate_token()
            else:
                now = datetime.datetime.now()
                if now > datetime.datetime.fromisoformat(self.__data['expires']):
                    if self.__data['refresh_token']:
                        self.__refresh_token()
                    else:
                        self.__generate_token()

        return self.__data['token']

    def __generate_token(self):
        '''
        La APP de Strava en la configuracion te redirige al localhost, pero no permite poner un puerto especifico, 
        por esta razon no funciona levantar un servidor con Python en un puerto especifico, para que escuche una peticion
        reciba el CODE y se cierre. Tampoco lo puedo levantar en el el puerto 80 pq entra en conflicto con el APACHE.
        Esta funcion abre el navegador con la URL de acceso a los datos de privados de usuario, luego con una expresion
        regular lee de busca en el LOG de APACHE entrada que comiencen con la palabra y luego captura todos los 32 caracteres 
        siguientes que forman parte de CODE.
        '''
        global code
        webbrowser.open_new_tab(Auth.__url_app_verificacion)
        time.sleep(7)
        list_codes =  []
        with open('/var/log/apache2/access.log') as fp:
            for entry in fp:
                list_codes.append(re.findall('(?<=code=)[A-Za-z0-9]{1,}', entry))
            code = list_codes[-1]
            print('Code:',*code)

        self.__exchange_code_for_access_token(code)

    def __refresh_token(self):
        '''
        Esta funcion refresca el TOKEN enviando a la API un request.post con el ID de y el SECRET y el TOKEN de refresco 
        del cliente luego llama a la funcion que guarda en un JSON el TOKEN de acceso, de refresco y el tiempo en que expira.
        en caso de haya expirado, solicita nuevamente el TOKEN.
        '''
        data = {
                'client_id': Auth.__client_id,
                'client_secret': Auth.__client_secret,
                'grant_type': 'refresh_token',
                'refresh_token': self.__data['refresh_token'],
                }

        url = 'https://www.strava.com/oauth/token',

        response = requests.post(url, data=data)

        if response:
            response_json = response.json()
            self.__save_token_to_file(response_json["access_token"], '', response_json['expires_in'])
            self.__load_token_from_file()
        else:
            raise Exception(f"Could Not Get Token... {response.status_code} = {response.content}")

    def __exchange_code_for_access_token(self, code=None):
        '''
        Esta funcion recibe el CODE como parametro y lo intercambien por el TOKEN 
        enviando a la API un request.post con el ID de y el SECRET del cliente luego
        llama a la funcion que guarda en un JSON el TOKEN de acceso, de refresco y el tiempo en que expira.
        '''
        data = {
                'client_id': Auth.__client_id,
                'client_secret': Auth.__client_secret,
                'code': code,
                'grant_type': 'authorization_code',
        }
        url = 'https://www.strava.com/oauth/token'

        response = requests.post(url, data=data)
        response_json = response.json()

        if response:
            self.__save_token_to_file(response_json["access_token"], response_json["refresh_token"], response_json['expires_in'])
            self.__load_token_from_file()
        else:
            raise Exception(f"Could Not Get Token... {response.status_code} = {response.content}")

    def __save_token_to_file(self, token, refresh_token, expires_in):
        '''
        Esta funcion salva en un JSON el TOKEN de acceso, de refresco y el tiempo en que expira.
        '''
        expires = datetime.datetime.now() + datetime.timedelta(seconds = expires_in)
        with open(Auth.__auth_file, 'w') as file:
            json.dump({"token":token, "refresh_token":refresh_token, "expires": expires.isoformat()},file, indent= 4)

    def __load_token_from_file(self):
        '''
        Esta funcion carga del un JSON el TOKEN de acceso, de refresco y el tiempo en que expira y lo mete a la variable data.
        '''
        with open(Auth.__auth_file, 'r') as file:
            self.__data = json.load(file)