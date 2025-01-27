import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os
import time

def is_same_domain(base_url, target_url):
    """
    base_urlとtarget_urlのドメインが同じかどうかをチェックする関数
    """
    base_domain = urlparse(base_url).netloc
    target_domain = urlparse(target_url).netloc
    return base_domain == target_domain

def get_links(url, base_url):
    """
    指定したurlのページを取得し、HTML内のリンクを全て返す関数。
    同じドメインのリンクのみ返すようにフィルタ。
    """
    links = []
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # aタグのhrefを全て取得
            for a_tag in soup.find_all('a', href=True):
                link = urljoin(url, a_tag['href'])
                # 同じドメインのリンクのみ返す
                if is_same_domain(base_url, link):
                    links.append(link)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
    return links

def save_html(url, output_dir):
    """
    指定したURLのHTMLを取得し、output_dir配下にファイルとして保存する関数。
    ファイル名はURLを安全に変換したものを使う。
    """
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            # URLをファイル名に使えるよう変換
            parsed = urlparse(url)
            # パスやクエリを含めてファイル名にする例（長くなるので工夫が必要）
            safe_path = parsed.path.replace('/', '_') or '_root'
            safe_query = parsed.query.replace('=', '_').replace('&', '_')
            # 拡張子をhtmlにする
            if safe_query:
                file_name = f"{parsed.netloc}{safe_path}_{safe_query}.html"
            else:
                file_name = f"{parsed.netloc}{safe_path}.html"

            file_path = os.path.join(output_dir, file_name)
            # ディレクトリがなければ作成
            os.makedirs(output_dir, exist_ok=True)

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(response.text)

            print(f"Saved: {file_path}")
    except requests.exceptions.RequestException as e:
        print(f"Error saving {url}: {e}")

def crawl_domain(start_url, output_dir="downloaded_pages"):
    """
    start_urlを起点に、同じドメインのリンクを再帰的(またはBFS的)にクロールし、
    HTMLを保存する関数。
    """
    visited = set()
    to_visit = [start_url]

    while to_visit:
        url = to_visit.pop(0)
        if url in visited:
            continue
        visited.add(url)

        # HTMLを保存
        save_html(url, output_dir)

        # 短いウェイトを入れる（サーバーへの負荷軽減）
        time.sleep(1)

        # 同じドメインのリンクを取得
        new_links = get_links(url, start_url)
        for link in new_links:
            if link not in visited:
                to_visit.append(link)

    print("クロール完了")

if __name__ == "__main__":
    # 例: "https://example.com" を起点に同じドメインのHTMLを全取得する
    start_url = "https://www.preferred.jp/ja/"
    crawl_domain(start_url)
