from unittest import TestCase

from samplecode.slack import SlashCommandFactory


class TestSCFactory(TestCase):
    def setUp(self):
        self.BODY_SAMPLE = 'command=/test&text=param1%20param2&response_url=https://hooks.slack.com/commands/1234/5678&user_id=U2147483697'  # noqa:E501

    def test_load_from_event(self):
        event = {
            'headers': {
                'X-Slack-Request-Timestamp': '12345678',
                'X-Slack-Signature': 'slacksignature'},
            'body': self.BODY_SAMPLE}

        c = SlashCommandFactory('SigingSecret').load_from_event(event)

        self.assertEqual(c.signature, 'slacksignature')
        self.assertEqual(c.timestamp, '12345678')
        self.assertEqual(c.body, self.BODY_SAMPLE)  # noqa: E501
        self.assertEqual(c.response_url, 'https://hooks.slack.com/commands/1234/5678')  # noqa: E501
        self.assertEqual(c.name, 'test')
        self.assertEqual(c.params, ['param1', 'param2'])
        self.assertEqual(c.user_id, 'U2147483697')

    def test_load_from_event_with_noparams(self):
        event = {
            'headers': {
                'X-Slack-Request-Timestamp': '12345678',
                'X-Slack-Signature': 'slacksignature'},
            'body': 'command=/test&response_url=https://hooks.slack.com/commands/1234/5678&user_id=U2147483697'}  # noqa: E501

        c = SlashCommandFactory('SigingSecret').load_from_event(event)

        self.assertEqual(c.params, [''])

    def test_load_from_state(self):
        state = {'response_url': 'https://hooks.slack.com/commands/abcd/efgh',  # noqa: E501
                 'command': 'test2',
                 'text': ['hoge', 'fuga']}

        c = SlashCommandFactory().load_from_state(state)

        self.assertEqual(c.response_url, 'https://hooks.slack.com/commands/abcd/efgh')  # noqa: E501
        self.assertEqual(c.name, 'test2')
        self.assertEqual(c.params, ['hoge', 'fuga'])
