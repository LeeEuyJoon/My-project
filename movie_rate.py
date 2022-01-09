
# ----------------프로젝트 사전 연습------------------
# from selenium import webdriver
# headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"}

# 네이버 영화로 이동
# browser = webdriver.Chrome()
# url = "https://movie.naver.com/"
# browser.get(url)

# # 검색창 클릭 & 영화 검색
# search = browser.find_element_by_id("ipt_tx_srch")
# search.click()
# search.send_keys("스파이더맨: 노웨이홈")
# browser.find_element_by_xpath("//*[@id='jSearchArea']/div/button").click()

# # 별점 추출 1
# from bs4 import BeautifulSoup
# soup = BeautifulSoup(browser.page_source,"lxml")
# star = soup.find("em",attrs={"class":"num"}).get_text()
# print(star)

# # 별점 추출 2
# # import requests
# # from bs4 import BeautifulSoup
# # res = requests.get(url,headers=headers)
# # res.raise_for_status()
# # soup = BeautifulSoup(res.text,"lxml")
# # star = soup.find("em",attrs={"class":"num"}).get_text()
# # print(star)

# ---------------------------------------------------------
#---------------------실전---------------------------------

from selenium import webdriver
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"}

# 내가 본 영화 제목, 평점 가져오기
import pandas as pd
my = pd.read_excel('C:/Users/wds66/Desktop/work/my project/movie.xlsx')[['제목','평점']]
title = my['제목']

# 네이버 영화로 이동
browser = webdriver.Chrome()
browser.maximize_window() # 창 최대화
url = "https://movie.naver.com/"
browser.get(url)

# 별점 저장용 리스트 생성
star_list = []

# # 검색창 클릭 & 영화 검색
for i in range(len(my)):
    search = browser.find_element_by_id("ipt_tx_srch")
    # search.click()
    search.send_keys(title[i])
    browser.find_element_by_class_name("btn_srch").click()
    # 평점 정보 없으면 건너 뛰기
    try:
        box = browser.find_element_by_class_name("point")
        star = box.find_element_by_class_name("num").text
        star_list.append(star)
    except:
        star_list.append('nan')

# 브라우저 종료
browser.close()

# 가져온 데이터를 my 데이터프레임에 추가
my['관람객 평점'] = star_list

# 관람객 평점이 nan인 행 삭제
index1 = my[my['관람객 평점']=='nan'].index
my.drop(index1,inplace=True)

# 내 평점 - 관람객 평점 계산하여 열 추가
my['평점 차'] = my['평점'] - my['관람객 평점'].astype(float)


# 평점차이 평균 계산
import numpy as np
average = np.average(my['평점 차'])
if average >= 0:
    print("나는 관람객들보다 평균적으로 평점을 {}점 정도 높게 생각한다.".format(round(abs(average),2)))
else:
    print("나는 관람객들보다 평균적으로 평점을 {}점 정도 낮게 생각한다.".format(round(abs(average),2)))

# my 데이터프레임 csv 파일로 저장
my.to_csv('C:/Users/wds66/Desktop/work/my project/comparison.csv',encoding="utf-8-sig")
