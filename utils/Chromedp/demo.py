from utils.Chromedp.chromedp import Chromedp


def demo():
    ch = Chromedp()
    ch.clear_browser_cookies()
    ch.clear_browser_cache()
    ch.open_url('https://www.dianping.com/chongqing/ch10')
    ch.wait_visible('/html/body/div[2]/div[3]/div[1]/div[1]')
    data = ch.get_cookies()

    print(data)


if __name__ == '__main__':
    demo()
