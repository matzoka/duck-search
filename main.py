import streamlit as st
from duck_search import text_search, image_search, news_search
import json
import pandas as pd
import base64
from io import BytesIO

# ページ設定
st.set_page_config(page_title="Duck Search", layout="wide", page_icon="app.ico")

# Base64でエンコードされた簡単なダック画像
HEADER_IMAGE = """iVBORw0KGgoAAAANSUhEUgAAA+gAAABkCAYAAAAxOQ7zAAAACXBIWXMAAAsTAAALEwEAmpwYAAAF0WlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4gPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iQWRvYmUgWE1QIENvcmUgNy4yLWMwMDAgNzkuMWI2NWE3OWI0LCAyMDIyLzA2LzEzLTIyOjAxOjAxICAgICAgICAiPiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPiA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtbG5zOnhtcE1NPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvbW0vIiB4bWxuczpzdEV2dD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL3NUeXBlL1Jlc291cmNlRXZlbnQjIiB4bWxuczpkYz0iaHR0cDovL3B1cmwub3JnL2RjL2VsZW1lbnRzLzEuMS8iIHhtbG5zOnBob3Rvc2hvcD0iaHR0cDovL25zLmFkb2JlLmNvbS9waG90b3Nob3AvMS4wLyIgeG1wOkNyZWF0b3JUb29sPSJBZG9iZSBQaG90b3Nob3AgMjQuMCAoTWFjaW50b3NoKSIgeG1wOkNyZWF0ZURhdGU9IjIwMjQtMDEtMjVUMTk6MTY6MDErMDk6MDAiIHhtcDpNZXRhZGF0YURhdGU9IjIwMjQtMDEtMjVUMTk6MTY6MDErMDk6MDAiIHhtcDpNb2RpZnlEYXRlPSIyMDI0LTAxLTI1VDE5OjE2OjAxKzA5OjAwIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOjY5ZjM5Y2Y5LTRkYzItNDM5NS05YmI0LTdjZjU3YzM1NzQ5OCIgeG1wTU06RG9jdW1lbnRJRD0iYWRvYmU6ZG9jaWQ6cGhvdG9zaG9wOjIyNzNmZDY1LTY5OTAtNDM0NC05MjQ5LTYzZWE1MzIxNzM5NiIgeG1wTU06T3JpZ2luYWxEb2N1bWVudElEPSJ4bXAuZGlkOjY5ZjM5Y2Y5LTRkYzItNDM5NS05YmI0LTdjZjU3YzM1NzQ5OCIgZGM6Zm9ybWF0PSJpbWFnZS9wbmciIHBob3Rvc2hvcDpDb2xvck1vZGU9IjMiPiA8eG1wTU06SGlzdG9yeT4gPHJkZjpTZXE+IDxyZGY6bGkgc3RFdnQ6YWN0aW9uPSJjcmVhdGVkIiBzdEV2dDppbnN0YW5jZUlEPSJ4bXAuaWlkOjY5ZjM5Y2Y5LTRkYzItNDM5NS05YmI0LTdjZjU3YzM1NzQ5OCIgc3RFdnQ6d2hlbj0iMjAyNC0wMS0yNVQxOToxNjowMSswOTowMCIgc3RFdnQ6c29mdHdhcmVBZ2VudD0iQWRvYmUgUGhvdG9zaG9wIDI0LjAgKE1hY2ludG9zaCkiLz4gPC9yZGY6U2VxPiA8L3htcE1NOkhpc3Rvcnk+IDwvcmRmOkRlc2NyaXB0aW9uPiA8L3JkZjpSREY+IDwveDp4bXBtZXRhPiA8P3hwYWNrZXQgZW5kPSJyIj8+G4GQAAAA2UlEQVR42u3BMQEAAADCoPVPbQZ/oAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOA1v9QAATX68/0AAAAASUVORK5CYII=""".strip()

# タイトルの直前に画像を表示
st.markdown("<style>div.stImage {margin-bottom: 20px;}</style>", unsafe_allow_html=True)
try:
    image_data = base64.b64decode(HEADER_IMAGE)
    st.image(BytesIO(image_data), use_container_width=True)
except Exception as e:
    st.error(f"ヘッダー画像の読み込みに失敗しました: {str(e)}")

# タイトル
st.title("Duck Search App")

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
