from urllib.parse import parse_qs
import hmac
import hashlib


class SlashCommandFactory:
    def __init__(self, sigining_secret=None):
        self.sigining_secret = sigining_secret

    def load_from_event(self, event):
        payload = parse_qs(event['body'])

        ts = event['headers']['X-Slack-Request-Timestamp']
        sig = event['headers']['X-Slack-Signature']
        body_raw = event['body']
        resp_url = payload['response_url'][0]
        name = payload['command'][0].lstrip('/')
        # 送られたコマンドに引数がない場合は、空文字のlistを加える
        params = payload['text'][0].split() if 'text' in payload else ['']

        return SlashCommand(body=body_raw, timestamp=ts,
                            signature=sig, response_url=resp_url,
                            name=name, params=params,
                            sigining_secret=self.sigining_secret)

    def load_from_state(self, state):
        resp_url = state['response_url']
        name = state['command']
        params = state['text']

        return SlashCommand(response_url=resp_url, name=name, params=params)


class SlashCommand:
    def __init__(self, body=None, timestamp=None, signature=None,
                 response_url=None, name=None, params=None,
                 sigining_secret=None, **args):
        self.body = body
        self.timestamp = timestamp
        self.signature = signature
        self.response_url = response_url
        self.name = name
        self.params = params
        self.sigining_secret = sigining_secret
        self.extra = args

    def verify_request(self):
        if (self.sigining_secret is None
                or self.signature is None
                or self.body is None
                or self.timestamp is None):
            return False

        req = str.encode('v0:' + self.timestamp + ':' + self.body)
        req_hash = 'v0=' + hmac.new(str.encode(self.sigining_secret),
                                    req,
                                    hashlib.sha256).hexdigest()

        return hmac.compare_digest(req_hash, self.signature)

    def dump_state(self):
        return {'response_url': self.response_url,
                'command': self.name,
                'text': self.params}
