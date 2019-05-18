from unittest import TestCase

from code.slack import SlashCommand


class TestSlashCommand(TestCase):
    def setUp(self):
        self.c = SlashCommand('SigingSecret')
        event = {
            'headers': {
                'X-Slack-Request-Timestamp': '12345678',
                'X-Slack-Signature': 'slacksignature'},
            'body': 'command=/test&text=param1%20param2&response_url=https://hooks.slack.com/commands/1234/5678'}  # noqa: E501
        self.c.load_event(event)

    def test_load_event(self):
        self.assertEquals(self.c.signature, 'slacksignature')
        self.assertEquals(self.c.timestamp, '12345678')
        self.assertEquals(self.c.payload_raw,
                          'command=/test&text=param1%20param2&response_url=https://hooks.slack.com/commands/1234/5678')  # noqa: E501
        self.assertEquals(self.c.response_url,
                          'https://hooks.slack.com/commands/1234/5678')
        self.assertEquals(self.c.command_name, 'test')
        self.assertEquals(self.c.params, ['param1', 'param2'])

    def test_verify(self):
        c = SlashCommand('abcd1234')
        c.payload_raw = 'command=/test&text=param1%20param2&response_url=https://hooks.slack.com/commands/1234/5678'  # noqa: E501
        c.timestamp = '1234567890'
        c.signature = 'v0=4700da1669cac1f44451880f3b5668e85bb0782af521580543feb77d3e47a5fc'  # noqa: E501

        self.assertTrue(c.verify_request())

    def test_verify_fail(self):
        c = SlashCommand('abcd123456')
        c.payload_raw = 'command=/test&text=param1%20param2&response_url=https://hooks.slack.com/commands/1234/5678'  # noqa: E501
        c.timestamp = '1234567890'
        c.signature = 'v0=4700da1669cac1f44451880f3b5668e85bb0782af521580543feb77d3e47a5fc'  # noqa: E501

        self.assertFalse(c.verify_request())

    def test_dump_state(self):
        state = self.c.dump_state()

        self.assertEquals(state, {'response_url': 'https://hooks.slack.com/commands/1234/5678',  # noqa: E501
                                  'command': 'test',
                                  'text': ['param1', 'param2']})

    def test_dump_state_noparams(self):
        event = {
            'headers': {
                'X-Slack-Request-Timestamp': '12345678',
                'X-Slack-Signature': 'slacksignature'},
            'body': 'command=/test&response_url=https://hooks.slack.com/commands/1234/5678'}  # noqa: E501

        self.c.load_event(event)
        state = self.c.dump_state()

        self.assertEquals(state, {'response_url': 'https://hooks.slack.com/commands/1234/5678',  # noqa: E501
                                  'command': 'test',
                                  'text': ['']})
