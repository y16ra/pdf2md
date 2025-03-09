# PDF2MD

PDFファイルをMarkdownに変換するPythonツール。Mistral AI OCR APIを使用して、PDFファイルのテキストを抽出し、Markdown形式で保存します。

## インストール

以下の2つのインストール方法があります：

### 1. 開発モードでのインストール

```bash
# 仮想環境の作成と有効化
python -m venv venv
source venv/bin/activate  # Windowsの場合: venv\Scripts\activate

# 依存パッケージのインストール
pip install -r requirements.txt

# 開発用パッケージのインストール（テスト実行に必要）
pip install -e .
```

### 2. パッケージとしてのインストール

```bash
# 仮想環境の作成と有効化（推奨）
python -m venv venv
source venv/bin/activate  # Windowsの場合: venv\Scripts\activate

# パッケージのインストール
pip install .
```

## 環境設定

1. Mistral AI APIキーを取得します（https://docs.mistral.ai/）
2. `.env`ファイルを作成し、以下の内容を追加します：

```
MISTRAL_API_KEY=your_api_key_here
```

## 使用方法

パッケージをインストールした場合：
```bash
# 基本的な使用方法（小さなファイル向け）
pdf2md input.pdf

# 大きなファイルの変換（ファイルアップロード方式）
pdf2md input.pdf --upload

# 出力ファイルを指定する場合
pdf2md input.pdf -o output.md

# アップロード方式で出力ファイルを指定する場合
pdf2md input.pdf --upload -o output.md
```

開発モードの場合：
```bash
# 基本的な使用方法
python -m pdf2md.cli input.pdf

# 大きなファイルの変換（ファイルアップロード方式）
python -m pdf2md.cli input.pdf --upload

# 出力ファイルを指定する場合
python -m pdf2md.cli input.pdf -o output.md
```

## 変換方式

このツールには2つの変換方式があります：

1. 直接変換方式（デフォルト）
   - PDFファイルを直接APIに送信
   - 小さなファイルに適している
   - 追加のAPIコールが不要

2. アップロード方式（`--upload`オプション）
   - PDFファイルを一度サーバーにアップロード
   - 大きなファイルに適している
   - 処理が2段階（アップロード→変換）

## 機能

- PDFファイルのテキスト抽出
- Markdown形式での保存
- コマンドラインインターフェース
- カスタム出力パスのサポート
- 大きなファイルのサポート（アップロード方式）

## テストの実行

テストを実行するには、以下のコマンドを使用します：

```bash
# Makefileを使用してテストを実行（推奨）
make test

# カバレッジレポートを生成する場合
make test-report
```

または、直接pytestを使用することもできます：

```bash
# すべてのテストを実行
pytest

# カバレッジレポート付きでテストを実行
pytest --cov=pdf2md

# 詳細なカバレッジレポートをHTML形式で生成
pytest --cov=pdf2md --cov-report=html
```

テストを実行する前に、必ず開発モードでパッケージをインストール（`pip install -e .`）していることを確認してください。

## ライセンス

MITライセンスの下で公開されています。詳細は[LICENSE](LICENSE)ファイルを参照してください。
