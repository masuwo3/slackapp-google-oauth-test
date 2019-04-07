import os
import hmac
import hashlib
import json
from urllib.parse import urlencode
from urllib.parse import urljoin

GOOGLE_CLIENT_ID = os.environ['GOOGLE_CLIENT_ID']
SLACK_SIGNING_SECRET = os.environ['SLACK_SIGNING_SECRET']

SCOPE = 'email'


def invoke(event, context):
    headers = event['headers']
    body_raw = event['body']

    if not verify_request(headers, body_raw, SLACK_SIGNING_SECRET):
        resp = json.dumps({
                    "response_type": "ephemeral",
                    "text": "Request is unverified."})
        return {'statusCode': 200, 'body': resp}

    domain = event['requestContext']['domainName']
    path = event['requestContext']['path']
    redirect_uri = urljoin('https://' + domain + path, 'callback')

    return {"statusCode": 200,
            "body": json.dumps({
                        "text": __oauth_link(redirect_uri)})}


def __oauth_link(redirect_uri, state=None):
    url = 'https://accounts.google.com/o/oauth2/v2/auth?'
    query = {'client_id': GOOGLE_CLIENT_ID,
             'redirect_uri': redirect_uri,
             'scope': SCOPE,
             'response_type': 'code'}

    if state:
        query['state'] = state

    return url + urlencode(query)


def verify_request(headers, body, signing_secret):
    timestamp = headers['X-Slack-Request-Timestamp']
    signature = headers['X-Slack-Signature']

    req = str.encode('v0:' + timestamp + ':' + body)
    req_hash = 'v0=' + hmac.new(str.encode(signing_secret),
                                req,
                                hashlib.sha256).hexdigest()

    return hmac.compare_digest(req_hash, signature)
