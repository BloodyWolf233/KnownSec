import os
import requests
import json
import sys

IPnum: int = 0
SITEnum: int = 0

user = 's_x_zhang@163.com'
passwd = 'nstl18982067786'


def ZoomEyeLogin():

    data = {
        'username': user,
        'password': passwd,
    }

    try:
        r = requests.post(url='https://api.zoomeye.org/user/login', json=data)

    except requests.RequestException as e:
        print("[-] %s" % e)
        print("[-] 连接失败!")
    else:
        if r.status_code == 200:
            r_decoded = json.loads(r.text)# dumps是将dict转化成str格式，loads是将str转化成dict格式。
            access_token = ''
            access_token = r_decoded['access_token']
            return access_token
        else:
            print("[-] %s %s \n[-] %s" % (r.status_code, r.json()["error"], r.json()["message"]))
            print("[-] 连接失败!")


def ZoomEyeSearch(access_token, ip, page):#api search
    headers = {'Authorization': 'JWT ' + access_token, }

    try:
        r = requests.get(url='https://api.zoomeye.org/web/search?query=' + ip + "&page=" + str(page),
                               headers=headers)
    except requests.RequestException as e:
        print("[-] %s" % e)
        print("[-] %s 检索失败!")
    else:
        if r.status_code == 200:
            if r.content:
            #r_temp = json.loads(r.text)
            #return r_temp
                return r.json()
        else:
            print("[-] %s %s \n[-] %s" % (r.status_code, r.json()["error"], r.json()["message"]))
            print("[-] %s 检索失败!" )


def output_IPtabledata(temp):#what we need to download
    global IPnum
    result = list()
    for line in temp["matches"]:

        iplen = len(line["ip"])
        iplenTemp = 0
        while iplenTemp < iplen:

            result.append(str(IPnum) + "\t" + null_print(str(line["ip"][iplenTemp])) + "\t" + null_print(str(line["site"])) + "\t"

                          + null_print(str(line["geoinfo"]["city"]["names"]["en"])) + "\t"
                          + null_print(str(line["geoinfo"]["country"]["names"]["en"])) + "\t" + null_print(str(line["geoinfo"]["organization"])) + "\t"
                          + null_print(str(line["geoinfo"]["location"]["lat"])) + "\t" + null_print(str(line["geoinfo"]["location"]["lon"])) + "\n"
                          )
            iplenTemp += 1
            IPnum += 1

    return result


def output_SITEtabledata(temp):
    global SITEnum
    result = list()
    for line in temp["matches"]:

        iplen = len(line["ip"])
        iplenTemp = 0
        while iplenTemp < iplen:
            domainlen = len(line["domains"])
            domainTemp = 0
            while domainTemp < domainlen:
                result.append(str(SITEnum) + "\t" + null_print(str(line["ip"][iplenTemp])) + "\t" + null_print(str(line["site"])) + "\t"
                              + null_print(str(line["domains"][domainTemp])) + "\n"
                              )
                domainTemp += 1
                SITEnum += 1
            iplenTemp += 1

    return result


def null_print(a):#fill the empty data
    if a != "" and a != "[]":
        return a
    else:
        return "NULL"


def getTable2txt(ip):#download to local
    access_token = ''

    while(not access_token):
        access_token = ZoomEyeLogin()

    f1 = open('ZoomEyesIP.txt', "a+")
    f2 = open('ZoomEyesSITE.txt', "a+")
#    result1 = list()
#    result2 = list()
    page: int = 0
    while page <= 1: #每页10条,限制页数
        temp = ZoomEyeSearch(access_token, ip, page)
        if not temp:
            print('[-]检索完成!')
            break
        else:
            if not temp["matches"]:
                print('[-]没有数据!')
                break
            else:
#                result1.extend(output_IPtabledata(temp))
#                result2.extend(output_SITEtabledata(temp))
                f1.writelines((set(output_IPtabledata(temp))))
                f2.writelines(set(output_SITEtabledata(temp)))
                print('[-]开始下载第 %s 页' % page)
        page += 1

#    result1 = set(result1)
#    with open('ZoomEyesIP.txt', "a+") as f1:
#        f1.writelines(result1)
#        f1.close()
#    result2 = set(result2)
#    with open('ZoomEyesSITE.txt', "a+") as f2:
#        f2.writelines(result2)
#        f2.close()
    f1.close()
    f2.close()

def getip():#need to download ip first, it's search list
    f = open('C:\\Users\\DZKD\\PycharmProjects\\untitled\\ip.txt', 'r')
    line = f.readline()
    while line:
        #print(line)
        if line[-1] == "\n":
            line = line[:-1]
        else:
            line = line
        getTable2txt(line)
        line = f.readline()
    f.close()


if __name__ == '__main__':
    #getTable2txt("81.92.80.55")
    #getip()
    #print(ZoomEyeSearch(ZoomEyeLogin(), "81.92.80.55", 1))
    access_token = ZoomEyeLogin()
    #print(access_token)
    headers = {'Authorization': 'JWT ' + access_token, }
    try:
        r = requests.get(url='https://www.zoomeye.org/search?q=google&1')
    except requests.RequestException as e:
        print("[-] %s" % e)
        print("[-] %s 检索失败!")
    else:
        if r.status_code == 200:
            if r.content:
            #r_temp = json.loads(r.text)
            #return r_temp
                print(r.text)
        else:
            #print("[-] %s %s \n[-] %s" % (r.status_code, r.json()["error"], r.json()["message"]))
            print("[-] %s 检索失败!!!!" )
