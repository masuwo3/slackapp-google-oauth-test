import unittest
from unittest import TestCase

from samplecode.slack.slackapp import SlackApp


class TestSlackApp(TestCase):
    def setUp(self):
        self.BODY_SAMPLE = 'command=/test&text=param1%20param2&response_url=https://hooks.slack.com/commands/1234/5678&user_id=U2147483697'  # noqa:E501
        self.SIGNATURE_SAMPLE = 'v0=70e3a8c83f306dc9eb7752518f8bfadabbad04729fbaffded1b93fc6e63ef480'  # noqa: E501

        self.event = {
            'headers': {
                'X-Slack-Request-Timestamp': '12345678',
                'X-Slack-Signature': self.SIGNATURE_SAMPLE},
            'body': self.BODY_SAMPLE}

        # self.BODY_SAMPLE = 'command=/test&text=param1%20param2&response_url=https://hooks.slack.com/commands/1234/5678&user_id=U2147483697'  # noqa:E501

    def test_load_command(self):
        c = SlackApp('SigingSecret').load_command(self.event)

        self.assertEqual(c.signature, self.SIGNATURE_SAMPLE)
        self.assertEqual(c.timestamp, '12345678')
        self.assertEqual(c.body, self.BODY_SAMPLE)  # noqa: E501
        self.assertEqual(c.response_url, 'https://hooks.slack.com/commands/1234/5678')  # noqa: E501
        self.assertEqual(c.name, 'test')
        self.assertEqual(c.params, ['param1', 'param2'])
        self.assertEqual(c.user_id, 'U2147483697')

    def test_load_command_with_noparams(self):
        self.event['body'] = 'command=/test&response_url=https://hooks.slack.com/commands/1234/5678&user_id=U2147483697'  # noqa: E501
        c = SlackApp('SigingSecret').load_command(self.event)

        self.assertEqual(c.params, [''])

    def test_verify(self):
        self.assertTrue(SlackApp('abcd1234').verify(self.event))

    def test_verify_failed(self):
        self.assertFalse(SlackApp('abcd123456').verify(self.event))


if __name__ == '__main__':
    unittest.main()
