import pickle
import time

from selenium import webdriver
from crawl_community import CrawlCommunity


def GetCookie():
    driver = webdriver.Chrome()
    driver.get('https://x.com/')
    while 1:
        if driver.current_url == "https://x.com/home":
            time.sleep(3)
            pickle.dump(driver.get_cookies(), open("comment_acc_1.pkl", "wb"))
            break


def LoginWithCookie(cookie_path):
    driver = webdriver.Chrome()
    print(f'Login with cookie')
    driver.get("https://x.com")
    time.sleep(3)
    print(f"setting cookie")
    cookies = pickle.load(open(f"{cookie_path}", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    time.sleep(1)
    print(f"setting cookie success -> redirect to the login page")
    driver.get("https://x.com/home")
    time.sleep(3)

    # if 'https://x.com/home' not in driver.current_url:
    #     return cookie_path
    # driver.quit()

    if 'https://x.com/home' not in driver.current_url:
        raise ValueError(
            f'general exceptions not caught by specific handling, current url: {driver.current_url}')


# arr = [LoginWithCookie(cookie_path=f"cookies/comment_acc_{i}.pkl") for i in range(11)]

LoginWithCookie(cookie_path=f"cookies/comment_acc_1.pkl")
