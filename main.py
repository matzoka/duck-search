import streamlit as st
from duck_search import text_search, image_search, news_search
import json
import pandas as pd
from datetime import datetime, timedelta
import os

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

# 検索結果を表示する関数
def display_results(df, search_type):
    if search_type == "画像":
        cols = st.columns(2)
        for i, (_, row) in enumerate(df.iterrows()):
            with cols[i % 2]:
                st.image(row['画像URL'], caption=row['タイトル'])
                url = row['ソースURL']
                st.write(f"[{url}]({url})")
    else:
        for _, row in df.iterrows():
            with st.expander(row['タイトル']):
                st.write(row['内容'])
                url = row['URL']
                st.write(f"[{url}]({url})")

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

# メインコンテナの作成
main_container = st.container()

# セッション状態の初期化
if 'search_results' not in st.session_state:
    st.session_state.search_results = None
if 'current_search_type' not in st.session_state:
    st.session_state.current_search_type = None

# 検索実行
if st.button("検索"):
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
        else:  # ニュース
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
                data.append([
                    result['title'],
                    result['body'],
                    result.get('href', result.get('url', ''))
                ])

        st.session_state.search_results = pd.DataFrame(data[1:], columns=data[0])
        st.session_state.current_search_type = search_type

    except Exception as e:
        st.error(f"検索中にエラーが発生しました: {str(e)}")

# 結果の表示
if st.session_state.search_results is not None:
    with main_container:
        st.write(f"### {st.session_state.current_search_type}検索結果")

        # 結果内検索のUI
        st.write("#### 結果内検索")
        col1, col2 = st.columns([4, 1])
        with col1:
            filter_keyword = st.text_input("検索キーワード（スペース区切りでAND検索）", key="filter")
        with col2:
            case_sensitive = st.checkbox("大文字/小文字を区別", key="case")

        try:
            df = st.session_state.search_results
            filtered_df = df

            if filter_keyword:
                filter_keywords = filter_keyword.split()

                if not case_sensitive:
                    df_lower = df.copy()
                    for col in df.columns:
                        df_lower[col] = df_lower[col].astype(str).str.lower()
                    filter_keywords = [k.lower() for k in filter_keywords]
                    df_to_search = df_lower
                else:
                    df_to_search = df

                mask = pd.Series([True] * len(df))
                for k in filter_keywords:
                    keyword_mask = pd.Series([False] * len(df))
                    for col in df.columns:
                        keyword_mask |= df_to_search[col].astype(str).str.contains(k, na=False)
                    mask &= keyword_mask
                filtered_df = df[mask]

            # 結果表示
            if len(filtered_df) > 0:
                st.write(f"検索結果: {len(filtered_df)}件")
                display_results(filtered_df, st.session_state.current_search_type)

                # ダウンロードボタン用のコンテナ
                download_container = st.container()
                with download_container:
                    col1, col2 = st.columns(2)
                    if file_format == "CSV":
                        with col1:
                            csv = filtered_df.to_csv(index=False, encoding='utf-8-sig')
                            st.download_button(
                                label="CSVとしてダウンロード",
                                data=csv,
                                file_name=f"{keyword}_{st.session_state.current_search_type}_results.csv",
                                mime='text/csv'
                            )
                    else:
                        with col2:
                            filtered_df.to_excel("temp.xlsx", index=False)
                            with open("temp.xlsx", "rb") as f:
                                st.download_button(
                                    label="Excelとしてダウンロード",
                                    data=f,
                                    file_name=f"{keyword}_{st.session_state.current_search_type}_results.xlsx"
                                )
                            if os.path.exists("temp.xlsx"):
                                os.remove("temp.xlsx")
            else:
                st.warning("検索条件に一致する結果が見つかりませんでした。")

        except Exception as e:
            st.error(f"結果内検索中にエラーが発生しました: {str(e)}")
