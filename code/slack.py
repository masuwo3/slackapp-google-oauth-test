from urllib.parse import parse_qs
import hmac
import hashlib


class SlashCommand:
    def __init__(self, sigining_secret):
        self.secret = sigining_secret

    def load_event(self, event):
        headers = event['headers']
        payload_raw = event['body']
        payload = parse_qs(payload_raw)

        self.timestamp = headers['X-Slack-Request-Timestamp']
        self.signature = headers['X-Slack-Signature']
        self.payload_raw = payload_raw
        self.response_url = payload['response_url'][0]
        self.command_name = payload['command'][0].lstrip('/')
        # 引数がない場合は、空文字のlistを加える
        self.params = payload['text'][0].split() if 'text' in payload else ['']

    def verify_request(self):
        req = str.encode('v0:' + self.timestamp + ':' + self.payload_raw)
        req_hash = 'v0=' + hmac.new(str.encode(self.secret),
                                    req,
                                    hashlib.sha256).hexdigest()

        return hmac.compare_digest(req_hash, self.signature)

    def dump_state(self):
        return {'response_url': self.response_url,
                'command': self.command_name,
                'text': self.params}
