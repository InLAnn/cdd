import requests
import json
import sys
# from lxml import etree
import time
import hashlib
import smtplib
import base64
from email.mime.text import MIMEText
from email.utils import formataddr
# from email.header import Header


class WeiboMonitor:

    def __init__(self, ):
        self.session = requests.session()
        self.req_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://passport.weibo.cn/signin/login',
            'Connection': 'close',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
        }
        self.weibo_info = ''
        self.item_ids = []

    def login(self, user_name, password):
        login_api = 'https://passport.weibo.cn/sso/login'
        login_post_data = {
            'username': user_name,
            'password': password,
            'savestate': 1,
            'r': '',
            'ec': '0',
            'pagerefer': '',
            'entry': 'mweibo',
            'wentry': '',
            'loginfrom': '',
            'client_id': '',
            'code': '',
            'qq': '',
            'mainpageflag': 1,
            'hff': '',
            'hfp': ''
        }
        # get user session
        try:
            r = self.session.post(login_api, data=login_post_data, headers=self.req_headers)
            if r.status_code == 200 and json.loads(r.text)['retcode'] == 20000000:
                print('weibo登陆成功！用户id：' + json.loads(r.text)['data']['uid'])
            else:
                print('weibo登陆失败。。')
                sys.exit()
        except Exception as e:
            print(e)
            sys.exit()

    def get_wb_queue(self, wb_user_id):
        # get user weibo container_id
        user_info = 'https://m.weibo.cn/api/container/getIndex?uid=%s&type=uid&value=%s' % (wb_user_id, wb_user_id)
        container_id = 0
        try:
            r = self.session.get(user_info, headers=self.req_headers)
            for i in r.json()["data"]["tabsInfo"]["tabs"]:
                if i["tab_type"] == 'weibo':
                    container_id = i["containerid"]
        except Exception as e:
            print('获取微博队列时错误：', str(e))
            sys.exit()
        # get user weibo index

        self.weibo_info = 'https://m.weibo.cn/api/container/getIndex?uid=%s&type=uid&value=%s&containerid=%s' % (wb_user_id, wb_user_id, container_id)
        try:
            r = self.session.get(self.weibo_info, headers=self.req_headers)
            # print(r.json())
            for i in r.json()["data"]["cards"]:
                if i["card_type"] == 9:
                    weibo_id = i["mblog"]["id"]
                    self.item_ids.append(weibo_id)
            print('获取到 %d 条已有微博' % len(self.item_ids))
        except Exception as e:
            print('获取微博队列时错误：', str(e))
            sys.exit()

    def start_monitor(self):
        return_dict = {}
        try:
            r = self.session.get(self.weibo_info, headers=self.req_headers)
            for i in r.json()["data"]['cards']:
                if i['card_type'] == 9:
                    if str(i['mblog']['id']) not in self.item_ids:
                        self.item_ids.append(i['mblog']['id'])
                        print('获取到一条新微博')
                        return_dict['created_at'] = i['mblog']['created_at']
                        return_dict['text'] = i['mblog']['text']
                        return_dict['source'] = i['mblog']['source']
                        return_dict['nick_name'] = i['mblog']['user']['screen_name']
                        # 如果有图片
                        if 'pics' in i['mblog']:
                            return_dict['pic_urls'] = []
                            for j in i['mblog']['pics']:
                                return_dict['pic_urls'].append(j['url'])
                        return return_dict
            # print(return_dict)
            if return_dict:
                print('收到新微博 %d 条' % len(self.item_ids))
        except Exception as e:
            print('获取新微博时出错：', str(e))
            sys.exit()


def get_md5(strs):
    m = hashlib.md5()
    m.update(strs)
    return m.hexdigest()


def download_image(image_source):
    r = requests.get(image_source.strip())
    file_name = get_md5(image_source) + '.png'
    with open('./images/' + file_name, 'wb') as f:
        f.write(r.content)
    return './images/' + file_name


def send_email(result_dicts):
    flag = True
    user = "@qq.com"  # 发件人
    pwd = ""  # qq授权码
    to = "@qq.com"  # 收件人
    try:
        text = u'发送时间: '+result_dicts['created_at']+u'<br>'
        text += u'发送内容: <br>'+result_dicts['text']+u'<br>'
        # 如果有图片
        if 'pic_urls' in result_dicts:
            for pic in result_dicts['pic_urls']:
                img_file = download_image(pic)
                f = open(img_file, 'rb')
                base_code = base64.b64encode(f.read())
                text += u'<img src="data:image/png;base64,%s">' % base_code
        text += u'<br>来自: '+result_dicts['source']

        msg = MIMEText(text.encode('utf-8'), 'html', 'utf-8')
        msg['Subject'] = u"您关注的微博用户" + result_dicts['nick_name'] + u"发布微博啦"
        msg['Form'] = formataddr(["微博关注系统", user])
        msg['To'] = formataddr(["微博关注系统", to])
        server = smtplib.SMTP_SSL('smtp.qq.com', 465)
        server.login(user, pwd)
        server.sendmail(user, to, msg.as_string())
        server.quit()
    except Exception as e:
        print('发送邮件是错误：', str(e))
        flag = False
    return flag


w = WeiboMonitor()
w.login('', '')
w.get_wb_queue(0)  # 

while True:
    print('checking...')
    new_wb = w.start_monitor()

    if new_wb:
        print(new_wb)
        email_flag = send_email(new_wb)
        if email_flag:
            print('send email successful')
        else:
            print('send email failed')
    else:
        print('没有新微博')
    print('300s sleeping...')
    time.sleep(300)


