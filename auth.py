import os
import json
from urllib.parse import urljoin

from requests_oauthlib import OAuth2Session

from code.slack import SlashCommandFactory

GOOGLE_CLIENT_ID = os.environ['GOOGLE_CLIENT_ID']
SLACK_SIGNING_SECRET = os.environ['SLACK_SIGNING_SECRET']

SCOPE = ['email']


def invoke(event, context):
    command = SlashCommandFactory(SLACK_SIGNING_SECRET).load_from_event(event)

    # Slack Appから送られたリクエストかどうかを判別
    if not command.verify_request():
        resp = json.dumps({"response_type": "ephemeral",
                           "text": "Request is Invalid."})

        return {'statusCode': 200, 'body': resp}

    # API GatewayのContextからOAuth認証用のリダイレクトURLを作成
    redirect_uri = __redirect_uri(event['requestContext'])

    # slackのresponse_urlをリダイレクト後も参照できるようにstateに渡す
    oauth_link = __oauth_link(redirect_uri, command.dump_state())

    body = {'text': '<{}|Googleアカウントでログイン>'.format(oauth_link)}

    return {"statusCode": 200,
            "body": json.dumps(body)}


def __oauth_link(redirect_uri, state=None):
    auth_base_url = 'https://accounts.google.com/o/oauth2/v2/auth?'
    _state = json.dumps(state) if state else None

    sess = OAuth2Session(GOOGLE_CLIENT_ID, scope=SCOPE,
                         redirect_uri=redirect_uri)
    auth_url, _ = sess.authorization_url(auth_base_url, state=_state)

    return auth_url


def __redirect_uri(req_ctx):
    this_uri = 'https://' + req_ctx['domainName'] + req_ctx['path']
    return urljoin(this_uri, 'callback')
