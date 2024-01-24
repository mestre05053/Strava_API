import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

swagger_client.ApiClient()
# Configure OAuth2 access token for authorization: strava_oauth
configuration = swagger_client.Configuration()
configuration.access_token = '7505e3cd9f679aa67a3422ac3c5dd57cee6673d8' 
'''swagger_client.configuration.access_token = '16ba0f4b0dc26de9fc1e521979c1f2ae06910c0f'
swagger_client.'''
'''
# create an instance of the API class
#api_instance = swagger_client.ActivitiesApi()
api_instance = swagger_client.ApiClient()
id = 789 # Long | The identifier of the activity.
includeAllEfforts = True # Boolean | To include all segments efforts. (optional)

try: 
    # Get Activity
    api_response = api_instance.getActivityById(id, includeAllEfforts=includeAllEfforts)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ActivitiesApi->getActivityById: %s\n" % e)

'''
id = 34 # Long | The identifier of the activity.
include_all_efforts = True # bool | To include all segments efforts. (optional)
api_instance = swagger_client.ActivitiesApi(swagger_client.ApiClient(configuration))
try:
    # Get Activity
    api_response = api_instance.get_activity_by_id(id, include_all_efforts=include_all_efforts)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ActivitiesApi->get_activity_by_id: %s\n" % e)




