# PDF2MD

PDFファイルをMarkdownに変換するPythonツール。Mistral AI OCR APIを使用して、PDFファイルのテキストを抽出し、Markdown形式で保存します。

## インストール

```bash
# 仮想環境の作成と有効化
python -m venv venv
source venv/bin/activate  # Windowsの場合: venv\Scripts\activate

# 依存パッケージのインストール
pip install -r requirements.txt
```

## 環境設定

1. Mistral AI APIキーを取得します（https://docs.mistral.ai/）
2. `.env`ファイルを作成し、以下の内容を追加します：

```
MISTRAL_API_KEY=your_api_key_here
```

## 使用方法

```bash
# 基本的な使用方法
python -m pdf2md.cli input.pdf

# 出力ファイルを指定する場合
python -m pdf2md.cli input.pdf -o output.md
```

## 機能

- PDFファイルのテキスト抽出
- Markdown形式での保存
- コマンドラインインターフェース
- カスタム出力パスのサポート

## ライセンス

MITライセンスの下で公開されています。詳細は[LICENSE](LICENSE)ファイルを参照してください。
