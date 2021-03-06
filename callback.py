import os
import json
import logging

import boto3
import requests
from requests import HTTPError
from requests_oauthlib import OAuth2Session

from code.slack import SlashCommandFactory
from code.log_util import setup_loglevel

GOOGLE_CLIENT_ID = os.environ['GOOGLE_CLIENT_ID']
GOOGLE_CLIENT_SECRET = os.environ['GOOGLE_CLIENT_SECRET']
TASK_QUEUE_ENDPOINT = os.environ['TASK_QUEUE_ENDPOINT']

setup_loglevel()
logger = logging.getLogger(__name__)


def invoke(event, context):
    logger.debug(json.dumps(event))

    query = event['queryStringParameters']
    state = json.loads(query['state'])
    c = SlashCommandFactory().load_from_state(state)

    code = query['code']
    redirect_uri = __redirect_uri(event['requestContext'])
    access_token = __get_access_token(code, redirect_uri)

    task_msg = {'command': c.name,
                'command_params': c.params,
                'g_access_token': access_token,
                'response_url': c.response_url}

    queue = boto3.resource('sqs').Queue(TASK_QUEUE_ENDPOINT)
    queue.send_message(MessageBody=json.dumps(task_msg))

    __post_response(c.response_url,
                    {'text': 'タスクを開始します。'})

    return {'statusCode': 200,
            'body': 'ok'}


def __get_access_token(code, redirect_uri):
    token_url = 'https://www.googleapis.com/oauth2/v4/token'

    try:
        sess = OAuth2Session(GOOGLE_CLIENT_ID, redirect_uri=redirect_uri)
        resp = sess.fetch_token(token_url, code=code,
                                client_secret=GOOGLE_CLIENT_SECRET)
    except HTTPError as e:
        logger.error(f"status code: {e.response.status_code}")
        logger.error(f"text: {e.response.text}")
        raise e

    logger.debug('Get below tokens.')
    logger.debug(json.dumps(resp))

    return resp['access_token']


def __post_response(response_url, data):
    try:
        requests.post(response_url,
                      headers={'Content-Type': 'application/json'},
                      data=json.dumps(data))
    except HTTPError as e:
        logger.error(f"status code: {e.response.status_code}")
        logger.error(f"text: {e.response.text}")
        raise e


def __redirect_uri(req_ctx):
    return 'https://' + req_ctx['domainName'] + req_ctx['path']
