import requests

from requests.exceptions import ConnectionError, ProxyError, ReadTimeout, ConnectTimeout


# lock = threading.Lock()
#
# r = RedisClientClass()
#
# def get_proxy():
#     lock.acquire()
#     if r.count('Proxy') < 5:
#         url = 'http://webapi.http.zhimacangku.com/getip?num=5&type=2&pro=&city=0&yys=0&port=11&time=2&ts=1&ys=0&cs=0&lb=1&sb=0&pb=45&mr=1&regions='
#         response = requests.get(url).json()
#         print(response)
#         for i in response['data']:
#             data = '{}:{}'.format(i['ip'], i['port'])
#             r.add('Proxy', data)
#         r.set_time()
#     lock.release()

def get_proxy():
    global res
    try:
        url = 'http://mgr.jinnezha.com/interface/If_Proxy/getThirdProxy?site=992'
        res = requests.get(url, timeout=5).json()
        if res['status'] == 0:
            return res['data']['ip'] + ':' + res['data']['port']
        else:
            return get_proxy()
    except (ConnectionError, ProxyError, ReadTimeout, ConnectTimeout):
        return get_proxy()


def hmd_ip(host):
    try:
        ip = host.split(':')[0]
        port = host.split(':')[1]
        requests.get(
            'http://mgr.jinnezha.com/interface/If_Proxy/noticeFetchFail?site=992&ip=' + ip + '&port=' + port + '&proxyType=2&failType=2')
    except:
        pass


if __name__ == '__main__':
    print(get_proxy())
