import streamlit as st
from duck_search import text_search, image_search, news_search
import json
import pandas as pd
from datetime import datetime, timedelta

# ページ設定
st.set_page_config(page_title="Duck Search", layout="wide", page_icon="app.ico")

# タイトルのスタイルとデザイン
st.markdown("""
    <style>
        .title-container {
            background-color: #f5f5f5;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 20px;
        }
        .title-text {
            color: #333333;
            font-size: 2.5em;
            font-weight: bold;
            font-family: sans-serif;
        }
        @media (prefers-color-scheme: dark) {
            .title-container {
                background-color: #262626;
            }
            .title-text {
                color: #ffffff;
            }
        }
    </style>
    <div class="title-container">
        <div class="title-text">🦆 Duck Search</div>
    </div>
    """, unsafe_allow_html=True)

# サイドバー
with st.sidebar:
    st.header("検索設定")
    search_type = st.selectbox(
        "検索タイプ",
        ["テキスト", "画像", "ニュース"],
        help="""
        検索タイプの説明:
        - テキスト: 一般的なWeb検索。Webページやブログ記事などを検索します。
        - 画像: 画像専用の検索。画像とその説明、ソースURLが表示されます。
        - ニュース: ニュース記事に特化した検索。最新のニュース記事が表示されます。
        """
    )
    keyword = st.text_input(
        "検索キーワード",
        value="教師　なり方",
        help="""
        検索キーワードの指定方法:
        - 除外ワード指定: キーワードの前に「-」を付ける
          例: 東京 -大阪（「東京」を含み「大阪」を含まない）
        - サイト除外: -site:ドメイン名
          例: Python -site:stackoverflow.com
        """
    )
    timelimit = st.selectbox(
        "期間",
        ["指定なし", "過去1日", "過去1週間", "過去1か月", "過去1年", "カスタム期間"],
        index=0,
        help="カスタム期間を選択すると、開始日と終了日を指定できます。"
    )

    # カスタム期間の日付選択
    custom_date_range = None
    if timelimit == "カスタム期間":
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("開始日", datetime.now() - timedelta(days=7))
        with col2:
            end_date = st.date_input("終了日", datetime.now())

        if start_date and end_date:
            if start_date <= end_date:
                custom_date_range = f"{start_date}..{end_date}"
            else:
                st.error("開始日は終了日より前の日付を選択してください。")

    region = st.selectbox(
        "リージョン",
        ["jp-jp", "wt-wt"],
        index=0,
        help="""
        検索対象の地域設定:
        - jp-jp: 日本からの検索結果を優先（日本語コンテンツが中心）
        - wt-wt: 全世界からの検索結果（地域を限定しない）
        """
    )
    safesearch = st.selectbox(
        "セーフサーチ",
        ["off", "on", "moderate"],
        index=0,
        help="""
        検索結果のフィルタリング設定:
        - off: フィルタリングなし（すべての検索結果を表示）
        - on: 厳格なフィルタリング（成人向けコンテンツを除外）
        - moderate: 中程度のフィルタリング（過度な成人向けコンテンツのみ除外）
        """
    )
    file_format = st.selectbox(
        "出力形式",
        ["Excel", "CSV"]
    )
    max_results = st.slider("最大結果数", 1, 50, 50)

# 期間の設定を変換
timelimit_map = {
    "指定なし": None,
    "過去1日": "d",
    "過去1週間": "w",
    "過去1か月": "m",
    "過去1年": "y"
}

# カスタム期間の場合は日付範囲を使用
final_timelimit = custom_date_range if timelimit == "カスタム期間" else timelimit_map.get(timelimit)

# 検索実行
if st.button("検索"):
    st.write(f"### {search_type}検索結果: {keyword}")

    try:
        if search_type == "テキスト":
            results = text_search(
                keyword=keyword,
                region=region,
                safesearch=safesearch,
                timelimit=final_timelimit,
                max_results=max_results
            )
        elif search_type == "画像":
            results = image_search(
                keyword=keyword,
                region=region,
                safesearch=safesearch,
                timelimit=final_timelimit,
                max_results=max_results
            )
        elif search_type == "ニュース":
            results = news_search(
                keyword=keyword,
                region=region,
                safesearch=safesearch,
                timelimit=final_timelimit,
                max_results=max_results
            )

        # データ準備
        if search_type == "画像":
            data = [["タイトル", "画像URL", "ソースURL"]]
            for result in results:
                data.append([result['title'], result['image'], result['url']])
        else:
            data = [["タイトル", "内容", "URL"]]
            for result in results:
                data.append([result['title'], result['body'],
                               result.get('href', result.get('url', ''))])

        df = pd.DataFrame(data[1:], columns=data[0])

        # 結果表示
        if search_type == "画像":
            cols = st.columns(2)
            for i, result in enumerate(results):
                with cols[i % 2]:
                    st.image(result['image'], caption=result['title'])
                    url = result['url']
                    st.write(f"[{url}]({url})")
        else:
            for result in results:
                with st.expander(result['title']):
                    st.write(result['body'])
                    url = result.get('href', result.get('url', ''))
                    st.write(f"[{url}]({url})")

        # ダウンロードボタン
        if file_format == "CSV":
            file = f"{keyword}_{search_type}_results.csv"
            csv = df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="CSVとしてダウンロード",
                data=csv,
                file_name=file,
                mime='text/csv',
            )
        else:
            file = f"{keyword}_{search_type}_results.xlsx"
            df.to_excel(file, index=False)
            with open(file, "rb") as f:
                st.download_button("Excelとしてダウンロード", f, file_name=file)

    except Exception as e:
        st.error(f"検索中にエラーが発生しました: {str(e)}")
