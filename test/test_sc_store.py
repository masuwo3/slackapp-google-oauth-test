from unittest import TestCase
from unittest.mock import MagicMock

from code.slack import SlashCommand
from code.slack import SlashCommandStore


class TestSCStore(TestCase):
    def test_save(self):
        pass
        # store = SlashCommandStore('dummy')
        # store.table.put_item = MagicMock(return_value={})

        # c = SlashCommand()

        # store.save(c)

    def test_load(self):
        pass

        # self.assertEquals(c.load(key), {})
