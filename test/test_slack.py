from unittest import TestCase

from code.slack import SlashCommand
from code.slack import SlashCommandFactory


class TestSlashCommand(TestCase):
    def setUp(self):
        self.BODY_SAMPLE = 'command=/test&text=param1%20param2&response_url=https://hooks.slack.com/commands/1234/5678&user_id=U2147483697'  # noqa:E501

        self.c = SlashCommand(
            body=self.BODY_SAMPLE,
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
            'body': self.BODY_SAMPLE}

        c = SlashCommandFactory('SigingSecret').load_from_event(event)

        self.assertEquals(c.signature, 'slacksignature')
        self.assertEquals(c.timestamp, '12345678')
        self.assertEquals(c.body, self.BODY_SAMPLE)  # noqa: E501
        self.assertEquals(c.response_url, 'https://hooks.slack.com/commands/1234/5678')  # noqa: E501
        self.assertEquals(c.name, 'test')
        self.assertEquals(c.params, ['param1', 'param2'])
        self.assertEquals(c.user_id, 'U2147483697')

    def test_load_from_event_with_noparams(self):
        event = {
            'headers': {
                'X-Slack-Request-Timestamp': '12345678',
                'X-Slack-Signature': 'slacksignature'},
            'body': 'command=/test&response_url=https://hooks.slack.com/commands/1234/5678&user_id=U2147483697'}  # noqa: E501

        c = SlashCommandFactory('SigingSecret').load_from_event(event)

        self.assertEquals(c.params, [''])

    def test_load_from_state(self):
        state = {'response_url': 'https://hooks.slack.com/commands/abcd/efgh',  # noqa: E501
                 'command': 'test2',
                 'text': ['hoge', 'fuga']}

        c = SlashCommandFactory().load_from_state(state)

        self.assertEquals(c.response_url, 'https://hooks.slack.com/commands/abcd/efgh')  # noqa: E501
        self.assertEquals(c.name, 'test2')
        self.assertEquals(c.params, ['hoge', 'fuga'])

    def test_verify(self):
        c = SlashCommand(
            body='command=/test&text=param1%20param2&response_url=https://hooks.slack.com/commands/1234/5678',  # noqa:E501
            response_url='https://hooks.slack.com/commands/1234/5678',
            timestamp='1234567890',
            sigining_secret='abcd1234',
            signature='v0=4700da1669cac1f44451880f3b5668e85bb0782af521580543feb77d3e47a5fc',  # noqa: E501
            name='test',
            params=['param1', 'param2'])

        self.assertTrue(c.verify_request())

    def test_verify_fail(self):
        c = SlashCommand(
            body='command=/test&text=param1%20param2&response_url=https://hooks.slack.com/commands/1234/5678',  # noqa:E501
            response_url='https://hooks.slack.com/commands/1234/5678',
            timestamp='1234567890',
            sigining_secret='abcd123456',  # 不正な値
            signature='v0=4700da1669cac1f44451880f3b5668e85bb0782af521580543feb77d3e47a5fc',  # noqa: E501
            name='test',
            params=['param1', 'param2'])

        self.assertFalse(c.verify_request())

    def test_dump_state(self):
        state = self.c.dump_state()

        self.assertEquals(state, {'response_url': 'https://hooks.slack.com/commands/1234/5678',  # noqa: E501
                                  'command': 'test',
                                  'text': ['param1', 'param2']})
