import requests
from bs4 import BeautifulSoup
import re
import csv
import lxml

def get_Jinfo(url):
    global acount
    re1 = requests.get(url,"lxml")
    bs1 = BeautifulSoup(re1.text,'lxml')
    a = bs1.find_all(class_ = 'colPic')
    for l in a:
        for m in l.find_all('a'):
            if len(m.attrs)==2 and 'title' in m.attrs :
                hrefs = str(m['href'])
                valuelist = re.split(';|&',hrefs)
                for n in valuelist:
                    if n.startswith('BaseID='):
                        value = n[7:]
                j_name = m['title']
                j_code = value
                j_url = url_head+m['href']
                writer.writerow({'j_name':j_name,'j_code':j_code,'j_url':j_url,'j_big_type':j_big_type,'j_small_type':j_small_type})
                acount = acount+1


acount = 0
url = "https://epub.cnki.net/kns/oldnavi/n_navi.aspx?NaviID=31"
url_head = "https://epub.cnki.net/kns/oldnavi/"
res = requests.get(url,"lxml")
bs = BeautifulSoup(res.text,'lxml')
total = bs.find_all(class_ = 'col')
#j_infos = []
labels = ['j_name', 'j_code', 'j_url','j_big_type','j_small_type']
with open('data/j_infos.csv', 'w',newline='') as f:
    writer = csv.DictWriter(f, fieldnames=labels)
    writer.writeheader()
    for i in total:
        j = i.find_all(class_ = 'list')
        for l in j:
            k=0
            j_info = {}
            for p in l.find_all('a'):
                if k==0:
                    #print(re.split(' |\(',p.get_text())[1])
                    j_big_type = re.split(' |\(',p.get_text())
                else:
                    #print(p.get_text(),url_head+p['href'])
                    j_small_type=p.get_text()
                    url_1 = url_head+p['href']
                    get_Jinfo(url_1)
                #print("-"*100)
                k=1
f.close()                
print("已完成"+str(acount)+"条写入")