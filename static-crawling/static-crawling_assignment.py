!pip install bs4
!pip install requests
!pip install pandas

from bs4 import BeautifulSoup
import requests

# 알라딘 베스트셀러 페이지 URL
url = "https://www.aladin.co.kr/shop/common/wbest.aspx?BestType=Bestseller&BranchType=1&CID=0&page=1&cnt=1000&SortOrder=1"
response = requests.get(url) # 요청 보내기
html =  response.text # 응답 받은 HTML 문서
soup = BeautifulSoup(html, "html.parser") # BeautifulSoup으로 파싱

tree = soup.select_one("div.ss_book_box")

# 제목과 링크 추출
title_tag = tree.select_one(".bo3")
link = title_tag.get("href")
title = title_tag.text

# 할인가와 별점 추출
price_tag = tree.select_one(".ss_p2")
price = price_tag.text
review_tag = tree.select_one(".star_score")
print("제목:",title)
print("링크:", link)

#price_tag.text, review_tag.text
review = review_tag.text
print("할인가:",price)
print("별점:",review)

trees = soup.select("div.ss_book_box")
for tree in trees:
    try:
        title = tree.select_one(".bo3")
        title_text = title.text
        title_link = title.attrs['href']
        price = (tree.select_one(".ss_p2")).text
        review = (tree.select_one(".star_score")).text
        print(title_text, title_link, price, review)
    except: continue

import pandas as pd

datas = []
for page_num in range(1, 4):
    url = f"https://www.aladin.co.kr/shop/common/wbest.aspx?BestType=Bestseller&BranchType=1&CID=0&page=1&cnt=1000&SortOrder={page_num}"
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    trees = soup.select("div.ss_book_box")
    for tree in trees:
        try:
            title = tree.select_one(".bo3")
            title_text = title.text
            title_link = title.attrs['href']
            price = (tree.select_one(".ss_p2")).text
            review = (tree.select_one(".star_score")).text

            datas.append([title_text, title_link, price, review])

        except: continue

df = pd.DataFrame(datas, columns = ['title', 'link', 'price', 'review'])

# csv 파일로 저장해 봅시다.
df.to_csv('static-crawling_assignment.csv', index = False)