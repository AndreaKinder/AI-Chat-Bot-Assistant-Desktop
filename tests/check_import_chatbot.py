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


if __name__ == '__main__':
    unittest.main()
