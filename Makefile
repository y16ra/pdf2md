.PHONY: help test lint format check clean install install-dev

help: ## このヘルプを表示する
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

install: ## 本番用の依存関係をインストール
	pip install -r requirements.txt

install-dev: ## 開発用の依存関係をインストール
	pip install -r requirements-dev.txt

test: ## テストを実行
	pytest -v --cov=pdf2md tests/

test-report: ## テストを実行してカバレッジレポートを生成
	pytest -v --cov=pdf2md --cov-report=html tests/

lint: ## コードの静的解析を実行
	flake8 src/pdf2md tests
	mypy src/pdf2md

format: ## コードをフォーマット
	black src/pdf2md tests
	isort src/pdf2md tests

check: lint test ## 静的解析とテストを実行

clean: ## 一時ファイルを削除
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type f -name ".DS_Store" -delete 
