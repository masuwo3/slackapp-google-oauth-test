import hashlib

import boto3


class SlashCommandStore:
    def __init__(self, table_name, session=None):
        if session is None:
            session = boto3.Session()
        self.table = session.resource('dynamodb').Table(table_name)

    def save(self, command):
        id_ = command.gen_id()
        self.table.put_item(Item={'id': id_, 'command': command.dump()})
        return id_

    def load(self, id_):
        resp = self.table.get_item(Key={'id': id_})
        command_params = resp['Item']['command']
        return SlashCommand(**command_params)


class SlashCommand:
    def __init__(self, body=None, timestamp=None, signature=None,
                 response_url=None, name=None, params=None,
                 sigining_secret=None, user_id=None, **args):
        self.body = body
        self.timestamp = timestamp
        self.signature = signature
        self.response_url = response_url
        self.name = name
        self.params = params
        self.sigining_secret = sigining_secret
        self.user_id = user_id
        self.extra = args

    def dump(self):
        d = {'body': self.body,
             'timestamp': self.timestamp,
             'signature': self.signature,
             'response_url': self.response_url,
             'name': self.name,
             'params': self.params,
             'sigining_secret': self.sigining_secret,
             'user_id': self.user_id,
             'extra': self.extra}

        return dict(filter(lambda x: bool(x[1]), d.items()))

    def gen_id(self):
        seed = '/'.join([self.timestamp, self.user_id])
        return hashlib.md5(str.encode(seed)).hexdigest()
