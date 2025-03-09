import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pdf2md.cli import main


class TestPDF2MarkdownConverter(unittest.TestCase):

    @patch("pdf2md.cli.PDF2MarkdownConverter")
    def test_convert_success(self, MockConverter):
        # モックの設定
        mock_instance = MockConverter.return_value
        mock_instance.convert.return_value = "output.md"

        # コマンドライン引数のモック
        test_args = ["cli.py", "test.pdf", "--output", "output.md"]
        with patch("sys.argv", test_args):
            main()

        # 変換メソッドが呼ばれたことを確認
        mock_instance.convert.assert_called_once_with("test.pdf", "output.md")

    @patch("pdf2md.cli.PDF2MarkdownConverter")
    def test_convert_with_upload(self, MockConverter):
        # モックの設定
        mock_instance = MockConverter.return_value
        mock_instance.convert_with_upload.return_value = "output.md"

        # コマンドライン引数のモック
        test_args = ["cli.py", "test.pdf", "--upload"]
        with patch("sys.argv", test_args):
            main()

        # アップロード変換メソッドが呼ばれたことを確認
        mock_instance.convert_with_upload.assert_called_once_with("test.pdf", None)

    @patch("pdf2md.cli.PDF2MarkdownConverter")
    def test_convert_file_not_found(self, MockConverter):
        # モックの設定
        mock_instance = MockConverter.return_value
        mock_instance.convert.side_effect = FileNotFoundError("File not found")

        # コマンドライン引数のモック
        test_args = ["cli.py", "nonexistent.pdf"]
        with patch("sys.argv", test_args):
            with self.assertRaises(SystemExit) as cm:
                main()

        # エラーメッセージが表示されたことを確認
        self.assertEqual(cm.exception.code, 1)


if __name__ == "__main__":
    unittest.main()
