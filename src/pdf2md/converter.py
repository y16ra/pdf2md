import os
import base64
import requests
from dotenv import load_dotenv
from pathlib import Path

class PDF2MarkdownConverter:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('MISTRAL_API_KEY')
        if not self.api_key:
            raise ValueError("MISTRAL_API_KEY environment variable is not set")
        
        self.api_url = "https://api.mistral.ai/v1/ocr"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

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
        with open(pdf_path, 'rb') as file:
            pdf_content = file.read()
            pdf_name = os.path.basename(pdf_path)

        # Base64エンコードされたPDFデータをdata URLとして準備
        base64_pdf = base64.b64encode(pdf_content).decode('utf-8')
        data_url = f"data:application/pdf;base64,{base64_pdf}"

        # APIリクエストの準備
        payload = {
            "model": "mistral-ocr-latest",  # 正しいモデル名を使用
            "document": {
                "type": "document_url",
                "document_url": data_url,
                "document_name": pdf_name
            }
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
            output_path = pdf_path.with_suffix('.md')
        
        # Markdownファイルの保存
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_text)

        return str(output_path) 
