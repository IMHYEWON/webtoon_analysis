#!/usr/bin/env python
# coding: utf-8

# In[106]:


from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import exceptions
from time import sleep


# In[107]:


driver = webdriver.Chrome('C:\\Users\\dbwjd\\Desktop\\studying\\chromedriver')
driver.implicitly_wait(1)
#driver.get('https://m.comic.naver.com/scrolltoon/comment.nhn?titleId=718017&no=16')
driver.get('https://m.comic.naver.com/webtoon/detail.nhn?titleId=729938&no=8&weekday=fri')


# In[108]:


# 전체 댓글 더보기 클릭
btn_all = driver.find_element_by_xpath('//*[@id="cbox_module"]/div/div[6]/a')
btn_all.click()
sleep(5)

try:
    while True:
        # 더보기 클릭
        btn_more = driver.find_element_by_xpath('//*[@id="cbox_module"]/div/div[7]/a')
        btn_more.click()
        sleep(3)
except exceptions.ElementNotVisibleException as e:
    pass
except Exception as e:
    print(e)


# In[109]:


html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
comments = soup.find_all("span", {"class":"u_cbox_contents"})
#recomm = soup.find_all("em", {"class":"u_cbox_cnt_recomm"})     # 좋아요 수
#unrecomm = soup.find_all("em",{"class":"u_cbox_cnt_unrecomm"})  # 싫어요 수

comment_list = []
#recomm_list = []
#unrecomm_list = []

for line in comments:
    comment_list.append(line.string)
    
#for element in recomm:
#    recomm_list.append(element.get_text())
    
#for element in unrecomm:
#    unrecomm_list.append(element.get_text())


# In[110]:


import pandas as pd

#df = pd.DataFrame({"댓글":comment_list, "좋아요":recomm_list, "싫어요":unrecomm_list})
#df

df = pd.DataFrame({"댓글":comment_list})
df


# In[111]:


import os 

currentPath = os.getcwd()

os.chdir('C:/Users/dbwjd/Desktop')
# 텍스트 파일로 저장
df.to_csv("test4.txt",encoding='utf-8-sig')


# In[112]:


# 불필요한 문자 제거
import re

# 입,출력 파일명
INPUT_FILE_NAME = 'test4.txt' 
OUTPUT_FILE_NAME = 'test4_clean.txt'

# re.sub('바꿀 정규식 표현','바꾸게 될 단어', 바꿀 문자열)
def clean_text(text):
    cleaned_text = re.sub('[0-9]','',text)
    cleaned_text = re.sub('[~!@#$%^&*;,.?/+=-]','',cleaned_text)
    return cleaned_text

#메인 함수
def main():
    read_file = open(INPUT_FILE_NAME, 'r', encoding="UTF8")
    write_file = open(OUTPUT_FILE_NAME, 'w', encoding="UTF8")
    text = read_file.read()
    text = clean_text(text)
    write_file.write(text)
    read_file.close()
    write_file.close()
    
if __name__ == "__main__":
    main()


# In[113]:


review_file = open("test4_clean.txt","rt",encoding="UTF8")
lines = review_file.read()


# In[114]:


from newspaper import Article
from konlpy.tag import Kkma
from konlpy.tag import Twitter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import normalize
import numpy as np


# ### 문서 타입에 따른 문장 단위로 분리하기
# * <big>텍스트 크롤링</big>
# * <big>문장 단위 분리</big>
# * <big>명사 추출</big>  
# `[텍스트 크롤링, 문장단위 분리, 명사추출]과정을 SentenceTokenizer 클래스로 생성`

# In[115]:


class SentenceTokenizer(object):
    def __init__(self):
        self.kkma = Kkma()
        #self.okt = Okt()
        self.stopwords = []
        
    def text2sentences(self, text):
        sentences = self.kkma.sentences(text)
        for idx in range(0, len(sentences)):
            if len(sentences[idx]) <= 10:
                sentences[idx - 1] += (' ' + sentences[idx])
                sentences[idx] = ''
        return sentences
    
    def get_nouns(self, sentences):
        nouns = []
        for sentence in sentences:
            if sentence is not '':
                nouns.append(' '.join([noun for noun in self.kkma.nouns(str(sentence))
                                      if noun not in self.stopwords and len(noun) > 1]))
                
        return nouns


# ### TF-IDF 모델 생성 및 그래프 생성

# In[116]:


class GraphMatrix(object):
    def __init__(self):
        self.tfidf = TfidfVectorizer()
        self.cnt_vec = CountVectorizer()
        self.graph_sentence = []
    
    def build_sent_graph(self, sentence):
        tfidf_mat = self.tfidf.fit_transform(sentence).toarray()
        self.graph_sentence = np.dot(tfidf_mat, tfidf_mat.T)
        return self.graph_sentence
    
    def build_words_graph(self, sentence):
        cnt_vec_mat =  normalize(self.cnt_vec.fit_transform(sentence).toarray().astype(float),
                                axis=0)
        vocab = self.cnt_vec.vocabulary_
        return np.dot(cnt_vec_mat.T, cnt_vec_mat), {vocab[word] : word for word in vocab}


# ### Textrank 알고리즘

# In[117]:


class Rank(object):
    def get_ranks(self, graph, d=0.85): # d = damping factor
        A = graph
        matrix_size = A.shape[0]
        for id in range(matrix_size):
            A[id,id] = 0 # diagonal 부분을 0 으로 (diagonal matrix는 대각행렬)
            link_sum = np.sum(A[:,id]) # A[:,id] = A[:][id]
            if link_sum != 0:
                A[:,id] /= link_sum
            A[:,id] *= -d
            A[id, id] = 1
        
        B = (1-d) * np.ones((matrix_size, 1))
        ranks = np.linalg.solve(A,B) # 연립방정식 Ax = b
        return {idx: r[0] for idx, r in enumerate(ranks)}


# ### TextRank Class 구현

# In[118]:


class TextRank(object):
    def __init__(self, text):
        self.sent_tokenize =  SentenceTokenizer()
        
        if text[:5] in ('http:', 'https'):
            self.sentences = self.sent_tokenize.url2sentences(text)
        else:
            self.sentences = self.sent_tokenize.text2sentences(text)
        
        self.nouns = self.sent_tokenize.get_nouns(self.sentences)
        
        self.graph_matrix = GraphMatrix()
        self.sent_graph = self.graph_matrix.build_sent_graph(self.nouns)
        self.words_graph, self.idx2word = self.graph_matrix.build_words_graph(self.nouns)
        
        self.rank = Rank()
        self.sent_rank_idx = self.rank.get_ranks(self.sent_graph)
        self.sorted_sent_rank_idx = sorted(self.sent_rank_idx, key = lambda k:
                                          self.sent_rank_idx[k], reverse = True)
        self.word_rank_idx = self.rank.get_ranks(self.words_graph)
        self.sorted_word_rank_idx = sorted(self.word_rank_idx, key=lambda k:
                                           self.word_rank_idx[k], reverse=True)
    def summarize(self, sent_num=3):
        summary = []
        index = []
        for idx in self.sorted_sent_rank_idx[:sent_num]:
            index.append(idx)
        index.sort()
        for idx in index:
            summary.append(self.sentences[idx])
        
        return summary
    
    def keywords(self, word_num=10):
        rank = Rank()
        rank_idx = rank.get_ranks(self.words_graph)
        sorted_rank_idx = sorted(rank_idx, key=lambda k: rank_idx[k], reverse=True)
        
        keywords = []
        index = []
        for idx in sorted_rank_idx[:word_num]:
            index.append(idx)
        
        #index.sort()
        for idx in index:
            keywords.append(self.idx2word[idx])
        
        return keywords        


# In[119]:


textrank = TextRank(lines)
for row in textrank.summarize(3):
    print(row)
    print()
print('keywords :', textrank.keywords())


# In[ ]:




