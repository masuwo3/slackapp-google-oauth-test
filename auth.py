import os
import json
from urllib.parse import urlencode
from urllib.parse import urljoin

from code.slack import SlashCommand

GOOGLE_CLIENT_ID = os.environ['GOOGLE_CLIENT_ID']
SLACK_SIGNING_SECRET = os.environ['SLACK_SIGNING_SECRET']

SCOPE = 'email'


def invoke(event, context):
    command = SlashCommand(SLACK_SIGNING_SECRET)
    command.load_event(event)

    req_ctx = event['requestContext']

    # Slack Appから送られたリクエストかどうかを判別
    if not command.verify_request():
        resp = json.dumps({"response_type": "ephemeral",
                           "text": "Request is Invalid."})

        return {'statusCode': 200, 'body': resp}

    # API GatewayのContextからOAuth認証用のリダイレクトURLを作成
    redirect_uri = __redirect_uri(req_ctx)

    # slackのresponse_urlをリダイレクト後も参照できるようにstateに渡す
    oauth_link = __oauth_link(redirect_uri, command.dump_state())

    body = {'text': '<{}|Googleアカウントでログイン>'.format(oauth_link)}

    return {"statusCode": 200,
            "body": json.dumps(body)}


def __oauth_link(redirect_uri, state=None):
    url = 'https://accounts.google.com/o/oauth2/v2/auth?'
    query = {'client_id': GOOGLE_CLIENT_ID,
             'redirect_uri': redirect_uri,
             'scope': SCOPE,
             'response_type': 'code'}

    if state:
        query['state'] = json.dumps(state)

    return url + urlencode(query)


def __redirect_uri(req_ctx):
    this_uri = 'https://' + req_ctx['domainName'] + req_ctx['path']
    return urljoin(this_uri, 'callback')
