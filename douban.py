import requests
import time, sys
from bs4 import BeautifulSoup



class DouBanScrapy():

    def __init__(self, cookies, headers, urlList, keywords, pages, AvalibleTime, filename):
        self.urlList = urlList
        self.InvalidUrl = []
        self.keywords = keywords
        self.cookies = cookies
        self.headers = headers
        self.pages = pages
        self.AvalibleTime = AvalibleTime

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


    def getData(self, html, url, cur):
        soup = BeautifulSoup(html, "html.parser")
        targetList = soup.find("table", attrs={'class':'olt'})

        for idx, target in enumerate(targetList.find_all("tr",attrs={'class':''})):
            dataRow = target.find("a", attrs={""})
            dataInfo = dataRow["title"]
            dataLink = dataRow["href"]
            dataTime = target.find("td", attrs={"nowrap":"nowrap", "class":"time"}).string

            if dataTime < AvalibleTime:
                return False

            data = [dataInfo, dataLink, dataTime]
            for key in self.keywords:
                if dataInfo.find(key) != -1:
                    self.num = self.num + 1
                    print("第%d条信息, 来源: %s, 页数: %d" % (self.num, url.split('/')[-2], cur))
                    self.file.write("第%d条信息\n" % self.num)
                    try:
                        print("地址:%s" % data[0])
                        self.file.write("地址:%s\n" % data[0])
                    except:
                        print("Unkown Character can not identified!")
                        self.file.write("Unkown Character can not identified!\n\n")
                        
                    print("链接:%s" % data[1])
                    print("最后回应:%s\n" % data[2])
                    self.file.write("链接:%s\n\n" % data[1])
                    self.file.write("最后回应:%s\n" % data[2])
                    break
        return True


    def getResultFromOneUrlOnePage(self, url, cur):
        resp = self.getURLText(url)
        if not self.getData(resp, url, cur):
            return False
        return True


    def getResultFromMultiUrlOnePage(self, cur):    
        for url in self.urlList:
            if len(self.urlList) == len(self.InvalidUrl):
                return False

            if url not in self.InvalidUrl:
                if not self.getResultFromOneUrlOnePage(url+str(25*cur), cur):
                    self.InvalidUrl.append(url)
                time.sleep(5)  # 防止封号
        return True
    

    def getResultFromMultiUrlMultiPage(self):
        for page in range(self.pages):
            if not self.getResultFromMultiUrlOnePage(page):
                break

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

    # 将cookie填入此
    cookies = {'Cookie': 'xxxxx'}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',}
    # 筛选关键字填入此
    keywords = ["浦三路","御桥","三林", "云锦路", "华龙新苑", "民苑小区"]
    saveFile = "douban.txt"
    # 日期失活（去掉年份，%month-%day %hour-%minutes)
    AvalibleTime = '02-26 00:00' # 5天前的无效

    scrapy = DouBanScrapy(
                            cookies = cookies,
                            headers = headers,
                            urlList = url,
                            keywords = keywords,
                            pages = 100,
                            AvalibleTime = AvalibleTime,
                            filename = saveFile
                        )

    scrapy.getResultFromMultiUrlMultiPage()