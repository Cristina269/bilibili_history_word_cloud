import qrcode
from threading import Thread
import time
import requests
from io import BytesIO
import http.cookiejar as cookielib
from PIL import Image
import os


class showpng(Thread):
    def __init__(self, data):
        Thread.__init__(self)
        self.data = data

    def run(self):
        img = Image.open(BytesIO(self.data))
        img.show()


class To_login:
    def __init__(self):
        pass

    def login_status(self, session):
        session.cookies = cookielib.LWPCookieJar('cookie.txt')
        try:
            session.cookies.load(ignore_discard=True)
        except Exception:
            pass
        result = session.get('https://api.bilibili.com/x/web-interface/nav').json()
        if result['code'] == 0:
            print('已登陆：', result['data']['uname'])
            return session, True
        else:
            print('未登录')
            return session, False

    def try_to_login(self):
        if not os.path.exists('cookie.txt'):
            with open("cookie.txt", 'w') as f:
                f.write("")
        else:
            pass
        session = requests.session()
        session, status = self.login_status(session)
        if status == 0:
            get_login = session.get('https://passport.bilibili.com/qrcode/getLoginUrl').json()
            login_url = requests.get(get_login['data']['url']).url
            oauthKey = get_login['data']['oauthKey']
            qr = qrcode.QRCode()
            qr.add_data(login_url)
            img = qr.make_image()
            a = BytesIO()
            img.save(a, 'png')
            png = a.getvalue()
            a.close()
            t = showpng(png)
            t.start()
            tokenurl = 'https://passport.bilibili.com/qrcode/getLoginInfo'
            while 1:
                qrcodedata = session.post(tokenurl,
                                          data={'oauthKey': oauthKey, 'gourl': 'https://www.bilibili.com/'}).json()
                print(qrcodedata)
                if '-4' in str(qrcodedata['data']):
                    print('二维码未失效，请扫码')
                elif 'True' in str(qrcodedata['status']):
                    print('已确认，登入成功')
                    session.get(qrcodedata['data']['url'])
                    break
                else:
                    print(qrcodedata)
                time.sleep(2)
            session.cookies.save()
        return session
