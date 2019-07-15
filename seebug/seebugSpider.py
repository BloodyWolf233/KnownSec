# -*- coding: utf-8 -*-

import re
import time
import js2py
import requests
from bs4 import BeautifulSoup
import json


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    "Host": 'www.seebug.org',
    "Upgrade-Insecure-Requests": '1',
    #"x-test": "false",
}


def get_521_content(url):
    req = requests.get(url=url, headers=headers)
    cookies = req.cookies
    cookies = '; '.join(['='.join(item) for item in cookies.items()])
    txt_521 = req.text
    txt_521 = ''.join(re.findall('<script>(.*?)</script>', txt_521))
    return (txt_521, cookies, req)


def fixed_fun(function,url):
    try:
        #print(function)
        js = function.replace("<script>", "").replace("</script>", "").replace("{eval(", "{var my_data_1 = (")
        # print(js)
        # 使用js2py的js交互功能获得刚才赋值的data1对象
        context = js2py.EvalJs()
        context.execute(js)
        js_temp = context.my_data_1
        #print(js_temp)
        index1 = js_temp.find("document.")
        index2 = js_temp.find("};if((")
        js_temp = js_temp[index1:index2].replace("document.cookie", "my_data_2")
        new_js_temp = re.sub(r'document.create.*?firstChild.href', '"{}"'.format(url), js_temp)
        # print(new_js_temp)
        # print(type(new_js_temp))
        context.execute(new_js_temp)
        data = context.my_data_2
        # print(data)
        __jsl_clearance = str(data).split(';')[0]
        return __jsl_clearance
    except:
        return None

def spider(url , keyword):
    list = []
    count521 = 0

    txt_521, cookies, req = get_521_content(url)
    if req.status_code == 521:
        __jsl_clearance = fixed_fun(txt_521, url)
        if(__jsl_clearance) == None:
            list.append("error")
            return list

        request = requests.Session()
        request.headers.update({'x-text': 'false'})
        headers['x-text'] = 'false'
        headers['Cookie'] = __jsl_clearance + ';' + cookies
        #res1 = requests.get(url=url, headers=headers)


    page = 0
    while (page < 10):
        try:
            page += 1
            print("[-]page %s is spidering.[-]" % str(page))
            # request = requests.Session()
            # request.headers.update({'x-text': 'false'})
            request = requests.get(
                url='https://www.seebug.org/search/?keywords=' + keyword + '&category=&level=all' + str(page),
                headers=headers)
            if(request.status_code == 521):
                count521 += 1
            #print(request.status_code)
            #print(headers)
            #time.sleep(10)  # save time to excute js
            t = 0

            soup = BeautifulSoup(request.text, 'lxml')
            # print(soup.prettify())
            res = soup.select('body > div.container > div > div > div.table-responsive > table > tbody > tr > td')
            # print(res)
            # print(len(res))
            while t <= 60:
                data = {}
                data['keyword'] = keyword
                m = re.match(r"(.*)\">(?P<name>[^_]*)</a></td>", str(res[t + 0]))
                #print(m.groupdict()['name'])
                data['name'] = m.groupdict()['name']

                m = re.match(r"(.*)\">(?P<time>[^_]*)</td>", str(res[t + 1]))
                #print(m.groupdict()['time'])
                data['time'] = m.groupdict()['time']

                m = re.match(r"(.*)class=\"vul-level (?P<vul_lev>[^_]*)\"><span(.*)",
                             str(res[t + 2]).replace('\r', '').replace('\n', '').replace('\t', ''))
                #print(m.groupdict()['vul_lev'])
                data['vul_lev'] = m.groupdict()['vul_lev']

                m = re.match(r"(.*)title=\"(?P<description>[^_]*)\">(.*)", str(res[t + 3]))
                #print(m.groupdict()['description'])
                data['description'] = m.groupdict()['description']
                print(data)
                list.append(data)


                t += 6
        except:
            print("[-]page %s spider error![-]" % str(page))
            pass
    return list, count521


def seebugapi(keyword):
    list = []
    count521 = 0
    list, count521 = spider('https://www.seebug.org/search/?keywords=google.com&category=&level=all', keyword)
    #print("#########################################################")
    return json.dumps(list, ensure_ascii=False),count521


if __name__ == '__main__':
    #spider('https://www.seebug.org/search/?keywords=google.com&category=&level=all', "google.com")
    print(seebugapi("google.com"))
