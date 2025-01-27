# README

指定したURL（同一ドメイン）配下のHTMLをすべて保存するシンプルなPythonクローラーのサンプル実装です。

---

## 概要

- **目的**  
  指定したURLを起点に、同一ドメイン内にあるすべてのHTMLページを再帰的（あるいはBFS的）に巡回し、HTMLファイルとして保存します。

- **特徴**  
  - `requests` と `BeautifulSoup` を使用したシンプルな実装  
  - 同じURLを何度もクロールしないように `visited` セットで管理  
  - ドメインが異なるリンクは無視  
  - URLを簡易的にファイル名に変換し、`downloaded_pages` ディレクトリへ保存

---

## 動作環境

- Python 3.7 以上（推奨）
- インストールが必要な主要ライブラリ
  - [requests](https://pypi.org/project/requests/)
  - [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)

```bash
pip install requests beautifulsoup4
```

---

## 使い方

1. **ファイルの配置**  
   付属のスクリプト（例：`crawler.py`）を任意のフォルダに配置してください。

2. **スクリプトの編集**  
   `crawl_domain` 関数で定義されている `start_url` を、クロール開始地点としたいURLに変更してください。

   ```python
   if __name__ == "__main__":
       start_url = "https://example.com"  # 任意のURLを指定
       crawl_domain(start_url)
   ```

3. **実行**  

   ```bash
   python crawler.py
   ```

4. **結果の確認**  
   実行すると、`downloaded_pages` ディレクトリが自動的に作成され、その中にHTMLファイルが保存されます。  
   保存されるファイル名は、URLをファイルシステムに適した形に変換したものを用いています。  
   （ファイル名を工夫する場合は、`save_html` 関数内の命名ロジックを変更してください。）

---

## 主要関数説明

- **`crawl_domain(start_url, output_dir="downloaded_pages")`**  
  - `start_url` から同一ドメイン内のURLを再帰的にクロールし、HTMLを保存  
  - 一度クロールしたURLは `visited` セットに記録し、重複クロールを防止  
  - 保存場所は `output_dir`（デフォルト`downloaded_pages`）  

- **`save_html(url, output_dir)`**  
  - `url` のHTMLを取得し、ファイルとして保存  
  - URLをパースしてファイル名を生成し、`output_dir` に保存  

- **`get_links(url, base_url)`**  
  - `url` にあるすべてのリンク（`a` タグの `href`）を取得  
  - `base_url` と同じドメインのリンクだけを抽出して返す  

- **`is_same_domain(base_url, target_url)`**  
  - `urlparse` を使い、ドメイン（`netloc`）が一致しているかを判定  

---

## 注意事項

1. **robots.txt・利用規約の確認**  
   クローリングの対象サイトがクローリング許可されているかどうか、必ず事前に確認してください。利用規約に抵触したり、サーバーに過度の負荷をかける行為は厳禁です。

2. **リクエスト間隔・負荷対策**  
   `time.sleep(1)` などで遅延を入れていますが、大規模サイトをクロールする場合はリクエストの間隔や深さ制限を調整し、サーバーに過度の負荷を与えないよう配慮しましょう。

3. **ファイル名の長さ**  
   URLによってはファイル名が非常に長くなる場合があります。OSによってはファイル名の制限に引っかかることがあるため、必要に応じてハッシュ化などの命名ロジックを導入することを推奨します。

4. **動的コンテンツの取得**  
   本サンプルでは静的なHTMLページを想定しています。JavaScriptで動的に生成される要素をクロール・解析したい場合は、[Selenium](https://pypi.org/project/selenium/) などを活用する方法をご検討ください。

5. **無限ループ・ループリンク対策**  
   サイトの作りによってはループリンクや大量の重複URL、無限に生成されるURLが存在する可能性があります。`visited` セットで対策はしていますが、より高度な除外ロジックや最大深度設定などが必要なケースもあります。

---

## ライセンス

このサンプルコードは、学習・研究目的での利用を想定しています。  
商用利用や公開・配布の際は、必ず[MIT License](https://opensource.org/licenses/MIT)等をご検討ください。

---

## 開発者向けメモ

- **コードの拡張**  
  - robots.txtのチェック機能を実装して、クロールが許可されていないURLを除外する  
  - 並列処理（マルチスレッド・マルチプロセス）でクロール速度を向上させる  
  - HTML以外（PDFなどのファイル）も取得したい場合には、`Content-Type` チェック等を導入する  

- **テスト**  
  - 小規模かつ構造がシンプルなテストサイトを用意して動作検証することを推奨  
  - エッジケースとして、誤ったURLやアクセス不能なURLなどを与えて動作をテスト  

---

以上でREADMEです。どうぞご利用ください。
