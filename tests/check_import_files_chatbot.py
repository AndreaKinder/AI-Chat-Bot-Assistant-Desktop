import unittest
from unittest.mock import patch
from src.logs.check_log import check_file_log
from src.logs.create_log import capture_log
import unittest
from src.src_guides.directory_guide import log_directory


class LogDirectoryTest(unittest.TestCase):
    def test_log_directory(self):
        self.assertEqual(first=log_directory(), second='storage/log.json')


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
