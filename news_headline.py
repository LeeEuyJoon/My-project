import requests
from bs4 import BeautifulSoup

# 기본 작업
print("\n[헤드라인 뉴스]")
url = "https://news.naver.com"
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"}
res = requests.get(url,headers=headers)
soup = BeautifulSoup(res.text,"lxml")

# 뉴스 10개 가져오기
box = soup.find_all("div",attrs={"class","cjs_journal_wrap _item_contents"})[:10]
for num,article in enumerate(box):
    # 헤드라인과 링크 출력
    head = article.find("div",attrs={"class":"cjs_t"}).get_text()
    link = article.find("a",attrs={"class":"cjs_news_a"})["href"]
    url = link
    res = requests.get(url,headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text,"lxml")
    print("\n-",soup.find("a",attrs={"class":"ofhd_float_title_text"}).get_text(),"-")
    print("{}번 헤드라인 : {} \nlink : {}".format(num+1,head,link))
    
    # 감정표현
    # emotions = soup.find_all("a",attrs={"class":"u_likeit_list_button _button off"})[:5]
    # for emotion in emotions:
    #     print(emotion.find("span",attrs={"class":"u_likeit_list_name _label"}).get_text(),
    #         emotion.find("span",attrs={"class":"u_likeit_list_count _count"}).get_text())

