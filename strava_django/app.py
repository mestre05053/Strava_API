import requests
import webbrowser
import json
from strava_django.entities.auth import Auth

import os
import binascii
import urllib.parse

from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer

auth = Auth()
#token = auth.get_token()
# TO DO esta puesto esto aqui para evitar que de error con los headers
token = 0

state = binascii.hexlify(os.urandom(20)).decode('utf-8')

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global code
        self.close_connection = True
        query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        '''if not query['state'] or query['state'][0] != state:
            raise RuntimeError("state argument missing or invalid")'''
        code = query['code']
        print(code)

def test():
    base_url = 'http://www.strava.com/oauth/authorize'
    params = {
            "client_id": auth.client_id,
            "response_type": "code",
            "redirect_uri" :    "http://localhost/exchange_token",
            "approval_prompt": "force",
            "scope" : "profile:read_all,activity:read_all",
            "state" : state
        }

    #response = requests.get(base_url, params=params)
    #print(response.url)

    oauth_url = auth.sacar_afuera()
    response = requests.get(oauth_url)
    print(response.status_code)
    webbrowser.open_new_tab(oauth_url)

    server = HTTPServer(('localhost', 8081), RequestHandler)
    server.handle_request()

def get_user_data():

    base_url = 'https://www.strava.com/api/v3/'
    alejandro = '26116938' ##Es mi id de strava
    francisco = '96558356' ##Es mi id de strava
    athletes = '/athletes/'
    activities = '/athlete/activities'
    segments = '/segments/26116938/starred'


    headers = {
                        'Authorization': f'Bearer {token}',
                        "Accept": "application/json"
                        }

    response = requests.get(base_url+athletes+alejandro, headers=headers)
    #response = requests.get(base_url+segments, headers=headers)

    print(response.json())
