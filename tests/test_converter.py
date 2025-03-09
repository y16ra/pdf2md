import os
import unittest
from unittest.mock import patch, mock_open, MagicMock
from pathlib import Path

from pdf2md.converter import PDF2MarkdownConverter


class TestPDF2MarkdownConverter(unittest.TestCase):
    def setUp(self):
        """テストの前準備"""
        # 環境変数の設定
        if "MISTRAL_API_KEY" in os.environ:
            del os.environ["MISTRAL_API_KEY"]
        os.environ["MISTRAL_API_KEY"] = "dummy_api_key"
        self.converter = PDF2MarkdownConverter()
        self.test_pdf_path = "test.pdf"
        self.test_md_path = "test.md"

    def tearDown(self):
        """テスト後のクリーンアップ"""
        # 環境変数の削除
        if "MISTRAL_API_KEY" in os.environ:
            del os.environ["MISTRAL_API_KEY"]

    @patch('pdf2md.converter.load_dotenv')
    @patch.dict(os.environ, {}, clear=True)
    def test_init_without_api_key(self, mock_load_dotenv):
        """API keyが設定されていない場合のテスト"""
        # load_dotenvが何もしないようにする
        mock_load_dotenv.return_value = None

        with self.assertRaises(ValueError) as context:
            PDF2MarkdownConverter()
        
        self.assertEqual(str(context.exception), "MISTRAL_API_KEY environment variable is not set")

    @patch('pdf2md.converter.requests.post')
    def test_upload_file_success(self, mock_post):
        """ファイルアップロードの成功テスト"""
        # モックの設定
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "test_file_id"}
        mock_post.return_value = mock_response

        # テスト用のファイルデータ
        test_file_data = b"dummy pdf content"
        mock_file = mock_open()
        mock_file.return_value.read.return_value = test_file_data

        with patch('builtins.open', mock_file), \
             patch('os.path.exists', return_value=True):
            result = self.converter._upload_file(self.test_pdf_path)

        self.assertEqual(result, {"id": "test_file_id"})
        mock_post.assert_called_once()

    @patch('pdf2md.converter.requests.post')
    def test_upload_file_failure(self, mock_post):
        """ファイルアップロードの失敗テスト"""
        # モックの設定
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"
        mock_post.return_value = mock_response

        # テスト用のファイルデータ
        test_file_data = b"dummy pdf content"
        mock_file = mock_open()
        mock_file.return_value.read.return_value = test_file_data

        with patch('builtins.open', mock_file), \
             patch('os.path.exists', return_value=True):
            with self.assertRaises(Exception) as context:
                self.converter._upload_file(self.test_pdf_path)

        self.assertIn("APIリクエストエラー", str(context.exception))

    @patch('pdf2md.converter.requests.get')
    def test_get_signed_url_success(self, mock_get):
        """署名付きURL取得の成功テスト"""
        # モックの設定
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"url": "https://example.com/signed_url"}
        mock_get.return_value = mock_response

        result = self.converter._get_signed_url("test_file_id")

        self.assertEqual(result, "https://example.com/signed_url")
        mock_get.assert_called_once()

    @patch('pdf2md.converter.requests.get')
    def test_get_signed_url_failure(self, mock_get):
        """署名付きURL取得の失敗テスト"""
        # モックの設定
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        mock_get.return_value = mock_response

        with self.assertRaises(Exception) as context:
            self.converter._get_signed_url("test_file_id")

        self.assertIn("Failed to get signed URL", str(context.exception))

    @patch('pdf2md.converter.requests.post')
    @patch('pdf2md.converter.requests.get')
    def test_convert_with_upload_success(self, mock_get, mock_post):
        """convert_with_uploadメソッドの成功テスト"""
        # アップロードのモック
        upload_response = MagicMock()
        upload_response.status_code = 200
        upload_response.json.return_value = {"id": "test_file_id"}

        # 署名付きURLのモック
        signed_url_response = MagicMock()
        signed_url_response.status_code = 200
        signed_url_response.json.return_value = {"url": "https://example.com/signed_url"}

        # 変換APIのモック
        convert_response = MagicMock()
        convert_response.status_code = 200
        convert_response.json.return_value = {
            "pages": [{"markdown": "# Test Markdown\n\nThis is a test."}]
        }

        mock_post.side_effect = [upload_response, convert_response]
        mock_get.return_value = signed_url_response

        # ファイル操作のモック
        test_file_data = b"dummy pdf content"
        mock_file = mock_open()
        mock_file.return_value.read.return_value = test_file_data

        with patch('builtins.open', mock_file), \
             patch('os.path.exists', return_value=True):
            result = self.converter.convert_with_upload(self.test_pdf_path)

        self.assertTrue(isinstance(result, str))
        self.assertTrue(result.endswith(".md"))
        mock_post.assert_called()
        mock_get.assert_called_once()

    @patch('pdf2md.converter.requests.post')
    def test_convert_success(self, mock_post):
        """convertメソッドの成功テスト"""
        # モックの設定
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "pages": [{"markdown": "# Test Markdown\n\nThis is a test."}]
        }
        mock_post.return_value = mock_response

        # ファイル操作のモック
        test_file_data = b"dummy pdf content"
        mock_file = mock_open()
        mock_file.return_value.read.return_value = test_file_data

        with patch('builtins.open', mock_file), \
             patch('os.path.exists', return_value=True):
            result = self.converter.convert(self.test_pdf_path)

        self.assertTrue(isinstance(result, str))
        self.assertTrue(result.endswith(".md"))
        mock_post.assert_called_once()

    def test_convert_file_not_found(self):
        """存在しないファイルの変換テスト"""
        with self.assertRaises(FileNotFoundError):
            self.converter.convert("non_existent.pdf")

    def test_convert_with_upload_file_not_found(self):
        """存在しないファイルのアップロード変換テスト"""
        with self.assertRaises(FileNotFoundError):
            self.converter.convert_with_upload("non_existent.pdf")


if __name__ == '__main__':
    unittest.main() 
