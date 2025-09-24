!pip install selenium
!pip install bs4
!pip install pandas
!pip install openpyxl

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Selenium 드라이버 설정 (Chrome 사용)
driver = webdriver.Chrome()

# Yanolja 리뷰 페이지로 이동
url = 'https://www.yanolja.com/reviews/domestic/10041505'
driver.get(url)

# 페이지 로딩을 위해 대기
time.sleep(3)

# 스크롤 설정: 페이지 하단까지 스크롤을 내리기
scroll_count = 10  # 스크롤 횟수 설정
for _ in range(scroll_count):
    ######## your code here ########
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
    # 리뷰 요소 가져오기 (예시: 리뷰 텍스트가 들어있는 div 태그)
    reviews = driver.find_elements("css selector", ".css-vjs6b8")
    time.sleep(1)  # 스크롤 이후 대기

from bs4 import BeautifulSoup

# 웹페이지 소스 가져오기
page_source = driver.page_source

# BeautifulSoup를 사용하여 HTML 파싱
soup = BeautifulSoup(page_source, 'html.parser')

# 리뷰 텍스트 추출
reviews_class = soup.select(".review-item-container")
reviews = []

# 각 리뷰 텍스트 정리 후 추가
for review in reviews_class:
    cleaned_text = review.get_text(strip=True).replace('\r', '').replace('\n', '')
    reviews.append(cleaned_text)

ratings = []

for review_container in reviews_class:
    star_container = review_container.select_one(".css-rz7kwu")
    if not star_container:
        ratings.append(0)
        continue
    stars = star_container.find_all("svg")
    filled_stars = sum(
        1 for star in stars if not (star.find("path") and star.find("path").get("fill-rule") == "evenodd")
    ) #stars 안의 각 star에 대해 path의 fill-rule 속성이 evenodd이면 1을 더함
    ratings.append(filled_stars)

import pandas as pd

# 별점과 리뷰를 결합하여 리스트 생성
data = list(zip(ratings, reviews))

# DataFrame으로 변환
df_reviews = pd.DataFrame(data, columns=['Rating', 'Review'])

# 평균 별점 계산
average_rating = sum(ratings) / len(ratings)

from collections import Counter
import re

# 불용어 리스트 (한국어)
korean_stopwords = set(['이', '그', '저', '것', '들', '다', '을', '를', '에', '의', '가', '이', '는', '해', '한', '하', '하고', '에서', '에게', '과', '와', '너무', '잘', '또','좀', '호텔', '아주', '진짜', '정말'])

# 모든 리뷰를 하나의 문자열로 결합
all_reviews_text = " ".join(reviews)

# 단어 추출 (특수문자 제거)
words = re.findall(r"[가-힣]+", all_reviews_text)

# 불용어 제거
filtered_words = [w for w in words if w not in korean_stopwords and len(w) > 1]

# 단어 빈도 계산
word_counts = Counter(filtered_words)

# 자주 등장하는 상위 15개 단어 추출
common_words = word_counts.most_common(15)

# 분석 결과 요약
summary_df = pd.DataFrame({
    'Average Rating': [average_rating],
    'Common Words': [', '.join([f"{word}({count})" for word, count in common_words])]
})

# 최종 DataFrame 결합
final_df = pd.concat([df_reviews, summary_df], ignore_index=True)

# Excel 파일로 저장
final_df.to_excel('yanolja.xlsx', index = False)

# 드라이버 종료
driver.quit()