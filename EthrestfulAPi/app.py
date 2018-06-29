from flask import Flask

from urllib.request import Request, urlopen
import json
from flask import jsonify
from flask import Response
from flask import make_response

app = Flask(__name__, static_url_path='')



@app.route('/getjson')
def get_json():
    k_line_url = "http://api.bitkk.com/data/v1/kline?market=eth_usdt&times=1hour"
    firefox_headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Accept': 'text/html, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36',
    }
    # 构建请求
    request = Request(k_line_url, headers=firefox_headers)
    html = urlopen(request)
    data = html.read()  # .decode('gbk')
    data_json = json.loads(data)
    response = make_response(jsonify(response=data_json))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'

    return response
@app.route('/getrealprice')
def get_real_price():
    # zb网站获取数据Api
    url = "https://trans.bitkk.com/line/topall?area=&jsoncallback=jQuery191025699015513536727_1530079609291&_=1530079609293"
    # 包装头部
    firefox_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    # 构建请求
    request = Request(url, headers=firefox_headers)
    html = urlopen(request)
    # 获取数据
    data = html.read()
    # 转换成字符串
    strs = str(data)
    # 截取字符串
    print(len(strs))
    strs_for_json = strs[44:]
    strs_for_json = strs_for_json[:-2]
    print(strs_for_json)
    # 转换成JSON
    data = strs_for_json
    datas = json.dumps(data)
    # 转换成字典数据

    data_json = json.loads(data)
    print(type(data_json))  # <class 'dict'>
    print(data_json['datas'][0]['market'], data_json['datas'][0]['sell1Price'])
    print(len(data_json['datas']))
    lens = len(data_json['datas'])
    for i in range(0, lens):

        if(data_json['datas'][i]['market']=="ETH/USDT"):
            eth_json_dict = {}
            eth_json_dict['market']=data_json['datas'][i]['market']
            eth_json_dict['sell1Price'] = data_json['datas'][i]['sell1Price']
            eth_json_dict['hightPrice'] = data_json['datas'][i]['hightPrice']
            eth_json_dict['lastPrice'] = data_json['datas'][i]['lastPrice']
            eth_json_dict['riseRate'] = data_json['datas'][i]['riseRate']
            eth_json_dict['vol'] = data_json['datas'][i]['vol']
            response = make_response(jsonify(response=eth_json_dict))
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'POST'
            response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'

            return response
@app.route('/')
def index():
    return app.send_static_file('eth.html')

if __name__ == '__main__':
    app.run()
