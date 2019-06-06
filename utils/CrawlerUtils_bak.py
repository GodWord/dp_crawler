# -*- coding:utf-8 -*
import logging
import math
import re

import lxml.html as H
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger('utils')
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Host': 'www.dianping.com',
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36",
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Cookie': '_lxsdk_cuid=168ff1b1f28c8-0530d22c516dd5-4313362-1fa400-168ff1b1f28c8; _lxsdk=168ff1b1f28c8-0530d22c516dd5-4313362-1fa400-168ff1b1f28c8; _hc.v=1fbb6612-4867-971e-f3e0-f654067f7ced.1550468194; s_ViewType=10; ua=dpuser_84171807103; ctu=63d65f0d1425edfa29563fb26d584e80c15f18d963633def6a89adea59e9c08b; dper=303e94eeb39c0d5bc3897c53b39c6022cd9263098a23e298bda93bc90beee886db69fb0354af62bf419882a2d1caf70107ab1123b14f3b6897794338913f5cebdc6f0989b7bce0279a32499a118748840f74a5aa92c96b0c649ee3683440909b; ll=7fd06e815b796be3df069dec7836c3df; aburl=1; cy=6; cye=suzhou; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_s=1693186dc03-eeb-f64-c4a%7C%7C616',
    'Proxy-Connection': 'keep-alive'
}

headers2 = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36",
    "Cookie": "cy=9; cye=chongqing; _lxsdk_cuid=168ff1b1f28c8-0530d22c516dd5-4313362-1fa400-168ff1b1f28c8; _lxsdk=168ff1b1f28c8-0530d22c516dd5-4313362-1fa400-168ff1b1f28c8; _hc.v=1fbb6612-4867-971e-f3e0-f654067f7ced.1550468194; s_ViewType=10; ua=dpuser_84171807103; ctu=63d65f0d1425edfa29563fb26d584e80c15f18d963633def6a89adea59e9c08b; dper=303e94eeb39c0d5bc3897c53b39c6022cd9263098a23e298bda93bc90beee886db69fb0354af62bf419882a2d1caf70107ab1123b14f3b6897794338913f5cebdc6f0989b7bce0279a32499a118748840f74a5aa92c96b0c649ee3683440909b; ll=7fd06e815b796be3df069dec7836c3df; _lx_utm=utm_source%3Dgoogle%26utm_medium%3Dorganic; _lxsdk_s=1690eee42f0-866-1d-f77%7C%7C1218"
}


class CrawlerUtils(object):

    @staticmethod
    def get_user_agent():
        import random
        user_agents = [
            'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
            'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
            'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
            'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
        ]
        # 随机返回一个user_agent
        return user_agents[random.randint(0, len(user_agents) - 1)]

    @staticmethod
    def get_headers(cookies):
        headers2['User-Agent'] = CrawlerUtils.get_user_agent()
        headers2['Cookie'] = cookies
        return headers2

    @staticmethod
    def get_html(url, headers=None, **kwargs):
        """
        获取url的html结构
        :param url: 请求的url
        :param headers: 模拟headers,默认为None
        :param kwargs: 其他参数
        :return:
        """
        import requests
        import logging
        # 请求页面
        req = requests.get(url, headers=headers, **kwargs)
        # 将页面编码设置为框架推荐编码
        req.encoding = req.apparent_encoding

        try:
            print(req.url)
            # 获取请求状态码，若状态码不为200则抛出异常，正常返回数据
            req.raise_for_status()
            return req.text
        except Exception as e:
            logging.error(e)
            # 返回请求错误的状态码
            return req.status_code

    @staticmethod
    def get_md5_value(value):
        import hashlib
        # 将字符串转成md5
        md5 = hashlib.md5()  # 获取一个MD5的加密算法对象
        md5.update(value.encode("utf8"))  # 得到MD5消息摘要
        md5_vlaue = md5.hexdigest()  # 以16进制返回消息摘要，32位
        return md5_vlaue

    @staticmethod
    def get_css_and_px_dict(css_url):
        """
        获取css对应名与像素的映射
        :param css_url:css请求的url
        :return:
        """
        # 请求css页面，并取其content编码格式化为utf-8
        con = requests.get(css_url, headers=headers2).content.decode("utf-8")
        # 正则匹配所有css对应名与像素的映射
        find_datas = re.findall(r'(\.[a-zA-Z0-9-]+)\{background:(\-\d+\.\d+)px (\-\d+\.\d+)px', con)
        # 定义字典用于存放结果
        css_name_and_px = {}
        for data in find_datas:
            # 属性对应的值
            span_class_attr_name = data[0][1:]
            # 偏移量
            offset = data[1]
            # 阈值
            position = data[2]
            css_name_and_px[span_class_attr_name] = [offset, position]
        return css_name_and_px

    @staticmethod
    def get_tag(_list, offset=1):
        """
        用递归方法获取_list中所有类名的共同前缀
        :param _list:类名列表
        :param offset:共同部分字符长度
        :return:
        """
        # 用列表生成式是生成长度为offset列表，如['acd','aef'],在offset时=1，结果为:['a'，'a'],在offset时=2，结果为:['ac'，'ae']
        _new_list = [data[0:offset] for data in _list]
        # 当列表中元素去重之后只剩一个时，代表当前offset下，所有类名前缀是相同的
        if len(set(_new_list)) == 1:
            # 说明全部重复,offset自加1
            offset += 1
            # 递归调用该方法
            return CrawlerUtils.get_tag(_list, offset)
        else:
            # 当列表中元素不统一的时候，求列名在offset - 1下的列表，并取第一个
            _return_data = [data[0:offset - 1] for data in _list][0]
            return _return_data

    @staticmethod
    def get_css(content):
        # 用正则匹配css的url
        matched = re.search(r'href="([^"]+svgtextcss[^"]+)"', content, re.M)
        if not matched:
            # 当找不到css_url时抛出异常
            raise Exception("cannot find svgtextcss file")
        # 取出css_url
        css_url = matched.group(1)
        # 由于取出的css_url没有https:前缀，需手动加上
        css_url = "https:" + css_url
        return css_url

    @staticmethod
    def get_svg_threshold_and_int_dict(css_url, _add_res, _tag, is_num=True):
        con = requests.get(css_url, headers=headers2).content.decode("utf-8")
        index_and_word_dict = {}
        # 根据tag值匹配到相应的svg的网址
        find_svg_url = re.search(r'span\[class\^="%s"\].*?background\-image: url\((.*?)\);' % _tag, con)
        if not find_svg_url:
            raise Exception("cannot find svg file, check")
        svg_url = find_svg_url.group(1)
        svg_url = "https:" + svg_url
        svg_content = requests.get(svg_url, headers=headers2).content.decode('utf-8')
        last = 0
        if is_num:  # 当svg里面是数字时
            svg_doc = H.document_fromstring(svg_content)
            datas = svg_doc.xpath("//text")
            # 把阈值和对应的数字集合放入一个字典中
            for index, data in enumerate(datas):
                y = int(data.xpath('@y')[0])
                int_set = data.xpath('text()')[0]
                index_and_word_dict[int_set] = range(last, y + 1)
                last = y
            return index_and_word_dict
        else:  # 当svg里面是数字时
            svg_doc = BeautifulSoup(svg_content, "html.parser")
            all_y_values = svg_doc.findAll("path")
            all_y_dict = {}
            for _y in all_y_values:
                all_y_dict["#" + str(_y.attrs['id'])] = str(_y.attrs['d']).split(' ')[1]
            datas = svg_doc.findAll("textpath")  # svg_doc.xpath('.//span[@class="html-tag"]/text()') textpath
            for data in datas:
                y = int(all_y_dict[data.attrs['xlink:href']])
                int_set = data.text
                index_and_word_dict[int_set] = range(last, y + 1)
                last = y
            return index_and_word_dict

    @staticmethod
    def get_last_value(css_url, _add_res, css_and_px_dict, _tag, is_num=True):
        """
        根据_tag(类名前缀)获取svg图片中的阈值与文本的对应关系字典
        :param css_url:
        :param _add_res:
        :param css_and_px_dict:
        :param _tag:
        :param is_num:
        :return:
        """
        # 获取svg中阈值与文本的对应关系字典
        svg_threshold_and_int_dict = CrawlerUtils.get_svg_threshold_and_int_dict(css_url, _add_res, _tag, is_num=is_num)
        if svg_threshold_and_int_dict != {}:
            last_value = CrawlerUtils.get_svg_num(_add_res, css_and_px_dict, svg_threshold_and_int_dict, is_num=is_num)
            return last_value

    @staticmethod
    def get_bs(text, selector):
        from bs4 import BeautifulSoup  # 引入BeautifulSoup包
        bs = BeautifulSoup(text, 'lxml')  # 将传进来的字符串用lxml解析
        res = bs.select(selector)  # 根据selector搜索需要结果并返回
        return res

    @staticmethod
    def get_svg_num(datas, css_and_px_dict, svg_threshold_and_int_dict, is_num=True):
        num = ""
        if len(datas):
            for data in datas:
                # 如果是字符，则直接取出
                if isinstance(data, str):
                    num = num + data
                else:
                    # 如果是span类型，则要去找数据
                    # span class的attr
                    if not 'class' in data.attrib:
                        continue
                    span_class_attr_name = data.attrib["class"]
                    if span_class_attr_name == 'more-words':
                        num = num[:-3]
                        break
                    if span_class_attr_name == 'less-words':
                        break
                    if span_class_attr_name == 'emoji-img':
                        continue

                    # 偏移量，以及所处的段
                    offset, position = css_and_px_dict[span_class_attr_name]
                    index = abs(int(float(offset)))
                    position = abs(int(float(position)))
                    # 判断
                    for key, value in svg_threshold_and_int_dict.items():
                        if position in value:
                            threshold = int(math.ceil(index / 14))
                            if is_num:
                                number = key[threshold - 1]
                            else:
                                number = key[threshold]
                            num = num + str(number)
        else:
            return 0
        return num.strip()
