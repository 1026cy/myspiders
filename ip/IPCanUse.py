import requests
import gevent
import gevent.monkey
gevent.monkey.patch_all()

ipFile = open("./代理IP2.txt","r")

ipList = ipFile.readlines()

print(ipList)



def IPOK():
    try:
        for i in range(len(ipList)):

            ip = ipList.pop(0)
            print(ip)

            headers = {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0;Windows NT 6.1; Trident/5.0);"}

            proxies = {"http": ip}
            url = r"https://www.cyzone.cn/f/20150710/35.html"

            pageData = requests.get(url, proxies=proxies, headers=headers,timeout=1).text

            # print(pageData)

            if pageData:

                if ip not in ipOkList:
                    ipOkList.append(ip)

                    file.write(ip)
                    file.flush()

            else:

                pass

    except:
        pass

if __name__ == '__main__':
    geventList = []
    ipOkList = []
    file = open(r"./cyzone代理IPOK.txt", "w")

    for i in range(5):
        gev = gevent.spawn(IPOK)

        geventList.append(gev)

    gevent.joinall(geventList)

    # IPOK()

    file.close()