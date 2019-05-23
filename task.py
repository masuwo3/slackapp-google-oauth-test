import os
import json
import logging

import requests
from requests import HTTPError
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import AuthorizedSession

from code.log_util import setup_loglevel

TASK_QUEUE_ENDPOINT = os.environ['TASK_QUEUE_ENDPOINT']

setup_loglevel()
logger = logging.getLogger(__name__)


def invoke(event, context):
    logger.debug(json.dumps(event))

    for record in event['Records']:
        task_params = json.loads(record['body'])
        response_url = task_params['response_url']
        try:
            access_token = task_params['g_access_token']
            email = get_email(access_token)

            __post_response(response_url,
                            {'text': f'あなたのアドレスは {email} です。'})

            return 'ok'
        except HTTPError as e:
            logger.error(f"status code: {e.response.status_code}")
            logger.error(f"text: {e.response.text}")
            __post_response(response_url,
                            {'text': f'タスクに失敗しました : {e.response.text}'})
            raise e


def get_email(access_token):
    credentials = Credentials(access_token)
    session = AuthorizedSession(credentials)
    response = session.get('https://www.googleapis.com/oauth2/v1/userinfo')
    response.raise_for_status()

    return response.json()['email']


def __post_response(response_url, data):
    try:
        r = requests.post(response_url,
                          headers={'Content-Type': 'application/json'},
                          data=json.dumps(data))
        r.raise_for_status()
    except HTTPError as e:
        logger.error(f"status code: {e.response.status_code}")
        logger.error(f"text: {e.response.text}")
        raise e
