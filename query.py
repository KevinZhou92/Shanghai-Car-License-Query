import requests
import js2py
import json
import os
from pygments import highlight, lexers, formatters


def get_vali_code(image_content):
    with open('./test.jpg', 'wb') as f:
        f.write(image_content)

    return input('Please type vali code, image is stored at' + os.getcwd()  + ': \n')

def get_bid_result(bid_id, last4_of_id):
    print(f'-> Query bid id is {bid_id}, last 4 digit of id is {last4_of_id}')
    random_number = js2py.eval_js("Math.random()")
    print(f'-> Random Number is {random_number}')
    headers = {
        'Referer': 'https://pmcx.alltobid.com/gpcarquery.web/home/personal',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    val_code_url = 'https://pmcx.alltobid.com/GPCarQuery.Web/Image/ValiCode?r=' + str(random_number)
    response = requests.get(val_code_url, headers=headers)
    session_id, image_content = response.cookies, response.content

    vali_code = get_vali_code(image_content)

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'If-Modified-Since': '0',
        'Origin': 'https://pmcx.alltobid.com',
        'Referer': 'https://pmcx.alltobid.com/gpcarquery.web/home/personal',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    }

    data = {
        'idcard': last4_of_id,
        'number': bid_id,
        'type': 2,
        'code': vali_code 
    }

    url = 'https://pmcx.alltobid.com/GPCarQuery.Web/Home/Query'
    result = requests.post(url, headers=headers, data=data, cookies=session_id).json()
    query_status = result['code']

    result['NeedPay'] = '是' if result['NeedPay'] == 1 else '否'
    customer_name, bid_count, expire_date, success_bid, bid_time = result['ClientName'], result['used'], result['validdate'], result['NeedPay'], result['AucTime']
    result = {
        '客户姓名': customer_name,
        '投标次数': bid_count,
        '是否中标': success_bid,
        '有效日期': expire_date
    }

    formatted_json = json.dumps(result, indent=4, ensure_ascii=False).encode('utf8')
    colorful_json = highlight(formatted_json, lexers.JsonLexer(), formatters.TerminalFormatter())
    print(colorful_json)
    
    return customer_name, bid_count, expire_date, success_bid, bid_time, query_status
