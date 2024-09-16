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
    # proxy = TinSoft(_tinsoft_api)

    driver = webdriver.Chrome()
    main_acc = X_Functions(driver, 'main')
    main_acc.Login('lcurlis9ha1a@amachadoespera.com')
    # main_acc.Login('vipboy2903200321phu@gmail.com')

    while 1:
        pass

    main_acc.SurfX(200000)

