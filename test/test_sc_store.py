import unittest
from unittest import TestCase
from unittest.mock import MagicMock

from samplecode.slack.slashcommand import SlashCommand
from samplecode.slack.slashcommand import SlashCommandStore


class TestSCStore(TestCase):
    def setUp(self):
        self.c = SlashCommand(
            response_url='https://hooks.slack.com/commands/1234/5678',
            timestamp='1234567890',
            user_id='U2147483697',
            name='test',
            params=['param1', 'param2'])

    def test_save(self):
        store = SlashCommandStore('dummy')
        store.table.put_item = MagicMock(return_value={})

        _id = store.save(self.c)

        store.table.put_item.assert_called_with(
            Item={'id': '8b8f635617a60e22ac9e491241f03631',
                  'command': {
                      'response_url': 'https://hooks.slack.com/commands/1234/5678',  # noqa:E501
                      'timestamp': '1234567890',
                      'user_id': 'U2147483697',
                      'name': 'test',
                      'params': ['param1', 'param2']}})

        self.assertEqual(_id, '8b8f635617a60e22ac9e491241f03631')

    def test_load(self):
        resp = {'Item': {'user_id': 'hogehoge',
                         'command': self.c.dump()}}

        store = SlashCommandStore('dummy')
        store.table.get_item = MagicMock(return_value=resp)

        loaded_c = store.load('hogehoge')

        self.assertEqual(self.c.response_url, loaded_c.response_url)
        self.assertEqual(self.c.timestamp, loaded_c.timestamp)
        self.assertEqual(self.c.user_id, loaded_c.user_id)
        self.assertEqual(self.c.name, loaded_c.name)
        self.assertEqual(self.c.params, loaded_c.params)


if __name__ == '__main__':
    unittest.main()
