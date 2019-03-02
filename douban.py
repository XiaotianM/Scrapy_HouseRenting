import requests
import time, sys
from bs4 import BeautifulSoup



class DouBanScrapy():

    def __init__(self, cookies, headers, urlList, keywords, pages, filename):
        self.urlList = urlList
        self.keywords = keywords
        self.cookies = cookies
        self.headers = headers
        self.pages = pages
        self.num = 0
        self.file = open(filename, "w")


    def getURLText(self, url):
        try:
            if self.cookies is None:
                response = requests.get(url, headers=self.headers)
            else:
                response = requests.get(url, cookies=self.cookies,  headers=self.headers)
            response.raise_for_status()
            # response.encoding = response.apparent_encoding 
            response.encoding = "gbk2312"
        except:
            print("Getting URL:%s Failed!" % url)
        return response.text


    def getData(self, html):
        soup = BeautifulSoup(html, "html.parser")
        targetList = soup.find("table", attrs={'class':'olt'})

        for idx, target in enumerate(targetList.find_all("tr",attrs={'class':''})):
            dataRow = target.find("a", attrs={""})
            dataInfo = dataRow["title"]
            dataLink = dataRow["href"]
            data = [dataInfo, dataLink]
            for key in self.keywords:
                if dataInfo.find(key) != -1:
                    self.num = self.num + 1
                    print("第%d条信息" % self.num)
                    self.file.write("第%d条信息\n" % self.num)
                    try:
                        print("地址:%s" % data[0])
                        self.file.write("地址:%s\n" % data[0])
                    except:
                        print("Unkown Character can not identified!")
                        self.file.write("Unkown Character can not identified!\n\n")
                        
                    print("链接:%s\n" % data[1])
                    self.file.write("链接:%s\n\n" % data[1])
                    break
                    

    def getResultFromOneUrlOnePage(self, url):
        resp = self.getURLText(url)
        num = self.getData(resp)
        time.sleep(2)  # 防止封号


    def getResultFromMultiUrlOnePage(self, cur):    
        for url in self.urlList:
            self.getResultFromOneUrlOnePage(url+str(25*cur))
    

    def getResultFromMultiUrlMultiPage(self):
        for page in range(self.pages):
            self.getResultFromMultiUrlOnePage(page)

        self.file.close()




if __name__ == "__main__":
    
    url = [
        "https://www.douban.com/group/shzf/discussion?start=",                   # 上海租房（不良中介勿扰）
        "https://www.douban.com/group/SHLine11/discussion?start=",               # 上海租房@地铁11号线
        "https://www.douban.com/group/583132/discussion?start=",                 # 上海无中介租房
        "https://www.douban.com/group/SHwoman/discussion?start="                 # 上海租房
        "https://www.douban.com/group/shanghaizufang/discussion?start=",         # 上海租房
        "https://www.douban.com/group/homeatshanghai/discussion?start=",         # 上海租房---房子是租来的，生活不是    
        "https://www.douban.com/group/zufan/discussion?start="                   # 上海租房@长宁租房/徐汇/静安租房
    ]

    cookies = {'Cookie': 'gr_user_id=7d5b929a-b4ba-4061-963d-ef43e3a225e4; _vwo_uuid_v2=6C93DD01D14122EB4CCD93D7ED548D4D|10418eff5d6b6f4588cc744fd92dfd5b; ll="108296"; _ga=GA1.2.1853304387.1513307102; __utmv=30149280.10051; viewed="30179607_25728092_26593822_3112503_26590403_26979890_25819566"; douban-fav-remind=1; ue="maxiaotiandhu@foxmail.com"; push_doumail_num=0; bid=8Y2UoDNhHlA; __yadk_uid=rqqsUGagTFf7Y7gy0cOk2TN2tfVdA8YE; douban-profile-remind=1; push_noty_num=0; ct=y; __utmc=30149280; __utmz=30149280.1551406613.124.71.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; dbcl2="100513716:E9B6SolJc+o"; ck=S0-C; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1551424636%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DRXO56VBqez2Q65K-f0q5lAzWn0e9r5E5Qgn1rU4DyHHEFh1rp27p8e_0hB0o35xluhE6LjZvUI4kk8CzEz0ju_%26wd%3D%26eqid%3Dc1b79f60000531af000000045c789610%22%5D; _pk_ses.100001.8cb4=*; ap_v=0,6.0; __utma=30149280.1853304387.1513307102.1551421087.1551424637.127; __utmt=1; _pk_id.100001.8cb4=b384155da1560c6a.1513307101.123.1551424650.1551421243.; __utmb=30149280.21.5.1551424650839'}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',}
    keywords = ["浦三路","御桥","三林", "云锦路", "华龙新苑", "民苑小区"]
    saveFile = "douban.txt"
        
    scrapy = DouBanScrapy(
                            cookies = cookies,
                            headers = headers,
                            urlList = url,
                            keywords = keywords,
                            pages = 100,
                            filename = saveFile
                        )

    scrapy.getResultFromMultiUrlMultiPage()