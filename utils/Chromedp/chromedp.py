import os
import random
import time
import traceback
from threading import Thread

import pychrome

from utils.Chromedp.keyEvent import encode_key_events
from utils.Chromedp.options import Options
from utils.Chromedp.tools.check_port import random_port
from utils.Chromedp.tools.img_tools import *


class Chromedp:
    def __init__(self, proxy=None, log_out=False, is_pc=True):
        options = Options()
        self.port = str(random_port())
        # self.port = 9222
        if not is_pc:
            options.add_argument(
                '--user-agent="Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Mobile Safari/537.36"')
        options.add_argument('--no-first-run')
        options.add_argument('--no-default-browser-check')
        options.add_argument('--remote-debugging-port={}'.format(self.port))
        # options.add_argument('--headless')
        # options.add_argument('--disable-gpu')
        options.add_argument('--start-maximized')
        # options.add_argument('--no-sandbox')
        options.add_argument('--user-data-dir="C:/chrome/{}"'.format(self.port))
        if proxy:
            options.add_argument('--proxy-server=%(http)s' % proxy)
        self.t = Thread(target=self.start, args=(options,))

        self.t.start()
        for x in range(5):
            try:
                self.browser = pychrome.Browser(url="http://127.0.0.1:{}".format(self.port))
                self.tab_dict = {}
                self.curr_tab = self.browser.new_tab()
                break
            except:
                traceback.print_exc()
                time.sleep(1)
        self.log_out = log_out

        def request_will_be_sent(**kwargs):
            # print(kwargs)
            # print("loading: %s" % kwargs.get('request').get('url'))
            try:
                if kwargs['request']['url'] == 'https://www.jetstar.com/_bm/_data':
                    print(kwargs)
                    ret = self.curr_tab.call_method('Network.getRequestPostData', requestId=kwargs.get('requestId'))
                    self.ret = ret
                    print(ret)
                    # data = self.curr_tab.call_method('Network.getResponseBody', requestId=kwargs.get('requestId'))
                    # print(data)
            except:
                traceback.print_exc()
                pass

        def responseReceived(**kwargs):
            try:
                if kwargs['response']['url'] == 'https://www.jetstar.com/_bm/_data':
                    print(kwargs)

                    # data = self.curr_tab.call_method('Network.getResponseBody', requestId=kwargs.get('requestId'))
                    # print(data)
            except:
                traceback.print_exc()
                pass

        # self.curr_tab.set_listener("Network.requestWillBeSent", request_will_be_sent)
        # self.curr_tab.set_listener("Network.responseReceived", responseReceived)

        self.curr_tab.start()
        self.curr_tab.Network.enable()
        self.curr_tab.Log.enable()
        self.curr_tab.Runtime.enable()
        self.curr_tab.Inspector.enable()
        self.curr_tab.Page.enable()
        self.curr_tab.DOM.enable()
        self.curr_tab.CSS.enable()
        self.curr_tab.Page.getResourceTree()

    def start(self, options):
        cmd = ''
        for x in options.arguments:
            cmd = cmd + " " + x
        os.system(cmd)
        # subprocess.check_output(options.arguments)

    def call_method(self, _method, *args, **kwargs):
        msg = None

        try:
            msg = self.curr_tab.call_method(_method, *args, **kwargs)
            if self.log_out:
                _input = {'method': _method, 'params': dict(kwargs)}
                print(' <--', _input, '\n', '-->', msg)
        except:
            _input = {'method': _method, 'params': dict(kwargs)}
            if self.log_out:
                print(' <--', _input, '\n', 'error', _method, kwargs)
        return msg

    def close_tab(self):
        self.curr_tab.stop()
        self.browser.close_tab(self.curr_tab)

    def open_url(self, url):
        self.curr_tab.Page.navigate(url=url)

    def wait_visible(self, sel):
        msg = self.perform_search(sel)
        if msg is None:
            time.sleep(0.5)
            return self.wait_visible(sel)

    def set_node_id(self, tab=None, pierce=True):
        msg = self.call_method('DOM.getDocument', tab=tab, pierce=pierce)
        return msg

    def perform_search(self, sel):
        msg = self.call_method('DOM.performSearch', query=sel)

        msg = self.call_method('DOM.getSearchResults', searchId=msg['searchId'],
                               fromIndex=0, toIndex=msg['resultCount'])

        return msg

    def get_box_model(self, node_id):
        msg = self.curr_tab.DOM.getBoxModel(nodeId=node_id)
        return msg

    def find_element(self, sel, count=0):
        # time.sleep(1)
        self.wait_visible(sel)
        count = count + 1
        if count > 10:
            raise RuntimeError('can`t find ', sel, 'element')
        self.set_node_id()
        node_ids = self.perform_search(sel)
        if node_ids == None:
            return self.find_element(sel)
        node_ids = node_ids['nodeIds']
        if len(node_ids) > 1:
            ret = []
            for x in node_ids:
                box = self.get_box_model(x)
                if box:
                    ret.append(Element(self, self.curr_tab, sel, box['model'], x))
                else:
                    return self.find_element(sel)
            return ret
        else:
            ret = self.get_box_model(node_ids[0])
            if ret:
                return Element(self, self.curr_tab, sel, ret['model'], node_ids[0])
            else:
                return self.find_element(sel)

    def mouse_pressed(self, x, y, button='left'):
        msg = self.call_method('Input.dispatchMouseEvent', type='mousePressed', x=x, y=y, modifiers=0,
                               button=button, clickCount=1)
        return msg

    def mouse_released(self, x, y, button='left'):
        msg = self.call_method('Input.dispatchMouseEvent', type='mouseReleased', x=x, y=y, modifiers=0,
                               button=button, clickCount=1)
        return msg

    def mouse_moved(self, x, y, button='left'):
        msg = self.call_method('Input.dispatchMouseEvent', type='mouseMoved', x=x, y=y, modifiers=0,
                               button=button, clickCount=1)
        return msg

    def touch_start(self, x, y, ):
        TouchPoint = {
            'x': x,
            'y': y,

        }
        msg = self.call_method('Input.dispatchTouchEvent', type='touchStart', touchPoints=[TouchPoint], )
        return msg

    def touch_move(self, x, y, ):
        msg = self.call_method('Input.dispatchTouchEvent', type='touchMove', touchPoints=[{'x': x, 'y': y}], )
        return msg

    def touch_End(self, x, y, ):
        msg = self.call_method('Input.dispatchTouchEvent', type='touchEnd', touchPoints=[{'x': x, 'y': y}], )
        return msg

    def click(self, x, y):
        self.mouse_pressed(x, y)
        self.mouse_released(x, y)

    def focus(self, node_id):
        self.call_method('DOM.focus', nodeId=node_id)

    def dispatch_key_event(self, key_event):
        # print(key_event.to_params())
        self.call_method('Input.dispatchKeyEvent', **key_event.to_params())

    def key_action(self, keys):
        for r in keys:
            for k in encode_key_events(r):
                self.dispatch_key_event(k)

    def eval_js(self, js):
        ret = self.curr_tab.Runtime.evaluate(expression=js)
        print(ret)
        result = Result(**self.curr_tab.Runtime.evaluate(expression=js)['result'])
        return result.value

    def curr_page(self):
        js = '''
        document.documentElement.outerHTML
        '''
        return self.eval_js(js)

    def get_cookies(self):
        return self.curr_tab.Page.getCookies()['cookies']

    def get_document(self, depth=1, pierce=False):
        return self.curr_tab.DOM.getDocument(depth=depth, pierce=pierce)

    def get_flattened_document(self, depth=1, pierce=False):
        return self.curr_tab.DOM.getFlattenedDocument(depth=depth, pierce=pierce)

    def clear_browser_cookies(self):

        msg = self.curr_tab.Network.clearBrowserCookies()
        if len(self.get_cookies()) > 0:
            return self.clear_browser_cookies()
        return msg

    def clear_browser_cache(self):
        return self.curr_tab.Network.clearBrowserCache()

    def delete_cookie(self, **kwargs):
        """
        :param kwargs:
            name
            url
            domain
            path
        :return:
        """
        cookies = self.get_cookies()
        for cookie in cookies:
            is_delete = True
            for x in kwargs.keys():
                if cookie[x] != kwargs.get(x):
                    is_delete = False
            if is_delete:
                self.curr_tab.Network.deleteCookies(**cookie)
                if cookie in self.get_cookies():
                    time.sleep(0.1)
                    return self.delete_cookie(**kwargs)

    def set_cookie(self, **kwargs):
        """
        :param kwargs:
            name string
            value string
            url string
            domain string
            path string
            secure  boolean
            httpOnly boolean
            sameSite CookieSameSite
            expires TimeSinceEpoch
        :return:
            success boolean
        """
        return self.curr_tab.Network.setCookie(**kwargs)

    def capture_screenshot(self, **kwargs):
        """
        :param kwargs:
            format string: jpeg, png ,
            quality integer: [0..100] (jpeg only),
            clip Viewport_dict: Capture the screenshot of a given region only.,
            fromSurface boolean: Capture the screenshot from the surface, rather than the view. Defaults to true..
        :return:
            data string:Base64-encoded image data.
        """
        return self.curr_tab.Page.captureScreenshot(**kwargs)

    def scroll_to(self, x, y):
        js = '''
                (function(x, y) {
                window.scrollTo(x, y);
                return [window.scrollX, window.scrollY];
            })(__x__, __y__)'''.replace('__x__', str(x)).replace('__y__', str(y))
        self.eval_js(js)

    def quit(self):
        for x in self.browser.list_tab():
            self.browser.close_tab(x.id)


class Element:
    def __init__(self, chrome, tab, sel, modle, node_id):
        self.modle = modle
        self.content = modle['content']
        self.padding = modle['padding']
        self.border = modle['border']
        self.margin = modle['margin']
        self.width = modle['width']
        self.height = modle['height']
        self.chrome = chrome
        self.tab = tab
        self.sel = sel
        self.x = None
        self.y = None
        self.left_x = None
        self.left_y = None
        self.__set_xy()
        self.node_id = node_id
        self.view_port = Viewport(x=self.left_x, y=self.left_y, width=self.width, height=self.height)

    def __set_xy(self):
        c = len(self.content)
        x = 0
        y = 0
        for i in range(0, c, 2):
            x = x + self.content[i]
            y = y + self.content[i + 1]
        x = x / (c / 2)
        y = y / (c / 2)
        self.x = x
        self.y = y
        self.left_x = self.content[0]
        self.left_y = self.content[1]

    def click(self):
        self.scroll()
        self.chrome.click(self.x, self.y)

    def send_keys(self, keys, time_interval=None):
        self.chrome.focus(self.node_id)
        if time_interval:
            if isinstance(time_interval, list):
                for x in keys:
                    self.chrome.key_action(x)
                    time.sleep(time_interval[keys.index(x)])
            else:
                for x in keys:
                    self.chrome.key_action(x)
                    time.sleep(time_interval)
        else:
            self.chrome.key_action(keys)

    def get_attributes(self):
        return self.tab.DOM.getAttributes(nodeId=self.node_id)

    def text(self):
        js = '''(function (path) {
         return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
        })(`(__sel__)`).textContent'''.replace('(__sel__)', self.sel)

        return self.chrome.eval_js(js)

    def html(self):
        js = '''(function (path) {
         return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
        })(`(__sel__)`).innerHTML'''.replace('(__sel__)', self.sel)
        return self.chrome.eval_js(js)

    def focus(self):
        self.chrome.focus(self.node_id)

    def mouseover(self):
        self.chrome.mouse_released(self.x, self.y, button='left')

    def mouse_pressed(self):
        self.chrome.mouse_pressed(self.x, self.y)

    def mouse_released(self):
        self.chrome.mouse_released(self.x, self.y)

    def mouse_moved(self, x, y):
        self.x = self.x + x
        self.y = self.y + y
        self.chrome.mouse_moved(self.x, self.y)

    def touch_pressed(self):
        return self.chrome.touch_start(self.x, self.y)

    def touch_released(self):
        return self.chrome.touch_End(self.x, self.y)

    def touch_moved(self, x, y):
        self.x = self.x + x
        self.y = self.y + y
        return self.chrome.touch_move(self.x, self.y)

    def screenshot(self, **kwargs):
        params = {
            'format': kwargs.pop('format', 'png'),
            # 'quality': kwargs.pop('quality', 100),
            'clip': self.view_port.__dict__,
            # 'fromSurface': kwargs.pop('fromSurface', True)
        }
        return img_decode(self.chrome.capture_screenshot(**params)['data'])

    def scroll(self):
        self.chrome.scroll_to(self.left_x, self.left_y)
        new = self.chrome.find_element(self.sel)
        self.__init__(new.chrome, new.tab, new.sel, new.modle, new.node_id)

class Result(object):
    def __init__(self, **kwargs):
        self.type = kwargs.pop('type')
        self.value = kwargs.pop('value', None)


class Viewport(object):
    def __init__(self, **kwargs):
        self.x = kwargs.pop('x')
        self.y = kwargs.pop('y')
        self.width = kwargs.pop('width')
        self.height = kwargs.pop('height')
        self.scale = kwargs.pop('scale', 1)


if __name__ == '__main__':
    ch1 = Chromedp()
    ch1.clear_browser_cookies()
    ch1.clear_browser_cache()
    ch1.open_url('https://account.dianping.com/login?redir=http://www.dianping.com')
    ch1.wait_visible('/html/body/div/div[2]/div[5]/span')
    ch1.find_element('/html/body/div/div[2]/div[5]/span').click()
    ch1.wait_visible('//*[@id="tab-account"]')
    ch1.find_element('//*[@id="tab-account"]').click()
    ch1.find_element('//*[@id="account-textbox"]').send_keys('13883500424', )
    ch1.find_element('//*[@id="password-textbox"]').send_keys('zq13883500424', )
    ch1.find_element('//*[@id="login-button-account"]').click()
    hk = ch1.find_element('//*[@id="yodaBox"]')
    hk.mouse_pressed()
    for x in range(70):
        hk.mouse_moved((x + random.randint(0, 3)) * 0.4, random.randint(0, 10) - 5)
        # if x == 25:
        # time.sleep(1)
        time.sleep(random.randint(0, 30) / 1000)
    hk.mouse_released()
    time.sleep(200)
    ch1.quit()
