import os
import json

import requests
from requests import HTTPError

GOOGLE_CLIENT_ID = os.environ['GOOGLE_CLIENT_ID']
GOOGLE_CLIENT_SECRET = os.environ['GOOGLE_CLIENT_SECRET']


def invoke(event, context):
    q = event['queryStringParameters']
    print('query: {}'.format(q))

    code = q['code']

    state = json.loads(q['state'])
    print('state: {}'.format(state))

    response_url = state['response_url'][0]
    print('resp_url: {}'.format(response_url))

    redirect_uri = __redirect_uri(event['requestContext'])
    data = {'code': code,
            'client_id': GOOGLE_CLIENT_ID,
            'client_secret': GOOGLE_CLIENT_SECRET,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code'}

    try:
        # codeをaccess tokenに変換する
        r = requests.post('https://www.googleapis.com/oauth2/v4/token',
                          data=data)

        r.raise_for_status()
        access_token = r.json()['access_token']

        # access tokenを使ってGoogle APIからemailを取得する
        rr = requests.get('https://www.googleapis.com/oauth2/v1/userinfo',
                          headers={'Authorization': 'Bearer ' + access_token})
        rr.raise_for_status()
        email = rr.json()['email']

        # emailをslackのresponse_urlに送る
        rrr = requests.post(response_url,
                            headers={'Content-Type': 'application/json'},
                            data=json.dumps({'text': f'あなたのメールアドレスは {email}'}))

        rrr.raise_for_status()
    except HTTPError as e:
        print(f"status code: {e.response.status_code}")
        print(f"text: {e.response.text}")
        raise e

    return {"statusCode": 200,
            "body": 'ok'}


def __redirect_uri(req_ctx):
    return 'https://' + req_ctx['domainName'] + req_ctx['path']
