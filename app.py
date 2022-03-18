from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
app = Flask(__name__)

headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'en,mr;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}


@app.route('/')
def index():
    return "<h1>Home Page</h1>"


@app.route('/search', methods=['GET'])
def search():
    stock = request.args.get("stock", None)
    print(f"got stock {stock}")

    url = f"https://www.marketwatch.com/investing/stock/{stock}?mod=over_search"
    req = requests.get(url, headers=headers, timeout=5, verify=False)
    soup = BeautifulSoup(req.content, 'html.parser')

    price = soup.body.find('bg-quote', class_="value").text
    print(price)

    response = {}
    if not stock:
        response["ERROR"] = "no name found, please send a name."
    elif str(stock).isdigit():
        response["ERROR"] = "name can't be numeric."
    else:
        response["stock_price"] = f"{price}"
    return jsonify(response)


if __name__ == "__main__":
    app.run()