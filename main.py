import os
import random
import threading
import time
from queue import Queue
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from x_functions import X_Functions
from tinsoft_proxy import TinSoft

_ad_link_comment = "Looking for lucrative investment opportunities? Don't miss out! Simply click the link below, and we'll both receive 5 Doge coins if it's your first time signing up. Don't hesitate, this is your chance! https://reemebal.com/4/7335440"
_ad_link_comment = "📷📷HAMSTER KOMBAT is a very interesting event. It's truly a case of getting something for nothing."
"📷Those of you who don't know how to open and start working now: https://reemebal.com/4/7335440"
"📷Register to receive 5k coins immediately"
"📷$HAMTER KOMBAT is world cooperated"
_input_tweet = "div.public-DraftStyleDefault-block.public-DraftStyleDefault-ltr"
_tinsoft_api = 'TLT3KwQQAnQsExnq5mDDIMeXE9vQKOu8bSJd8N'


def MultiLoginAndComment(child_acc, cookie_path, profile_comment_link, content, _input_tweet, lock, usr_name, queue,
                         comment_links_by_usr):
    # login
    child_acc.LoginByCookie(cookie_path=cookie_path)

    # comment
    child_acc.CommentWithImage(post_link=profile_comment_link, content=content, _input_tweet=_input_tweet, lock=lock,
                               previous_comment=False)
    child_acc.CheckAccess()

    # get link just commented by acc
    commented_link = child_acc.GetCommentLink(usr_name=usr_name, queue=queue)
    child_acc.CheckAccess()

    # start lock for prevent race condition
    lock.acquire()
    comment_links_by_usr.append(commented_link)
    lock.release()

    # like comment
    # child_acc.LikeComment(comment_link_by_usr=comment_links_by_usr[len(comment_links_by_usr) - 1])
    # child_acc.CheckAccess()


def MultiLikeComment(cookie_path, name, comment_links_by_usr):
    driver_child_acc = webdriver.Chrome()

    # create obj
    child_acc = X_Functions(driver=driver_child_acc, name=name)

    # login
    child_acc.LoginWithCookie(cookie_path=cookie_path)

    # like comment
    for comment_link in comment_links_by_usr:
        child_acc.LikeComment(comment_link_by_usr=comment_link)

    # close driver
    driver_child_acc.quit()


def CreateContent():
    # get img path
    imgs_path = os.listdir('imgs/')

    # get all paragraphs from file
    with open('docs/spam_content.txt') as file:
        paragraphs = file.readlines()

    # make random content
    return [paragraphs[random.randint(0, len(paragraphs) - 1)], imgs_path[random.randint(0, len(imgs_path) - 1)]]


def GetProxy(proxy):
    print('getting new proxy')
    result = proxy.GetNewProxy()
    while result['success'] is False:
        time_sleep = result['next_change']
        print(f'sleep: {time_sleep} until next request')
        time.sleep(time_sleep)
        result = proxy.GetNewProxy()
    return result


if __name__ == "__main__":
    # lock for prevent race condition
    lock = threading.Lock()

    # create queue to get result from thread
    queue = Queue()

    # use for handle proxy
    proxy = TinSoft(_tinsoft_api)

    driver = webdriver.Chrome()
    main_acc = X_Functions(driver, 'main')
    main_acc.Login('lcurlis9ha1a@amachadoespera.com')

    # get all the porn link in file
    with open('link_list/porn_link.txt', 'r') as file:
        profile_links = file.readlines()

    # get all cookies
    cookies = os.listdir('cookies/')
    child_acc_name = [cookies[idx][cookies[idx].find('_') + 1:cookies[idx].find('.')] for idx in range(len(cookies))]

    for profile_link in profile_links:

        # get new proxy
        proxy_server = GetProxy(proxy)

        if not proxy_server['success']:
            print('cannot get proxy')
            break

        comment_links_by_usr = []

        # get post from usr profile
        print('getting comment')
        post_links = main_acc.CrawPost(number_of_post=3, profile_link=profile_link)

        number_acc_use = len(post_links)

        # check the number of remaining acc
        # used 3 acc for comment
        if 3 > len(cookies) > 0:
            number_acc_use = len(cookies)
        if len(cookies) <= 0:
            break

        # add proxy to Chrome
        service = Service(executable_path='./chromedriver-linux64/chromedriver')
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--proxy-server=%s' % proxy_server['proxy'])

        child_drivers = [webdriver.Chrome(service=service, options=chrome_options) for _ in range(number_acc_use)]
        child_acc = [X_Functions(child_drivers[idx], name=child_acc_name[idx]) for idx in range(number_acc_use)]

        # Login, comment & like
        print('start multi login and comment')
        t1 = [threading.Thread(target=MultiLoginAndComment, args=(
            child_acc[idx], f'{os.getcwd()}/cookies/{cookies[idx]}', post_links[idx], CreateContent(), _input_tweet,
            lock, child_acc_name[idx], queue,
            comment_links_by_usr)) for idx in range(number_acc_use)]

        # start thread
        thrds = []
        for t in t1:
            thrds.append(t)
            t.start()

        # wait for all task are done
        for thrd in thrds:
            thrd.join()

        # remove cookies and name used from list
        for idx in range(number_acc_use):
            cookies.remove(cookies[idx])
            child_acc_name.remove(child_acc_name[idx])

        # close all child driver
        for driver in child_drivers:
            driver.quit()

        # if not comment -> no write logs
        if not comment_links_by_usr:
            continue

        # write logs
        print('writing logs')
        with open('docs/commented_links.txt', 'a') as file:
            file.write('\n')
            file.writelines(time.ctime())
            file.write('\n')
            for link in comment_links_by_usr:
                file.writelines(link)
                file.write('\n')
            print('write logs ok')

        # # comment
        # print('start multi comment')
        # t1 = [threading.Thread(target=child_acc[idx].CommentWithImage, args=(
        #     comment_links[idx], CreateContent(), _input_tweet, lock,)) for idx in range(number_acc_use)]
        #
        # # start thread
        # thrds = []
        # for t in t1:
        #     thrds.append(t)
        #     t.start()
        #
        # # wait for all task are done
        # for thrd in thrds:
        #     thrd.join()
        #
        # # get link commented
        # print('start multi get link commented')
        # t1 = [threading.Thread(target=child_acc[idx].GetCommentLink, args=(
        #     child_acc_name[idx], queue,)) for idx in range(number_acc_use)]
        #
        # # start thread
        # thrds = []
        # for t in t1:
        #     thrds.append(t)
        #     t.start()
        #
        # # wait for all task are done
        # for thrd in thrds:
        #     thrd.join()
        #
        # # get result from thread
        # comment_links_by_usr = []
        # while not queue.empty():
        #     comment_links_by_usr.append(queue.get())
        # print(f'link commented: {comment_links_by_usr}')

        # write log

    # post_list = main_acc.GetComment(number_of_comment=3, link='https://x.com/UyenNhi3x')
    # main_acc.CommentWithImage(comment_link='https://x.com/wilfong255kv/status/1807253256764317810/',
    #                           _input_tweet=_input_tweet, text='adfdsaf', img_name='asdf')
    # main_acc.GetCommentLink(usr_name='LulitaC36489')
    # main_acc.LikeComment('https://x.com/LulitaC36489/status/1807801425717846291')
    # while 1:
    #     pass

    # asyncio.run(craw_acc.LoginWithCookie('cookies/wraisbeckbja1a@amachadoespera_WRaisbeck53282.pkl'))
    #
    # while 1:
    #     pass
    # community_link = 'https://x.com/cogiaomoon69'
    # comment_link_list = craw_acc.CrawlMostViewComment(community_link=community_link, number_of_comment_link=20)
    #
    # with open('link_list/co_giao_lon_ton.txt', 'w') as file:
    #     for link in comment_link_list:
    #         file.writelines(link+'\n')

    # i = 0
    # print('starting async')
    # while i < len(comment_link_list):
    #     asyncio.run(main(community_link=community_link, comment_link_list=comment_link_list, len=i))
    #     i += 5
    #
    # while 1:
    #     pass

    # community_list = craw_acc.CrawlMostViewComment('https://x.com/i/communities/1506800881525829633')
    # print(community_list)

    # p1 = threading.Thread(target=between_callback, args=('jemanuele99a1a@amachadoespera.com',))
    # p1.start()

    # p2 = threading.Thread(target=between_callback, args=(cookie_path_2,))
    # p2.start()
    #
    # p3 = threading.Thread(target=between_callback, args=(cookie_path_3,))
    # p3.start()
    #
    # p4 = threading.Thread(target=between_callback, args=(cookie_path_4,))
    # p4.start()
