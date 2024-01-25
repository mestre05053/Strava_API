import requests
import webbrowser
import re 
import time
from strava_django.entities.auth import Auth

auth = Auth()

def test():
   ''' base_url = 'http://www.strava.com/oauth/authorize'
    params = {
            "client_id": auth.client_id,
            "response_type": "code",
            "redirect_uri" :    "http://localhost/exchange_token",
            "approval_prompt": "force",
            "scope" : "profile:read_all,activity:read_all",
        }
        
    oauth_url = auth.sacar_afuera()
    response = requests.get(oauth_url)
    print(response.status_code)
    webbrowser.open_new_tab(oauth_url)
    time.sleep(7)
    list_codes =  []
    with open('/var/log/apache2/access.log') as fp:
        for entry in fp:
            list_codes.append(re.findall('(?<=code=)[A-Za-z0-9]{1,}', entry))
        code = list_codes[-1]
    print('Code:', *code)'''
   auth.get_token()

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
