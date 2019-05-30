from unittest import TestCase
from unittest.mock import MagicMock

from code.credential import CredsStore


class TestCredsStore(TestCase):
    def test_save(self):
        store = CredsStore('dummy')
        store.table.put_item = MagicMock(return_value={})

        store.save('test_user', {'access_token': 'hogehoge',
                                 'refresh_token': 'fugafuga'})

        store.table.put_item.assert_called_with(
            Item={'user_id': 'test_user',
                  'access_token': 'hogehoge',
                  'refresh_token': 'fugafuga'})

    def test_load(self):
        creds = {'user_id': 'hoge',
                 'access_token': 'hogehoge',
                 'refresh_token': 'fugafuga'}

        store = CredsStore('dummy')
        store.table.get_item = MagicMock(return_value=creds)

        self.assertEquals(store.load('hoge'), creds)
