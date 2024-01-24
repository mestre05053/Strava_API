import requests
import webbrowser
import os

def get_code():
    
    code_url = 'http://www.strava.com/oauth/authorize?client_id=120308&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=profile:read_all,activity:read_all'
    response = requests.get(code_url, allow_redirects=False, timeout=10)
    print(response.status_code)
    webbrowser.open_new_tab(code_url)
    code_reponse = requests.get(code_url)
    print(code_reponse.history)
    print(code_reponse.url)
    #new_url = requests.get(response.headers['Location'])
    #new_url = requests.get(response.headers)
    if code_reponse.history:
        print("Request was redirected")
        for resp in response.history:
            print(resp.status_code, resp.url)
        print("Final destination:")
        print(response.status_code, response.url)  

    callback_url = 'http://localhost/exchange_token?state=&code=59cc430d2c4f8774feb8290a8be804077877f09f&scope=read,activity:read_all,profile:read_all'
    params = {      
                    "state" : "",
                    'exchange_token' : "",
                    'scope' : ""
                    }
    
    callback_response = requests.get(callback_url, allow_redirects=False, timeout=200, params=params)
    print(callback_response.headers.)
    
    

    print(os.environ.get("code", "No Query String in url"))
get_code()