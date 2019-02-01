    
# -*- coding: UTF-8 -*-

import requests
import os

import sys

reload(sys)
sys.setdefaultencoding("utf-8")

def get_image_pages(keyword, pages):
    params = []
    for i in range(30, 30 * pages + 30, 30):
        params.append({
            'tn': 'resultjson_com',
            'ipn': 'rj',
            'ct': 201326592,
            'is': '',
            'fp': 'result',
            'queryWord': keyword,
            'cl': 2,
            'lm': -1,
            'ie': 'utf-8',
            'oe': 'utf-8',
            'adpicid': '',
            'st': -1,
            'z': '',
            'ic': 0,
            'word': keyword,
            's': '',
            'se': '',
            'tab': '',
            'width': '',
            'height': '',
            'face': 0,
            'istype': 2,
            'qc': '',
            'nc': 1,
            'fr': '',
            'pn': i,
            'rn': 30,
            'gsm': '1e',
            '1488942260214': ''
        })

    url = 'https://image.baidu.com/search/acjson'

    urls = []
    for i in params:
        try:
            baidu_resp = requests.get(url, params=i)
            if baidu_resp.status_code == 200:
                photo_json = baidu_resp.json()
                image_data_urls = photo_json.get('data')
                urls.append(image_data_urls)
            else:
                print(u'open baidu [%s] search linke error, status code=%d, content is %s' % (
                    keyword, baidu_resp.status_code, baidu_resp.text))
        except requests.ConnectionError as e:
            print(u'Error open baidu [%s] photo search link' % keyword, e.args)
        except ValueError as ve:
            print(u'Error parse baidu [%s] photo search link' % keyword, ve.args)
    return urls


def download_image(file_dir, url_list, local_file):
    file_path = '%s/%s' % (local_file, file_dir)
    if not os.path.exists(file_path):
        os.mkdir(file_path)

    x = 0
    for urls in url_list:
        for i in urls:
            image_url = i.get('thumbURL')

            if image_url is not None:
                print(u'正在下载[%s]：%s' % (file_dir, image_url))
                ir = requests.get(image_url)
                open(file_path + '/%d.jpg' % x, 'wb').write(ir.content)
                x += 1
            else:
                print(u'%s图片链接不存在' % image_url)


if __name__ == '__main__':
    # 需要爬取的明星
    mx_names = [u'杨幂', u'江疏影', u'迪丽热巴', u'孙俪', u'古力娜扎', u'赵丽颖', u'李成敏', 'anglebaby', u'鞠婧祎']
    # 爬取图片保存到本地的地址
    local_file_dir = '/Users/macwink/Downloads/images'
    # 总共爬取多少页
    image_pages = 5
    for mx_name in mx_names:
        image_url_list = get_image_pages(mx_name, image_pages)
        download_image(mx_name, image_url_list, local_file_dir)