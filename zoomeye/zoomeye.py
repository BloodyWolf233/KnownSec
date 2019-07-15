import os
import sys
import requests

page = 1

# 输入个人账号密码
user = ''
passwd = ''


# 验证用户名密码，返回access_token
def Check():
    data_info = {'username': user, 'password': passwd}
    try:
        respond = requests.post(url='https://api.zoomeye.org/user/login', json=data_info)
    except requests.RequestException as e:
        print("[-] %s" % e)
        print("[-] 连接失败!")
    else:
        if respond.status_code == 200:
            access_token = respond.json()
            return access_token
        else:
            print("[-] %s %s \n[-] %s" % (respond.status_code, respond.json()["error"], respond.json()["message"]))
            print("[-] 连接失败!")


def search():
    global mode, query
    mode = input('请选择要搜索的类型：host | web\n')
    query = input('请输入要查询的关键字:\n')


def getRespose(access_token):
    authorization = {'Authorization': 'JWT ' + access_token["access_token"]}
    try:
        respond = requests.get(url='https://api.zoomeye.org/' + mode + '/search?query=' + query + "&page=" + str(page),
                               headers=authorization)
    except requests.RequestException as e:
        print("[-] %s" % e)
        print("[-] %s 检索失败!" % mode.capitalize())
    else:
        if respond.status_code == 200:
            return respond.json()
        else:
            print("[-] %s %s \n[-] %s" % (respond.status_code, respond.json()["error"], respond.json()["message"]))
            print("[-] %s 检索失败!" % mode.capitalize())


def output_data(temp):
    result = list()
    if mode == "host":
        for line in temp["matches"]:
            result.append(line["ip"] + ":" + str(line["portinfo"]["port"]) + "\n")
    else:
        for line in temp["matches"]:
            result.append(str(line["ip"]) + "\n")
    return result


def mian():
    global page
    access_token = Check()
    search()
    if not access_token:
        sys.exit()
    else:
        pass
        result = list()
        if search:
            max_page = int(input('请输入最大页数(每页10条):\n'))
            while page <= max_page:
                temp = getRespose(access_token)
                if not temp:
                    print('[-]检索完成!')
                    break
                else:
                    if not temp["matches"]:
                        print('[-]没有数据!')
                        break
                    else:
                        result.extend(output_data(temp))
                        print('[-]开始下载第 %s 页' % page)
                page += 1
        result = set(result)
        with open('ZoomEyes.txt', "w") as f:
            f.writelines(result)
            f.close()
if __name__ == '__main__':
    mian()
