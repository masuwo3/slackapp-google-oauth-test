from unittest import TestCase

from code.slack import SlashCommand


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

    def test_verify(self):
        self.assertTrue(self.c.verify_request())

    def test_verify_fail(self):
        self.c.sigining_secret = 'abcd123456'  # 不正な値

        self.assertFalse(self.c.verify_request())

    def test_dump_state(self):
        self.assertEquals(self.c.dump_state(), {'response_url': 'https://hooks.slack.com/commands/1234/5678',  # noqa: E501
                                                'command': 'test',
                                                'text': ['param1', 'param2']})
