from unittest import TestCase

from samplecode.slack.slashcommand import SlashCommand


class TestSlashCommand(TestCase):
    def setUp(self):
        self.BODY_SAMPLE = 'command=/test&text=param1%20param2&response_url=https://hooks.slack.com/commands/1234/5678'  # noqa:E501
        self.SIGNATURE_SAMPLE = 'v0=4700da1669cac1f44451880f3b5668e85bb0782af521580543feb77d3e47a5fc'  # noqa: E501
        self.c = SlashCommand(
            body=self.BODY_SAMPLE,
            response_url='https://hooks.slack.com/commands/1234/5678',
            timestamp='1234567890',
            sigining_secret='abcd1234',
            signature=self.SIGNATURE_SAMPLE,
            name='test',
            user_id='U2147483697',
            params=['param1', 'param2'])

    def test_id(self):
        # md5('1234567890/U2147483697'.encode()).hexdigest() =>
        _id = '8b8f635617a60e22ac9e491241f03631'

        self.assertEqual(self.c.gen_id(), _id)

    def test_dump_state(self):
        self.assertEqual(self.c.dump(),
                         {'body': self.BODY_SAMPLE,
                          'response_url': 'https://hooks.slack.com/commands/1234/5678',  # noqa:E501
                          'timestamp': '1234567890',
                          'sigining_secret': 'abcd1234',
                          'signature': self.SIGNATURE_SAMPLE,
                          'user_id': 'U2147483697',
                          'name': 'test',
                          'params': ['param1', 'param2']})
