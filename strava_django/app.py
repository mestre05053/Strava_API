import requests, json
from strava_django.entities.auth import Auth

auth = Auth()
#token = auth.get_token()
# TO DO esta puesto esto aqui para evitar que de error con los headers
token = 0

def test():
    oauth_url = auth.sacar_afuera()
    print(oauth_url)
    response = requests.post(oauth_url)
    print(response)

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
