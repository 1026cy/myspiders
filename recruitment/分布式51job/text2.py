import lxml.etree
import requests
import lxml


def pagexpath(url):
    headers = {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0);"}
    response = requests.get(url,headers=headers).content.decode("gbk")
    # print(response)
    mytree = lxml.etree.HTML(response)

    joblist = mytree.xpath("//*[@id=\"resultList\"]//div[@class=\"el\"]")
    datalist = []
    for line in joblist:
        mystr = ""
        job = line.xpath("./p/span/a/text()")[0].strip()
        company = line.xpath("./span[1]/a/text()")[0].strip()
        addr = line.xpath("./span[2]/text()")[0].strip()
        money = line.xpath("./span[3]/text()")
        if len(money) == 0:
            money = ""
        else:
            money = money[0].strip()
        datetime = line.xpath("./span[4]/text()")[0].strip()

        mystr += job
        print job
        mystr += " # "
        mystr += company
        print company
        mystr += " # "
        mystr += addr
        print addr
        mystr += " # "
        mystr += money
        print money
        mystr += " # "
        mystr += datetime
        print datetime
        mystr += "\r\n"
        print mystr

        datalist.append(mystr)

    print datalist

    return  datalist
url = "http://search.51job.com/list/040000,000000,0000,00,9,99,python,2,5.html"
a = pagexpath(url)
for i in a:
    print i[0]