import requests
import json
import time

# Make Strava auth API call with your 
# client_code, client_secret and code

response = requests.post(
                    url = 'https://www.strava.com/oauth/token',
                    data = {
                            'client_id': '120308',
                            'client_secret': '45f626c9f96b35ff47ad8226e90aee444b46845d',
                            'code': '811c3da0cbb2a0a93642bd311d452e8af1c694ec',
                            'grant_type': 'authorization_code'
                            }
                )

#Save json response as a variable
strava_tokens = response.json()
print(strava_tokens)

# Save tokens to file
with open('strava_tokens.json', 'w',encoding='utf-8') as outfile:
    json.dump(strava_tokens, outfile, indent = 4,ensure_ascii=False)

# Open JSON file and print the file contents 
# to check it's worked properly

with open('strava_tokens.json') as check:
  data = json.load(check)

# Get the tokens from file to connect to Strava
with open('strava_tokens.json') as json_file:
    strava_tokens = json.load(json_file)

# If access_token has expired then 
# use the refresh_token to get the new access_token
if strava_tokens['expires_at'] > time.time():
    print('El token expiro')
    # Make Strava auth API call with current refresh token    
    response = requests.post(
                        url = 'https://www.strava.com/oauth/token',
                        data = {
                                'client_id': '120308',
                                'client_secret': '45f626c9f96b35ff47ad8226e90aee444b46845d',
                                'grant_type': 'refresh_token',
                                'refresh_token': strava_tokens['refresh_token']
                                }
                    )# Save response as json in new variable
    new_strava_tokens = response.json()
    with open('new_strava_tokens.json', 'w',encoding='utf-8') as outfile:
        json.dump(new_strava_tokens, outfile, indent = 4,ensure_ascii=False)