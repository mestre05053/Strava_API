import requests

from strava_django.entities.auth import Auth

auth = Auth()

def run():
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
