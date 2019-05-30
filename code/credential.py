import boto3


class CredsStore:
    def __init__(self, table_name, session=None):
        if session is None:
            session = boto3.Session()
        self.table = session.resource('dynamodb').Table(table_name)

    def save(self, user_id, tokens):
        self.table.put_item(Item={'user_id': user_id, **tokens})

    def load(self, user_id):
        return self.table.get_item(Key={'user_id': user_id})
