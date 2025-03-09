import argparse
from pathlib import Path
from .converter import PDF2MarkdownConverter

def main():
    parser = argparse.ArgumentParser(description='PDFファイルをMarkdownに変換します')
    parser.add_argument('pdf_path', type=str, help='入力PDFファイルのパス')
    parser.add_argument('--output', '-o', type=str, help='出力Markdownファイルのパス（オプション）')
    parser.add_argument('--upload', '-u', action='store_true', help='ファイルをアップロードして変換（大きなファイル向け）')
    
    args = parser.parse_args()
    
    try:
        converter = PDF2MarkdownConverter()
        if args.upload:
            output_path = converter.convert_with_upload(args.pdf_path, args.output)
        else:
            output_path = converter.convert(args.pdf_path, args.output)
        print(f"変換が完了しました。出力ファイル: {output_path}")
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")
        exit(1)

if __name__ == '__main__':
    main() 
