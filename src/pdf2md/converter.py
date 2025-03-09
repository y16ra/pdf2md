import base64
import os
import urllib.parse
from pathlib import Path

import requests
from dotenv import load_dotenv


class PDF2MarkdownConverter:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("MISTRAL_API_KEY")
        if not self.api_key:
            raise ValueError("MISTRAL_API_KEY environment variable is not set")

        self.api_url = "https://api.mistral.ai/v1/ocr"
        self.files_url = "https://api.mistral.ai/v1/files"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _upload_file(self, file_path: str) -> dict:
        """PDFファイルをMistral AIにアップロードする

        Args:
            file_path (str): アップロードするファイルのパス

        Returns:
            dict: アップロードされたファイルの情報
        """
        try:
            # バイナリモードでファイルを開く
            with open(file_path, "rb") as f:
                file_data = f.read()

            # ファイル名を取得
            file_name = os.path.basename(file_path)

            # multipart/form-dataのヘッダーを設定
            headers = {"Authorization": f"Bearer {self.api_key}"}

            # multipart/form-dataとしてファイルを送信
            files = {
                "purpose": (None, "ocr"),
                "file": (file_name, file_data, "application/pdf"),
            }

            # デバッグ用にリクエストの詳細をログ出力
            print(f"Uploading file: {file_name}")
            print(f"Headers: {headers}")
            print(f"Files structure: {files.keys()}")

            # ファイルのアップロード
            response = requests.post(self.files_url, headers=headers, files=files)

            # デバッグ用にレスポンスの詳細をログ出力
            print(f"Response status: {response.status_code}")
            print(f"Response headers: {response.headers}")
            print(f"Response body: {response.text}")

            if response.status_code != 200:
                error_detail = response.text
                try:
                    error_json = response.json()
                    if "detail" in error_json:
                        error_detail = error_json["detail"]
                except:
                    pass
                raise Exception(
                    f"APIリクエストエラー (Status: {response.status_code}): {error_detail}"
                )

            return response.json()

        except requests.exceptions.RequestException as e:
            raise Exception(f"ネットワークエラー: {str(e)}")
        except Exception as e:
            raise Exception(f"ファイルアップロードエラー: {str(e)}")

    def _get_signed_url(self, file_id: str) -> str:
        """アップロードされたファイルの署名付きURLを取得する

        Args:
            file_id (str): ファイルID

        Returns:
            str: 署名付きURL
        """
        url = f"{self.files_url}/{file_id}/url"
        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
            raise Exception(f"Failed to get signed URL: {response.text}")

        return response.json()["url"]

    def convert_with_upload(self, pdf_path: str, output_path: str = None) -> str:
        """PDFファイルをアップロードしてMarkdownに変換する

        Args:
            pdf_path (str): 入力PDFファイルのパス
            output_path (str, optional): 出力Markdownファイルのパス。
                                      指定がない場合はPDFと同じ場所に保存。

        Returns:
            str: 生成されたMarkdownファイルのパス
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        # ファイルのアップロード
        uploaded_file = self._upload_file(pdf_path)

        # 署名付きURLの取得
        signed_url = self._get_signed_url(uploaded_file["id"])

        # APIリクエストの準備
        payload = {
            "model": "mistral-ocr-latest",
            "document": {"type": "document_url", "document_url": signed_url},
        }

        # APIリクエストの実行
        response = requests.post(self.api_url, headers=self.headers, json=payload)

        if response.status_code != 200:
            raise Exception(f"API request failed: {response.text}")

        # レスポンスからMarkdownテキストを抽出
        result = response.json()
        markdown_text = ""
        for page in result.get("pages", []):
            markdown_text += page.get("markdown", "") + "\n\n"

        # 出力パスの設定
        if output_path is None:
            pdf_path = Path(pdf_path)
            output_path = pdf_path.with_suffix(".md")

        # Markdownファイルの保存
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown_text)

        return str(output_path)

    def convert(self, pdf_path: str, output_path: str = None) -> str:
        """PDFファイルをMarkdownに変換する

        Args:
            pdf_path (str): 入力PDFファイルのパス
            output_path (str, optional): 出力Markdownファイルのパス。
                                      指定がない場合はPDFと同じ場所に保存。

        Returns:
            str: 生成されたMarkdownファイルのパス
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        # PDFファイルをbase64エンコード
        with open(pdf_path, "rb") as file:
            pdf_content = file.read()
            pdf_name = os.path.basename(pdf_path)

        # Base64エンコードされたPDFデータをdata URLとして準備
        base64_pdf = base64.b64encode(pdf_content).decode("utf-8")
        data_url = f"data:application/pdf;base64,{base64_pdf}"

        # APIリクエストの準備
        payload = {
            "model": "mistral-ocr-latest",  # 正しいモデル名を使用
            "document": {
                "type": "document_url",
                "document_url": data_url,
                "document_name": pdf_name,
            },
        }

        # APIリクエストの実行
        response = requests.post(self.api_url, headers=self.headers, json=payload)

        if response.status_code != 200:
            raise Exception(f"API request failed: {response.text}")

        # レスポンスからMarkdownテキストを抽出
        result = response.json()
        markdown_text = ""
        for page in result.get("pages", []):
            markdown_text += page.get("markdown", "") + "\n\n"

        # 出力パスの設定
        if output_path is None:
            pdf_path = Path(pdf_path)
            output_path = pdf_path.with_suffix(".md")

        # Markdownファイルの保存
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown_text)

        return str(output_path)
