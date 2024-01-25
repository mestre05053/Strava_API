import requests
import webbrowser
import time
from urllib.parse import urlparse
from urllib.parse import parse_qs

def get_code():
    
    code_url = 'http://www.strava.com/oauth/authorize?client_id=120308&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=profile:read_all,activity:read_all'
    response = requests.get(code_url, allow_redirects=False, timeout=10)
    print(response.status_code)
    webbrowser.open_new_tab(code_url)
    code_reponse = requests.get(code_url)
    print(code_reponse.history)
    print(code_reponse.url)

    ### TODO
    #Buscar como hacer patra que se capture una url que tiene un parametro desconocido 
    #O buscar que se capture una URL aleatori 
    #callback_url = 'http://localhost/exchange_token?state=&code=59cc430d2c4f8774feb8290a8be804077877f09f&scope=read,activity:read_all,profile:read_all'
    callback_url = 'http://localhost/'+'exchange_token?state=&code='
    params = {      
                    "state" : "",
                    'exchange_token' : "",
                    'scope' : ""
                    }
    time.sleep(5)
    #parsed_url = urlparse(callback_url)
    #captured_value = parse_qs(parsed_url.query)['code'][0]
    #print(captured_value)

    callback_response = requests.get(callback_url, allow_redirects=False, timeout=200, params=params)
    print(callback_response.content)

get_code()