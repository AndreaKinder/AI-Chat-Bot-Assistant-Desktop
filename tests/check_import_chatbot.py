import unittest
from src.src_guides.hug_api import import_log
from unittest.mock import patch, MagicMock
from src.src_guides.hug_api import create_cookies


class TestImportChatBot(unittest.TestCase):

    @patch('src.src_guides.hug_api.check_file_log')
    @patch('src.src_guides.hug_api.read_log')
    def test_import_log_not_none(self, mock_read_log, mock_check_file_log):
        mock_check_file_log.return_value = True
        mock_read_log.return_value = ('email@example.com', 'password123')

        result1, result2 = import_log()

        self.assertIsNotNone(result1)
        self.assertIsNotNone(result2)

    @patch('src.src_guides.hug_api.check_file_log')
    def test_import_log_is_none(self, mock_check_file_log):
        mock_check_file_log.return_value = False

        result1, result2 = import_log()

        self.assertIsNone(result1)
        self.assertIsNone(result2)


class TestHugApi(unittest.TestCase):

    @patch('src.src_guides.hug_api.import_log')
    @patch('src.src_guides.hug_api.Login')
    def test_create_cookies(self, mock_login, mock_import_log):
        mock_import_log.return_value = ('test_email@example.com', 'test_password')
        mock_login_instance = MagicMock()
        mock_login.return_value = mock_login_instance
        mock_login_instance.login.return_value = MagicMock(get_dict=MagicMock(return_value={'cookie_key': 'cookie_value'}))

        cookies = create_cookies()

        mock_import_log.assert_called_once()
        mock_login.assert_called_once_with('test_email@example.com', 'test_password')
        mock_login_instance.login.assert_called_once_with(cookie_dir_path='./storage/', save_cookies=True)
        self.assertEqual(cookies.get_dict(), {'cookie_key': 'cookie_value'})


if __name__ == '__main__':
    unittest.main()