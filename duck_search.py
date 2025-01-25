from duckduckgo_search import DDGS
import json

def text_search(keyword, region='jp-jp', safesearch='off', timelimit=None, max_results=4):
    with DDGS() as ddgs:
        results = list(ddgs.text(
            keywords=keyword,
            region=region,
            safesearch=safesearch,
            timelimit=timelimit,
            max_results=max_results
        ))
        return results

def and_search(keyword1, keyword2, region='jp-jp', safesearch='off', timelimit=None, max_results=4):
    with DDGS() as ddgs:
        results = list(ddgs.text(
            keywords=f'{keyword1} {keyword2}',
            region=region,
            safesearch=safesearch,
            timelimit=timelimit,
            max_results=max_results
        ))
        return results

def ng_search(keyword, ng_keyword, region='jp-jp', safesearch='off', timelimit=None, max_results=4):
    with DDGS() as ddgs:
        results = list(ddgs.text(
            keywords=f'{keyword} -{ng_keyword}',
            region=region,
            safesearch=safesearch,
            timelimit=timelimit,
            max_results=max_results
        ))
        return results

def date_range_search(keyword, start_date, end_date, region='jp-jp', safesearch='off', max_results=4):
    with DDGS() as ddgs:
        results = list(ddgs.text(
            keywords=keyword,
            region=region,
            safesearch=safesearch,
            timelimit=f'{start_date}..{end_date}',
            max_results=max_results
        ))
        return results

def image_search(keyword, region='jp-jp', safesearch='off', timelimit=None, max_results=4):
    with DDGS() as ddgs:
        results = list(ddgs.images(
            keywords=keyword,
            region=region,
            safesearch=safesearch,
            timelimit=timelimit,
            max_results=max_results
        ))
        return results

def news_search(keyword, region='jp-jp', safesearch='off', timelimit=None, max_results=4):
    with DDGS() as ddgs:
        results = list(ddgs.news(
            keywords=keyword,
            region=region,
            safesearch=safesearch,
            timelimit=timelimit,
            max_results=max_results
        ))
        return results

def print_results(results):
    for result in results:
        print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    # 使用例
    print('=== 基本検索 ===')
    results = text_search('東京')
    print_results(results)

    print('\n=== AND検索 ===')
    results = and_search('東京', '大阪')
    print_results(results)

    print('\n=== NG検索 ===')
    results = ng_search('東京', '東京都')
    print_results(results)

    print('\n=== 期間指定検索 ===')
    results = date_range_search('東京', '2024-01-01', '2024-01-07')
    print_results(results)

    print('\n=== 画像検索 ===')
    results = image_search('東京')
    print_results(results)

    print('\n=== ニュース検索 ===')
    results = news_search('東京')
    print_results(results)
