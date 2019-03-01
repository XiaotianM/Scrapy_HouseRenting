import requests
import time, sys
from bs4 import BeautifulSoup



def getURLText(url, **kwargs):
    try:
        if 'headers' not in kwargs and 'cookies' not in kwargs:
            response = requests.get(url)
        else:
            response = requests.get(url, kwargs)
        response.raise_for_status()
        # response.encoding = response.apparent_encoding 
        response.encoding = "gbk2312"
    except:
        print("Getting URL:%s Failed!" % url)
    return response.text


def getData(html, kList, cnt, file):
    soup = BeautifulSoup(html, "html.parser")
    targetList = soup.find("table", attrs={'class':'olt'})

    for idx, target in enumerate(targetList.find_all("tr",attrs={'class':''})):
        dataRow = target.find("a", attrs={""})
        dataInfo = dataRow["title"]
        dataLink = dataRow["href"]
        data = [dataInfo, dataLink]
        for key in kList:
            if dataInfo.find(key) != -1:
                cnt = cnt + 1
                print("第%d条信息"%cnt)
                f.write("第%d条信息\n"%cnt)
                try:
                    print("地址:%s"%data[0])
                    f.write("地址:%s\n"%data[0])
                except:
                    print("Unkown Character can not identified!")
                    f.write("Unkown Character can not identified!\n\n")
                    
                print("链接:%s\n"%data[1])
                f.write("链接:%s\n\n"%data[1])
                break
    return cnt 
                


if __name__ == "__main__":
    
    url = "https://www.douban.com/group/shzf/discussion?start="
    cookies = {'Cookie': 'gr_user_id=7d5b929a-b4ba-4061-963d-ef43e3a225e4; _vwo_uuid_v2=6C93DD01D14122EB4CCD93D7ED548D4D|10418eff5d6b6f4588cc744fd92dfd5b; ll="108296"; _ga=GA1.2.1853304387.1513307102; __utmv=30149280.10051; viewed="30179607_25728092_26593822_3112503_26590403_26979890_25819566"; douban-fav-remind=1; ue="maxiaotiandhu@foxmail.com"; push_doumail_num=0; bid=8Y2UoDNhHlA; __yadk_uid=rqqsUGagTFf7Y7gy0cOk2TN2tfVdA8YE; douban-profile-remind=1; push_noty_num=0; ct=y; __utmc=30149280; __utmz=30149280.1551406613.124.71.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; dbcl2="100513716:E9B6SolJc+o"; ck=S0-C; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1551424636%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DRXO56VBqez2Q65K-f0q5lAzWn0e9r5E5Qgn1rU4DyHHEFh1rp27p8e_0hB0o35xluhE6LjZvUI4kk8CzEz0ju_%26wd%3D%26eqid%3Dc1b79f60000531af000000045c789610%22%5D; _pk_ses.100001.8cb4=*; ap_v=0,6.0; __utma=30149280.1853304387.1513307102.1551421087.1551424637.127; __utmt=1; _pk_id.100001.8cb4=b384155da1560c6a.1513307101.123.1551424650.1551421243.; __utmb=30149280.21.5.1551424650839'}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',}
    keyword = ["浦三路","御桥","三林", "云锦路", "华龙新苑", "民苑小区"]

    f = open("douban.txt", "w")
    num = 0  

    page = 200 
    for p in range(page):
        url_update = url + str(25*p)
        resp = getURLText(url_update, cookies=cookies, headers=headers)
        num = getData(resp, keyword, num, f)
        time.sleep(2)  # 防止封号
        
    f.close()