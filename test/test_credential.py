from unittest import TestCase
from unittest.mock import MagicMock

from code.credential import CredStore


class TestCredStore(TestCase):
    def test_save(self):
        store = CredStore('dummy')
        store.table.put_item = MagicMock(return_value={})

        store.save('test_user', {'access_token': 'hogehoge',
                                 'refresh_token': 'fugafuga'})

        store.table.put_item.assert_called_with(
            Item={'user_id': 'test_user',
                  'access_token': 'hogehoge',
                  'refresh_token': 'fugafuga'})

    def test_load(self):
        resp = {'Item': {'user_id': 'hoge',
                         'access_token': 'hogehoge',
                         'refresh_token': 'fugafuga'}}

        store = CredStore('dummy')
        store.table.get_item = MagicMock(return_value=resp)

        self.assertEquals(store.load('hoge'), {'user_id': 'hoge',
                                               'access_token': 'hogehoge',
                                               'refresh_token': 'fugafuga'})
