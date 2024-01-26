
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
        Esta funcion abre el navegador con al URL acceso a los datos de privados de usuario, luego le de 
        los logs de APACHE el codigo que devuelve Strava y llama a funcion que intercambia el CODE por el TOKEN        
        '''
        global code
        webbrowser.open_new_tab(Auth.__url_app_verificacion)
        time.sleep(7)
        list_codes =  []
        with open('/var/log/apache2/access.log') as fp:
            for entry in fp:
                list_codes.append(re.findall('(?<=code=)[A-Za-z0-9]{1,}', entry))
            code = list_codes[-1]

        self.__exchange_code_for_access_token(code)

    def __refresh_token(self):
        '''
        Esta funcion refresca el TOKEN en caso de haya expirado, si expiro solicita
        nuevamente el TOKEN.
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
        Esta funcion recibe el CODE como parametro y lo intercambien por el TOKEN y llama a la funcion 
        que guarda en un JSON el TOKEN de acceso, de refresco y el tiempo en que expira.
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