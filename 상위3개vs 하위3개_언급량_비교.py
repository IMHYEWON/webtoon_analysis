#!/usr/bin/env python
# coding: utf-8

# In[1]:


import GetOldTweets3 as got
import datetime
import time
import pandas as pd
from random import uniform
from tqdm import tqdm_notebook


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
    
    start_date = days_range[0]
    end_date = (datetime.datetime.strptime(days_range[-1], "%Y-%m-%d")
               + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    search_input = input()
    tweetCriteria = got.manager.TweetCriteria().setQuerySearch(search_input)                                           .setSince(start_date)                                           .setUntil(end_date)                                           .setMaxTweets(-1)
    print("Collecting data start.. from {} to {}".format(days_range[0], days_range[-1]))
    start_time = time.time()
    
    tweet = got.manager.TweetManager.getTweets(tweetCriteria)
    
    print("Collecting data end.. {0:0.2f} Minutes".format((time.time() - start_time)/60))
    print("=== Total num of tweets is {} ===".format(len(tweet)))


# In[45]:


# 하위 웹툰 3개월 언급 개수
day()
worst_1 = tweetCriteria()
worst_2 = tweetCriteria()
worst_3 = tweetCriteria()


# In[10]:


# 상위 웹툰 3개월 언급 개수
day()
best_1 = tweetCriteria()
best_2 = tweetCriteria()
best_3 = tweetCriteria()


# In[46]:


import pandas as pd
from pandas import DataFrame as df
import matplotlib.pyplot as plt
import matplotlib as mpl
get_ipython().run_line_magic('matplotlib', 'inline')

Worst_df = df(data={'Worst_Name':['악마와 계약연애','8월의 눈보라','안녕,대학생'],
                   'Amount':[214,25,228]})
Best_df = df(data={'Best_Name':['연애혁명','유미의 세포들','여신강림'],
                  'Amount':[1421,1294, 5773]})


# In[47]:


Worst_df


# In[48]:


Best_df


# In[ ]:




