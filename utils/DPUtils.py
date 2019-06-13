# -*- coding:utf-8 -*-
import json
import os
import re

from setting.config import BASE_DIR
from utils.CrawlerUtils import CrawlerUtils


class DPUtils:
    @staticmethod
    def get_real_by_tag(tags, css_and_px_dict, svg_threshold_and_int_dict, font_size=12, diff=0):
        import math
        result = ''
        for tag in tags:
            # 如果是字符，则直接取出
            if isinstance(tag, str):
                result += tag
            else:
                # 如果是span类型，则要去找数据
                # span class的attr
                span_class_attr_name = tag.attrs["class"][0]
                # 偏移量，以及所处的段
                offset, position = css_and_px_dict[span_class_attr_name]
                index = abs(int(float(offset)))
                position = abs(int(float(position)))
                # 判断
                for key, value in svg_threshold_and_int_dict.items():
                    if position in value:
                        threshold = int(math.ceil(index / font_size))
                        word = key[threshold + diff]
                        result += word
        return result

    @staticmethod
    def get_css(content):
        """
        用正则匹配网页中的css文件的url
        :param content: 网页HTML结构
        :return: CSS的URL
        """
        matched = re.search(r'href="([^"]+svgtextcss[^"]+)"', content, re.M)
        if not matched:
            raise FileNotFoundError("cannot find svgtextcss file")
        css_url = matched.group(1)

        css_url = "http:" + css_url
        return css_url

    @staticmethod
    def get_css_and_px_dict(con):
        find_datas = re.findall(r'(\.[a-zA-Z0-9-]+)\{background:(\-\d+\.\d+)px (\-\d+\.\d+)px', con)
        css_name_and_px = {}
        for data in find_datas:
            span_class_attr_name = data[0][1:]
            offset = abs(int(float(data[1])))
            position = abs(int(float(data[2])))
            css_name_and_px[span_class_attr_name] = [offset, position]
        return css_name_and_px

    @staticmethod
    def get_svg_threshold_int_dict(req, content, prefix, referer):
        index_and_word_dict = {}

        find_svg_url = re.search(r'\[class\^="{}"\].*?background\-image: url\((.*?)\);'.format(prefix), content)
        if not find_svg_url:
            raise Exception("cannot find svg file, check")

        svg_url = find_svg_url.group(1)
        req.get('http:' + svg_url, referer=referer)
        svg_content = req.text()
        req.close()
        last = 0
        font_size = int(re.search(r'font-size:([0-9]*)px', svg_content).group(1))

        svg_doc_path = CrawlerUtils.get_bs(svg_content, 'path')
        svg_doc_textath = CrawlerUtils.get_bs(svg_content, 'textPath')

        def __deal(value):
            return lambda x: value[x // font_size]

        if svg_doc_path and svg_doc_textath:
            for path, textpath in zip(svg_doc_path, svg_doc_textath):
                offset = int(path.attrs['d'].split(' ')[1].strip())
                index_and_word_dict[range(last, offset)] = __deal(textpath.text)
                last = offset

        else:
            svg_doc_text = CrawlerUtils.get_bs(svg_content, 'text')
            for i in svg_doc_text:
                index_and_word_dict[range(last, int(i.attrs['y']))] = __deal(i.text)
                last = int(i.attrs['y'])
        return index_and_word_dict

    @staticmethod
    def get_prefix_by_content(content, com, css_list):
        class_list = set(re.findall(com, str(content)))
        if len(class_list) == 0:
            return None
        for i in css_list:

            _new_list = set(list(data[0:len(i)] for data in class_list))

            if _new_list.__len__() == 1 and i in _new_list:
                return i

        def __deal(_list, offset=1):
            _new_list = [data[0:offset] for data in _list]

            if len(set(_new_list)) == 1:
                # 说明全部重复
                offset += 1
                return __deal(_list, offset)
            else:
                _return_data = [data[0:offset - 1] for data in _list][0]

                return _return_data

        prefix = __deal(class_list)
        return prefix



    @staticmethod
    def get_cookies(city, type=0):
        file_path = os.path.join(BASE_DIR, 'static/json/cookies.json')
        with open(file_path, 'r', encoding='utf-8') as r:
            data = json.loads(r.read())
        if city not in data.keys():
            return []
        return data[city]
