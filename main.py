import streamlit as st
from duck_search import text_search, image_search, news_search
import json
import pandas as pd

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
        ["テキスト", "画像", "ニュース"]
    )
    keyword = st.text_input("検索キーワード", "教師　なり方")
    region = st.selectbox(
        "リージョン",
        ["jp-jp", "wt-wt"],
        index=0
    )
    safesearch = st.selectbox(
        "セーフサーチ",
        ["off", "on", "moderate"],
        index=0
    )
    file_format = st.selectbox(
        "出力形式",
        ["Excel", "CSV"]
    )
    max_results = st.slider("最大結果数", 1, 50, 50)

# 検索実行
if st.button("検索"):
    st.write(f"### {search_type}検索結果: {keyword}")

    try:
        if search_type == "テキスト":
            results = text_search(
                keyword=keyword,
                region=region,
                safesearch=safesearch,
                max_results=max_results
            )
        elif search_type == "画像":
            results = image_search(
                keyword=keyword,
                region=region,
                safesearch=safesearch,
                max_results=max_results
            )
        elif search_type == "ニュース":
            results = news_search(
                keyword=keyword,
                region=region,
                safesearch=safesearch,
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
                    st.write(f"[ソース]({result['url']})")
        else:
            for result in results:
                with st.expander(result['title']):
                    st.write(result['body'])
                    st.write(f"[リンク]({result['href']})" if 'href' in result else f"[リンク]({result['url']})")

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
