import requests
import json

from strava_django.entities.auth import Auth

auth = Auth()

def run():
   auth.get_token()

class User_Data():
    
    def __init__(self):
        self.__auth = Auth()
        self.__token = self.__auth.get_token()
        self.__list_activities = {}
        self.__request_page_num = 1
        self.__per_page = 200
        self.__params = {
                        'per_page' : self.__per_page,
                        'page' : self.__request_page_num,
                        }
        self.__headers = {
                        'Authorization': f'Bearer {self.__token}',
                        "Accept": "application/json"
                        }
        self.__urls = {
            "base_url":     "https://www.strava.com/api/v3/",
            "activities":   "activities",
            "segments":     "/segments/26116938/starred",
            "alejandro" :   "athletes/26116938", ##Es mi id de strava
        }

        ## Funciones del constructor
        #self.__get_user_data()
        self.__get_user_activities()

    def __get_user_data(self):
        response = requests.get(self.__urls['base_url']+self.__urls['alejandro'], headers=self.__headers)

    def __get_user_activities(self):
        
        while True:
            
            response = requests.get(self.__urls['base_url']+self.__urls['activities'], headers=self.__headers, params=self.__params)
            print("Descargando pagina: ",self.__params['page'] )
            print(response.url)
            
            if response.json() == []:
                print("breaking out of while loop because the response is zero, which means there must be no more activities")
                break
            count = 0
            average_watts = 0
            for i in response.json():
                name = i['name']
                if 'type' in i:
                    type = i['type']
                start_date = i['start_date']
                location_country = i['location_country']
                start_latlng = i['start_latlng']
                end_latlng = i['end_latlng']
                distance = i['distance']/1000
                moving_time = i['moving_time']/60
                total_elevation_gain = i['total_elevation_gain']
                if 'average_watts' in i:
                    average_watts = i['average_watts']
                average_speed = i['average_speed']*3.6
                max_speed = i['max_speed']
                if 'average_heartrate' in i:
                    average_heartrate = i['average_heartrate']
                if 'max_heartrate' in i:
                    max_heartrate = i['max_heartrate']
                if 'elev_high' in i:
                    elev_high = i['elev_high']
                if 'elev_low' in i:
                    elev_low = i['elev_low']
                if 'map' in i:
                    map = i['map']
                    self.__list_activities[name] = [{
                                        'Tipo':type, 
                                        'Fecha':start_date, 
                                        'Pais':location_country, 
                                        'Latitud inicial':start_latlng, 
                                        'Latitud final':end_latlng, 
                                        'Distancia':distance, 
                                        'Tiempo en movimiento':moving_time,
                                        'Elevación acumulada':total_elevation_gain,
                                        'Potencia promedio': average_watts,
                                        'Velocidad promedio':average_speed,
                                        'Velocidad máxima':max_speed,
                                        'Ritmo cardiaco promedio':average_heartrate,
                                        'Ritmo cardiaco máximo':max_heartrate,
                                        'Elevación máxima':elev_high,
                                        'Elevación mínima':elev_low,
                                        'Mapa':map,
                                        }]
                
            self.__params['page'] += 1
            print('Lista de actividades',len(self.__list_activities))
            count = len(self.__list_activities)
            with open("user_activities.json", "w",encoding='utf-8') as outfile:
                json.dump({
                        "Total de actividades":count,
                        "Actividades":self.__list_activities,
                        }, outfile, indent = 4,ensure_ascii=False)
            
                
            

