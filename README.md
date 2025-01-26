# DuckDuckGo 統合検索ツール

## 概要
Duck Searchは、DuckDuckGo Search APIを使用した検索ツールです。Streamlitを使用しており、直感的なWebインターフェースを提供します。

## 主な機能
- テキスト検索
- 画像検索
- ニュース検索
- ビデオ検索
- AND検索（複数キーワード）
- NG検索（特定キーワード除外）
- 期間指定検索
- ダークモード対応
- 結果内検索（二次フィルタリング）

## 環境要件
- Python 3.8以上
- Windows/macOS/Linux

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

## 使用イメージ
![実行画面](https://github.com/user-attachments/assets/928564bd-575c-4855-803f-1056e79c750c)

## 検索オプション
### 検索タイプ
- 📝テキスト: 一般的なWeb検索。Webページやブログ記事などを検索
- 🖼️画像: 画像専用の検索。画像とその説明、ソースURLを表示
- 📰ニュース: ニュース記事に特化した検索。最新のニュース記事を表示
- 🎥ビデオ: 動画専用の検索。動画のサムネイル、タイトル、再生時間、元ページへのリンクを表示

### キーワード指定
- 通常の検索: キーワードをそのまま入力
- AND検索: スペースで区切って複数のキーワードを指定
- 除外検索:
  - キーワード除外: `-キーワード`（例: 東京 -大阪）
  - サイト除外: `-site:ドメイン名`（例: Python -site:stackoverflow.com）

### 期間指定
- プリセット期間:
  - 指定なし
  - 過去1日
  - 過去1週間
  - 過去1か月
  - 過去1年
- カスタム期間:
  - 開始日と終了日を自由に指定可能
  - 日付範囲での検索が可能（YYYY-MM-DD..YYYY-MM-DD形式）

### その他の設定
- リージョン: 検索対象地域を指定（jp-jp: 日本、wt-wt: グローバル）
- セーフサーチ: 検索結果のフィルタリングレベルを設定
  - off: フィルタリングなし
  - on: 厳格なフィルタリング
  - moderate: 中程度のフィルタリング
- 最大結果数: 1〜50件の範囲で指定
- 出力形式: CSVまたはExcelを選択

### 結果内検索（二次フィルタリング）
- 検索結果に対してさらに絞り込み検索が可能
- 機能:
  - 複数キーワードでAND検索（スペース区切り）
  - 大文字/小文字の区別設定
  - タイトルと本文の両方から検索
- 使用方法:
  1. 通常の検索を実行
  2. 検索結果上部の「結果内検索」セクションでキーワードを入力
  3. 必要に応じて大文字/小文字の区別を設定
  4. 結果が自動的にフィルタリングされる

## 主な依存パッケージ
- streamlit==1.29.0以上
- duckduckgo-search==4.5.0以上
- pandas==2.1.0以上

## 出力形式
検索結果は以下の形式でダウンロード可能:
- CSV (UTF-8 with BOM)
- Excel (.xlsx)

## 特徴
- レスポンシブなWebインターフェース
- システムのダークモード設定に自動対応
- 検索結果のインタラクティブな表示
- 複数の検索オプションによる柔軟な検索
- 検索結果の簡単なエクスポート機能
- カスタム期間指定による詳細な時間範囲検索
- 検索結果に対する二次フィルタリング機能

## 更新履歴
### 2025-01-26
- ビデオ検索機能を追加
  - YouTubeなどの動画コンテンツの検索が可能に
  - サムネイル画像とビデオ情報の表示機能
  - 再生時間の表示
  - 動画ページへの直接リンク
- 結果内検索機能の改善
  - 絞り込みボタンを廃止し、リアルタイムフィルタリングを実装
  - 検索結果の表示を最適化
  - セッション状態の管理を改善
  - エラーハンドリングを強化
- 検索タイプに絵文字を追加
  - 📝テキスト検索
  - 🖼️画像検索
  - 📰ニュース検索
  - 🎥ビデオ検索

## ライセンス
