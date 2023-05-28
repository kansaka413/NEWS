from flask import Flask, jsonify
from flask_cors import CORS
import urllib.request as req
import bs4

# 初始化 Flask 應用
app = Flask(__name__)
CORS(app)  # 允許跨域請求

@app.route('/api/news', methods=['GET'])
def get_news():
    # 設定要抓取的網頁 URL
    url="https://edition.cnn.com/world"

    # 建立一個 Request 物件，附加 Request Headers 的資訊，模擬瀏覽器訪問
    request=req.Request(url, headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    })

    # 使用 urllib.request.urlopen 打開網頁，並將響應對象存儲在 response 中
    with req.urlopen(request) as response:
        # 讀取 response 中的內容，並解碼為 utf-8 格式，將結果存儲在變數 data 中
        data=response.read().decode("utf-8")

    # 使用 BeautifulSoup 解析 HTML，並將結果存儲在變數 root 中
    root=bs4.BeautifulSoup(data, "html.parser")

    # 使用 BeautifulSoup 的 find_all 方法找到所有 class 為 "card container__item container__item--type-section container_lead-plus-headlines__item container_lead-plus-headlines__item--type-section" 的 div 標籤
    articles=root.find_all("div", class_="card container__item container__item--type-section container_lead-plus-headlines__item container_lead-plus-headlines__item--type-section")

    news = []

    # 迭代每一個找到的 div 標籤
    for article in articles:
        # 在每個 div 標籤中找到 class 為 "container__headline container_lead-plus-headlines__headline" 的 div 標籤，並將結果存儲在變數 title 中
        title = article.find("div", class_="container__headline container_lead-plus-headlines__headline")
        # 如果找到了 title
        if title:
            news.append({
                'title': title.span.string,
                'link': 'https://edition.cnn.com' + article.a['href']
            })

    # 將新聞列表轉換為 JSON 格式並返回
    return jsonify(news)

if __name__ == '__main__':
    app.run(debug=True)