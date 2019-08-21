#!/usr/bin/env python
# coding: utf-8

# In[1]:


# 가담항설, 이영싫, 신의탑
import GetOldTweets3 as got
import datetime
import time
from random import uniform
from tqdm import tqdm_notebook
import pandas as pd
import matplotlib.pyplot as plt


# In[2]:


def day():
    global days_range
    days_range = []
    start_input = input()
    end_input = input()
    start = datetime.datetime.strptime(start_input, "%Y-%m-%d")
    end = datetime.datetime.strptime(end_input, "%Y-%m-%d")
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]
    
    for date in date_generated:
        days_range.append(date.strftime("%Y-%m-%d"))
        
    print("=== 설정된 트윗 수집 기간은 {} 에서 {} 까지 입니다 ===".format(days_range[0], days_range[-1]))
    print("=== 총 {}일 간의 데이터 수집 ===".format(len(days_range)))


# In[3]:


def tweetCriteria():
    global tweet
    
    # 수집 기간 맞추기
    start_date = days_range[0]
    end_date = (datetime.datetime.strptime(days_range[-1], "%Y-%m-%d")
               + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    
    # 트윗 수집 기준 정의
    search_input = input()
    tweetCriteria = got.manager.TweetCriteria().setQuerySearch(search_input)                                           .setSince(start_date)                                           .setUntil(end_date)                                           .setMaxTweets(-1)
    print("Collecting data start.. from {} to {}".format(days_range[0], days_range[-1]))
    start_time = time.time()
    
    tweet = got.manager.TweetManager.getTweets(tweetCriteria)
    
    # 수집 wirh GetOldTweet3
    print("Collecting data end.. {0:0.2f} Minutes".format((time.time() - start_time)/60))
    print("=== Total num of tweets is {} ===".format(len(tweet)))


# In[4]:


# 변수 저장하기
# 유저 아이디, 트윗 링크, 트윗 내용, 날짜, 리트윗 수, 관심글 수 수집 가능
# 원하는 변수 골라서 저장하기
def crawling():
    #initialize
    global tweet_list
    tweet_list = []
    
    for index in tqdm_notebook(tweet):
        # 메타데이터 목록
        # username = index.username
        # link = index.permalink 
        content = index.text
        tweet_date = index.date.strftime("%Y-%m-%d")
        # tweet_time = index.date.strftime("%H:%M:%S")
        # retweets = index.retweets
        # favorites = index.favorites
        
        # 결과 합치기
        info_list = [tweet_date, content]
        tweet_list.append(info_list)
        
        # 휴식
        time.sleep(uniform(1,2))


# In[6]:


day()
tweetCriteria()
crawling()


# In[7]:


day()
tweetCriteria()
crawling()


# In[9]:


day()
tweetCriteria()
crawling()


# In[28]:


from pandas import DataFrame as df

Tbest_df = df(data={'Name':['가담항설','신의탑','이영싫'],
                    'Amount':['1194','1671','3272']})
Tbest_df


# In[ ]:




