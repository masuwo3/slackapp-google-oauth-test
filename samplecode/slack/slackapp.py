from urllib.parse import parse_qs
import hmac
import hashlib

from samplecode.slack.slashcommand import SlashCommand


class SlackApp:
    def __init__(self, sigining_secret=None):
        self.sigining_secret = sigining_secret

    def load_command(self, event):
        payload = parse_qs(event['body'])

        ts = event['headers']['X-Slack-Request-Timestamp']
        sig = event['headers']['X-Slack-Signature']
        body_raw = event['body']
        resp_url = payload['response_url'][0]
        name = payload['command'][0].lstrip('/')
        # 送られたコマンドに引数がない場合は、空文字のlistを加える
        params = payload['text'][0].split() if 'text' in payload else ['']
        user_id = payload['user_id'][0]

        return SlashCommand(body=body_raw, timestamp=ts,
                            signature=sig, response_url=resp_url,
                            name=name, params=params,
                            sigining_secret=self.sigining_secret,
                            user_id=user_id)

    def verify(self, event):
        try:
            sig = event['headers']['X-Slack-Signature']
            timestamp = event['headers']['X-Slack-Request-Timestamp']
            body = event['body']

            req = str.encode('v0:' + timestamp + ':' + body)
            req_hash = 'v0=' + hmac.new(str.encode(self.sigining_secret),
                                        req,
                                        hashlib.sha256).hexdigest()

            return hmac.compare_digest(req_hash, sig)
        except KeyError:
            return False
