from unittest import TestCase

from code.slack import SlashCommand
from code.slack import SlashCommandFactory


class TestSlashCommand(TestCase):
    def setUp(self):
        self.c = SlashCommand(
            body='command=/test&text=param1%20param2&response_url=https://hooks.slack.com/commands/1234/5678',  # noqa:E501
            response_url='https://hooks.slack.com/commands/1234/5678',
            timestamp='1234567890',
            sigining_secret='abcd1234',
            signature='v0=4700da1669cac1f44451880f3b5668e85bb0782af521580543feb77d3e47a5fc',  # noqa: E501
            name='test',
            params=['param1', 'param2'])

    def test_load_from_event(self):
        event = {
            'headers': {
                'X-Slack-Request-Timestamp': '12345678',
                'X-Slack-Signature': 'slacksignature'},
            'body': 'command=/test&text=param1%20param2&response_url=https://hooks.slack.com/commands/1234/5678'}  # noqa: E501

        c = SlashCommandFactory('SigingSecret').load_from_event(event)

        self.assertEquals(c.signature, 'slacksignature')
        self.assertEquals(c.timestamp, '12345678')
        self.assertEquals(c.body, 'command=/test&text=param1%20param2&response_url=https://hooks.slack.com/commands/1234/5678')  # noqa: E501
        self.assertEquals(c.response_url, 'https://hooks.slack.com/commands/1234/5678')  # noqa: E501
        self.assertEquals(c.name, 'test')
        self.assertEquals(c.params, ['param1', 'param2'])

    def test_load_from_event_with_noparams(self):
        event = {
            'headers': {
                'X-Slack-Request-Timestamp': '12345678',
                'X-Slack-Signature': 'slacksignature'},
            'body': 'command=/test&response_url=https://hooks.slack.com/commands/1234/5678'}  # noqa: E501

        c = SlashCommandFactory('SigingSecret').load_from_event(event)

        self.assertEquals(c.params, [''])

    def test_load_from_state(self):
        state = {'response_url': ['https://hooks.slack.com/commands/abcd/efgh'],
                 'command': ['test2'],
                 'text': [['hoge', 'fuga']]}

        c = SlashCommandFactory().load_from_state(state)

        self.assertEquals(c.response_url, 'https://hooks.slack.com/commands/abcd/efgh')
        self.assertEquals(c.name, 'test2')
        self.assertEquals(c.params, ['hoge', 'fuga'])

    def test_verify(self):
        self.assertTrue(self.c.verify_request())

    def test_verify_fail(self):
        self.c.sigining_secret = 'abcd123456'

        self.assertFalse(self.c.verify_request())

    def test_dump_state(self):
        state = self.c.dump_state()

        self.assertEquals(state, {'response_url': 'https://hooks.slack.com/commands/1234/5678',  # noqa: E501
                                  'command': 'test',
                                  'text': ['param1', 'param2']})
