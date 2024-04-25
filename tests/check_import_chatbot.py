import unittest
from src.main import import_log
from unittest.mock import patch, MagicMock
from src.main import create_cookies
from unittest.mock import patch
from src.main import check_file_log
from src.main import capture_log


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
        mock_login_instance.login.return_value = MagicMock(get_dict=MagicMock(
            return_value={'cookie_key': 'cookie_value'}))

        cookies = create_cookies()

        mock_import_log.assert_called_once()
        mock_login.assert_called_once_with('test_email@example.com', 'test_password')
        mock_login_instance.login.assert_called_once_with(cookie_dir_path='./storage/', save_cookies=True)
        self.assertEqual(cookies.get_dict(), {'cookie_key': 'cookie_value'})


class TestCheckFileLog(unittest.TestCase):

    @patch('src.logs.check_log.os.path.isfile')
    @patch('src.logs.check_log.os.path.isdir')
    @patch('src.logs.check_log.os.path.exists')
    @patch('src.logs.check_log.create_window_log')
    def test_check_file_log_exists_and_is_file(self, mock_create_window_log, mock_exists, mock_isdir, mock_isfile):
        mock_exists.return_value = True
        mock_isdir.return_value = True
        mock_isfile.return_value = True

        result = check_file_log()

        self.assertTrue(result)
        mock_create_window_log.assert_not_called()

    @patch('src.logs.check_log.os.path.isfile')
    @patch('src.logs.check_log.os.path.isdir')
    @patch('src.logs.check_log.os.path.exists')
    @patch('src.logs.check_log.create_window_log')
    def test_check_file_log_not_exists_or_not_file(self, mock_create_window_log, mock_exists, mock_isdir, mock_isfile):
        mock_exists.return_value = True
        mock_isdir.return_value = True
        mock_isfile.return_value = False

        result = check_file_log()

        self.assertFalse(result)
        mock_create_window_log.assert_called_once()


class TestCaptureLog(unittest.TestCase):
    @patch('src.logs.create_log.json.dump')
    @patch('src.logs.create_log.open', new_callable=unittest.mock.mock_open)
    def test_capture_log(self, mock_open, mock_json_dump):
        result = capture_log(us='us', passwd='passwd')
        self.assertTrue(result)
        mock_json_dump.assert_called_once()
        mock_open.assert_called_once()


if __name__ == '__main__':
    unittest.main()


if __name__ == '__main__':
    unittest.main()
