# 회차 범위 직접 정해서 크롤링, 정식 웹툰만 가능

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import exceptions
from time import sleep
import pandas as pd

# 웹툰 정보 크롤링 함수
def crawler_info():
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    sleep(3)

    title = soup.find("title").get_text()    # 제목
    title = title.rstrip(" :: 네이버 만화")

    writer = soup.find("span",{"class":"wrt_nm"}).get_text()   # 작가
    writer = writer.lstrip("\n, \t")

    starScore = soup.find("span",{"id":"topPointTotalNumber"}).get_text()  # 별점

    episode = soup.find("div",{"class":"view"})  # 회차
    episode = episode.find("h3").get_text()

    info_date = soup.find("dd",{"class","date"}).get_text().replace(".","")  # 업로드 날짜

    dict_info = {"제목":title, "회차":episode, "작가":writer, "별점":starScore, "등록일":info_date}
    df_info = pd.DataFrame(dict_info, index=[0])
    return df_info

# 댓글 크롤링 시작 함수
def crawler_comment(url_episode):
    # 댓글 페이지로 이동
    url_comment = 'https://comic.naver.com/comment/comment.nhn?' + url_episode.split('?')[1]
    driver.get(url_comment)
    sleep(3)

    # 전체 댓글 더보기 클릭
    btn_all = driver.find_element_by_xpath('//*[@id="cbox_module"]/div/div[8]/a')
    btn_all.click()
    sleep(3)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    cnt_comment = soup.find("span",{"class":"u_cbox_count"}).get_text()
    cnt_comment = cnt_comment.replace(',',"")

    # 댓글이 총 1페이지일 때와 구분하여 크롤링
    if int(cnt_comment) <= 15:
        df_comment = comment_page1(soup)
    else:
        df_comment = comment_more(soup)

    return df_comment

# 1페이지 뿐일 때 댓글 크롤링 함수
def comment_page1(soup):
    comment_list = []
    recomm_list = []
    unrecomm_list = []
    date_list = []
    cnt_comment_list = []

    comments = soup.find_all("span", {"class":"u_cbox_contents"})   # 댓글 내용
    recomm = soup.find_all("em", {"class":"u_cbox_cnt_recomm"})     # 좋아요 수
    unrecomm = soup.find_all("em",{"class":"u_cbox_cnt_unrecomm"})  # 싫어요 수
    date = soup.find_all("span",{"class":"u_cbox_date"})            # 날짜
    cnt_comment = soup.find("span",{"class":"u_cbox_count"}).get_text()  # 총 댓글수
    cnt_comment = cnt_comment.replace(',',"")

    for line in comments:
        comment_list.append(line.string)

    for element in recomm:
        recomm_list.append(element.get_text())

    for element in unrecomm:
        unrecomm_list.append(element.get_text())

    for atag in date:
        date_list.append(atag['data-value'][:10].replace("-",""))

    for _ in range(int(cnt_comment)):
        cnt_comment_list.append(cnt_comment)

    dict_comment = {"댓글":comment_list, "좋아요":recomm_list, "싫어요":unrecomm_list, "날짜":date_list, "총 댓글수": cnt_comment_list}
    df_comment = pd.DataFrame(dict([(k,pd.Series(v)) for k,v in dict_comment.items()]))    # 클린봇으로 걸러진 댓글 NaN으로 처리
    df_comment = df_comment.dropna(axis=0)    # NaN 행 제거
    return df_comment

# 2페이지 이상일 때 댓글 크롤링 함수
def comment_more(soup):
    comment_list = []
    recomm_list = []
    unrecomm_list = []
    date_list = []
    cnt_comment_list = []

    cnt = 1
    boolean = True

    # 댓글 페이지 넘기면서 크롤링
    try:
        while True:
            next_xpath = '//*[@id="cbox_module"]/div/div[7]/div/a['+str(cnt)+']'
            btn_next = driver.find_element_by_xpath(next_xpath)
            btn_next.click()
            sleep(3)

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            sleep(3)

            comments = soup.find_all("span", {"class":"u_cbox_contents"})
            recomm = soup.find_all("em", {"class":"u_cbox_cnt_recomm"})
            unrecomm = soup.find_all("em",{"class":"u_cbox_cnt_unrecomm"})
            date = soup.find_all("span",{"class":"u_cbox_date"})
            cnt_comment = soup.find("span",{"class":"u_cbox_count"}).get_text()  # 총 댓글수
            cnt_comment = cnt_comment.replace(',',"")

            for line in comments:
                comment_list.append(line.string)

            for element in recomm:
                recomm_list.append(element.get_text())

            for element in unrecomm:
                unrecomm_list.append(element.get_text())

            for atag in date:
                date_list.append(atag['data-value'][:10].replace("-",""))

            for _ in range(int(cnt_comment)):
                cnt_comment_list.append(cnt_comment)

            cnt += 1

            if cnt == 12 and boolean == True:
                cnt = 3
                boolean = False
            elif cnt == 13:
                cnt = 3

    except exceptions.NoSuchElementException:
        print("해당 화 댓글 크롤링 종료")

    except Exception as e:
        print(e)

    dict_comment = {"댓글":comment_list, "좋아요":recomm_list, "싫어요":unrecomm_list, "날짜":date_list, "총 댓글수": cnt_comment_list}
    df_comment = pd.DataFrame(dict([(k,pd.Series(v)) for k,v in dict_comment.items()]))    # 클린봇으로 걸러진 댓글 NaN으로 처리
    df_comment = df_comment.dropna(axis=0)    # NaN 행 제거
    return df_comment

# 실행하면 모든 크롤링 시작되는 메인 함수, 실행 전에 회차 범위 정하기
def crawler_main():
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    sleep(2)

    # 한 화 페이지 주소 추출
    url = soup.find_all("meta", {"property": "og:url"})
    for atag in url:
        url = atag['content']
    url_list = url.replace("list","detail").split('&')

    df_info_all = pd.DataFrame()
    df_comment_all = pd.DataFrame()
    df_webtoon = pd.DataFrame()
    df_webtoon_all = pd.DataFrame()

    ######### range 안에 크롤링 할 회차 범위 설정해주기 #########
    # ex. 첫 화부터 5화까지 => range(1,6)
    for i in range(1,3):
        url_episode = url_list[0]+'&no='+str(i)+'&'+url_list[1]
        driver.get(url_episode)

        # 웹툰 정보 크롤링
        df_info = crawler_info()
        df_info_all = df_info_all.append(df_info, ignore_index=True)

        # 댓글 크롤링
        df_comment = crawler_comment(url_episode)
        df_comment_all = df_comment_all.append(df_comment, ignore_index=True)

        # 데이터 프레임 합치기
        df_webtoon = pd.concat([df_info, df_comment], axis=1).fillna(method = 'ffill')
        df_webtoon_all = df_webtoon_all.append(df_webtoon, ignore_index=True)
    return df_webtoon_all

# 드라이버 로드
driver = webdriver.Chrome('C:\\Program Files\\chromedriver')
driver.implicitly_wait(1)

# 해당 웹툰의 메인 페이지 주소 입력
html_web = 'https://comic.naver.com/webtoon/list.nhn?titleId=722542&weekday=fri'
driver.get(html_web)
sleep(2)

# 모든 크롤링 시작, 메인 함수에서 회차 범위 직접 설정해주고 실행하기
df_webtoon_all = crawler_main()

# 최종 DataFrame
#df_webtoon_all
