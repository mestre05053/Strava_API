import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

swagger_client.Configuration().access_token = '7505e3cd9f679aa67a3422ac3c5dd57cee6673d8'
# Configure OAuth2 access token for authorization: strava_oauth
configuration = swagger_client.Configuration()

# create an instance of the API class
api_instance = swagger_client.ActivitiesApi(swagger_client.ApiClient(configuration))
id = 56 # int | The identifier of the activity.
page = 56 # int | Page number. (optional)
per_page = 30 # int | Number of items per page. Defaults to 30. (optional) (default to 30)

try:
    # List Activity Kudoers
    api_response = api_instance.get_kudoers_by_activity_id(id, page=page, per_page=per_page)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ActivitiesApi->get_kudoers_by_activity_id: %s\n" % e)