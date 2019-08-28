# 자연어 처리를 이용한 웹툰 댓글 분석 ebtoon Comment Analysis


## 개요
웹툰 작가 및 웹툰 작가 지망생들을 위한 웹툰 댓글 분석 웹 페이지를 개발하여 제공함으로써 분석 결과를 통해 독자들의 의견을 보기 쉽게 확인하고 빠른 피드백을 가능하게 한다

## 사용된 패키지
### 데이터 수집
1. Selenium
2. BeautifulSoup

### 자연어 처리
1. konlpy 형태소 분석기 - twitter, okt
2. re (정규표현식)

### 감성분석 (LSTM)
1. Keras 

### 댓글 요약 (textrank)
1. newspaper
2. Keras 

### 작가 및 작품 키워드 포함 댓글 분석 (word2vec)
1. Gensim
