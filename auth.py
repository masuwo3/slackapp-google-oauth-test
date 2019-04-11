import os
import hmac
import hashlib
import json
from urllib.parse import urlencode
from urllib.parse import urljoin
from urllib.parse import parse_qs

GOOGLE_CLIENT_ID = os.environ['GOOGLE_CLIENT_ID']
SLACK_SIGNING_SECRET = os.environ['SLACK_SIGNING_SECRET']

SCOPE = 'email'


def invoke(event, context):
    headers = event['headers']
    payload_raw = event['body']
    req_ctx = event['requestContext']

    # Slack Appから送られたリクエストかどうかを判別
    if not verify_request(headers, payload_raw, SLACK_SIGNING_SECRET):
        resp = json.dumps({"response_type": "ephemeral",
                           "text": "Request is Invalid."})

        return {'statusCode': 200, 'body': resp}

    payload = parse_qs(payload_raw)

    # 以降の処理にslash commandのパラメータをstateとして渡す
    state = {'response_url': payload['response_url'],
             'command': payload['command'],
             'text': payload['text'] if 'text' in payload else ['']}

    # API GatewayのContextからOAuth認証用のリダイレクトURLを作成
    redirect_uri = __redirect_uri(req_ctx)

    # slackのresponse_urlをリダイレクト後も参照できるようにstateに渡す
    oauth_link = __oauth_link(redirect_uri, state)

    body = {'text': '<{}|Googleアカウントでログイン>'.format(oauth_link)}

    return {"statusCode": 200,
            "body": json.dumps(body)}


def verify_request(headers, payload_raw, signing_secret):
    timestamp = headers['X-Slack-Request-Timestamp']
    signature = headers['X-Slack-Signature']

    req = str.encode('v0:' + timestamp + ':' + payload_raw)
    req_hash = 'v0=' + hmac.new(str.encode(signing_secret),
                                req,
                                hashlib.sha256).hexdigest()

    return hmac.compare_digest(req_hash, signature)


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
