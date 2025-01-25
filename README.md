# Duck Search プロジェクト

## 概要
Duck Searchは、DuckDuckGo Search APIを使用した検索ツールです。Streamlitを使用しており、直感的なWebインターフェースを提供します。

## 主な機能
- テキスト検索
- 画像検索
- ニュース検索
- AND検索（複数キーワード）
- NG検索（特定キーワード除外）
- 期間指定検索

## インストール方法
1. リポジトリをクローン:
   ```bash
   git clone https://github.com/matzoka/duck-search.git
   ```
2. 依存関係をインストール:
   ```bash
   pip install -r requirements.txt
   ```

## 使用方法
1. プロジェクトディレクトリに移動:
   ```bash
   cd duck-search
   ```
2. アプリケーションを起動:
   ```bash
   streamlit run main.py
   ```
3. ブラウザで表示されるインターフェースを使用して検索を実行

## 検索オプション
- 検索タイプ: テキスト、画像、ニュースから選択
- リージョン: 検索対象地域を指定
- セーフサーチ: 検索結果のフィルタリングレベルを設定
- 最大結果数: 1〜50件の範囲で指定
- 出力形式: CSVまたはExcelを選択

## 出力形式
検索結果は以下の形式でダウンロード可能:
- CSV
- Excel

## 画像イメージ
![Image](https://github.com/user-attachments/assets/f1828eed-a182-4656-99e5-b8207c58fb4a)

## ライセンス
このプロジェクトはMITライセンスの下で公開されています。詳細はLICENSEファイルをご覧ください。
