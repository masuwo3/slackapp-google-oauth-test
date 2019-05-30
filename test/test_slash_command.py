from unittest import TestCase

from samplecode.slack import SlashCommand


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
            params=['param1', 'param2'])

    def test_verify(self):
        self.assertTrue(self.c.verify_request())

    def test_verify_fail(self):
        self.c.sigining_secret = 'abcd123456'  # 不正な値

        self.assertFalse(self.c.verify_request())

    def x_test_dump_state(self):
        self.assertEqual(self.c.dump(),
                         {'body': self.BODY_SAMPLE,
                          'response_url': 'https://hooks.slack.com/commands/1234/5678',  # noqa:E501
                          'timestamp': '1234567890',
                          'sigining_secret': 'abcd1234',
                          'signature': self.SIGNATURE_SAMPLE,
                          'name': 'test',
                          'params': ['param1', 'param2']})
