import os
import random
import threading
import time
from queue import Queue
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from x_functions import X_Functions
from tinsoft_proxy import TinSoft

_input_tweet = "div.public-DraftStyleDefault-block.public-DraftStyleDefault-ltr"
_tinsoft_api = 'TLT3KwQQAnQsExnq5mDDIMeXE9vQKOu8bSJd8N'
_cookie_path = 'cookies/'


def MultiLoginAndComment(child_acc, cookie_path):
    # login
    child_acc.LoginByCookie(cookie_path=cookie_path)


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


def RegAndSurf(child_acc, email, time_out, email_logged, cookie_path):
    child_acc.RegAcc(email=email, cookie_path=cookie_path)
    child_acc.SurfX(time_out)
    email_logged.append(email)


def LoginAndSurf(child_acc, time_out, cookie_path):
    child_acc.LoginByCookie(cookie_path=cookie_path)
    child_acc.SurfX(time_out)


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
        print(result)
        print(f'sleep: {time_sleep} until next request')
        time.sleep(time_sleep + 1)
        result = proxy.GetNewProxy()
    print(result)
    return result


if __name__ == "__main__":

    # use for handle proxy
    proxy = TinSoft(_tinsoft_api)

    # get email to reg acc
    # with open('email/mailTemp.txt', 'r') as file:
    #     emails = file.readlines()

    emails = os.listdir(_cookie_path)

    email_idx = 0

    while email_idx < len(emails):

        # get new proxy
        proxy_server = GetProxy(proxy)

        if not proxy_server['success']:
            print('cannot get proxy')
            break

        email_logged = []

        if len(emails) - email_idx <= 5:
            number_acc_use = len(emails)
        else:
            number_acc_use = 5

        # add proxy to Chrome
        service = Service(executable_path='./chromedriver-linux64/chromedriver')

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--proxy-server=%s' % proxy_server['proxy'])

        # chrome_options.add_argument('--proxy-server=116.104.241.237:31112')

        child_drivers = [webdriver.Chrome(service=service, options=chrome_options) for _ in range(number_acc_use)]
        child_acc = [X_Functions(child_drivers[idx], name=emails[email_idx + idx]) for idx in range(number_acc_use)]

        # regg & surf
        print('start multi login and comment')
        # t1 = [threading.Thread(target=RegAndSurf,
        #                        args=(child_acc[idx], emails[email_idx + idx], proxy_server['timeout'], email_logged,
        #                              _cookie_path))
        #       for idx in range(number_acc_use)]
        t1 = [threading.Thread(target=LoginAndSurf,
                               args=(child_acc[idx], proxy_server['timeout'], os.path.join(_cookie_path, emails[email_idx + idx])))
              for idx in range(number_acc_use)]

        # start thread
        thrds = []
        for t in t1:
            thrds.append(t)
            t.start()

        # wait for all task are done
        for thrd in thrds:
            thrd.join()

        # close all child driver
        for driver in child_drivers:
            driver.quit()

        # # if not comment -> no write logs
        # if not email_logged:
        #     continue

        # # write logs
        # print('writing logs')
        # with open('email/logged_email_7_days.txt', 'a') as file:
        #     file.write('\n')
        #     file.writelines(time.ctime())
        #     file.write('\n')
        #     for link in email_logged:
        #         file.writelines(link)
        #         # file.write('\n')
        #     print('write logs ok')

        # update email used
        email_idx += (number_acc_use + 1)
