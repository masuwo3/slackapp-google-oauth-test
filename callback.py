import os
import requests
from requests import HTTPError

GOOGLE_CLIENT_ID = os.environ['GOOGLE_CLIENT_ID']
GOOGLE_CLIENT_SECRET = os.environ['GOOGLE_CLIENT_SECRET']


def invoke(event, context):
    q = event['queryStringParameters']
    code = q['code']

    domain = event['requestContext']['domainName']
    path = event['requestContext']['path']
    redirect_uri = 'https://' + domain + path

    data = {'code': code,
            'client_id': GOOGLE_CLIENT_ID,
            'client_secret': GOOGLE_CLIENT_SECRET,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code'}

    try:
        r = requests.post('https://www.googleapis.com/oauth2/v4/token',
                          data=data)

        r.raise_for_status()
        access_token = r.json()['access_token']

        rr = requests.get('https://www.googleapis.com/oauth2/v1/userinfo',
                          headers={'Authorization': 'Bearer ' + access_token})
        email = rr.json()['email']
    except HTTPError as e:
        print(r.text)
        raise e

    return {"statusCode": 200,
            "body": email}
