import pickle
import time
import copilot
import json
import asyncio
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

__usr_name = "@NgCHn22001358"
__pwd = "quyetdoanlen"
__input_tweet = "//html/body/div/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div/div/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/div/label/div/div/div/div/div/div/div[2]/div/div/div/div"
__post_prompt = "create twitter post  related to the hashtag: "
__img_prompt = "create a image with hashtag: tiktok"


def ClickBtn(driver, div_type, text, time_sleep=3):
    elem = driver.find_element(By.XPATH, f"//{div_type}[text()='{text}']")
    elem.click()
    time.sleep(time_sleep)


def WriteInput(driver, div_inp_type, class_inp_name, div_submit_type, text_submit_name, text, time_sleep=3):
    elem = driver.find_element(By.XPATH, f"//{div_inp_type}[@class='{class_inp_name}']")
    elem.send_keys(text)
    time.sleep(time_sleep)
    ClickBtn(driver, div_submit_type, text_submit_name)


def Login(driver):
    driver.get("https://twitter.com/i/flow/login")
    time.sleep(5)
    # input usr_name and submit
    print("write usr_name")
    WriteInput(driver, "input",
               "r-30o5oe r-1dz5y72 r-13qz1uu r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-t60dpp r-fdjqy7",
               "span",
               "Next",
               text=__usr_name, time_sleep=1)
    time.sleep(5)
    # input pwd and login
    print("write pwd")
    WriteInput(driver, "input",
               "r-30o5oe r-1dz5y72 r-13qz1uu r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-t60dpp r-fdjqy7",
               "span",
               "Log in",
               text=__pwd, time_sleep=1)


def Scroll(driver):
    # return homepage
    driver.get("https://twitter.com/home")
    # if appear popup require 2FA -> close pop up
    try:
        elem = driver.find_element(By.XPATH, "//span[text()='Tăng cường bảo mật tài khoản của bạn']")
        print("have pop up -> closing")
        # click close btn
        ClickBtn(driver, "div",
                 "css-175oi2r r-sdzlij r-1phboty r-rs99b7 r-lrvibr r-2yi16 r-1qi8awa r-1loqt21 r-o7ynqc r-6416eg r-1ny4l3l")
    except:
        print("no popup")

    print("scrolling")
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    # scroll 10 times
    scroll_times = 0
    while scroll_times <= 3:
        # Scroll down to bottom
        for i in range(8, 0, -1):
            print(f"scroll time: {scroll_times}")
            driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight/{i});")
            # Wait to load page
            time.sleep(2)
            print(f"scroll loop: {i}")

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print("cannot load newsfeed")
            break
        last_height = new_height
        scroll_times += 1

    print("scroll finish")
    # refresh page to turn back top page
    driver.refresh()


def GetTrend(driver):
    # get list trends
    print("redirect to trending page")
    driver.get("https://twitter.com/i/trends")
    print("crawling trending")
    # wait for page loading
    time.sleep(3)
    trending_title_list = []
    elms = driver.find_elements(By.XPATH,
                                "//div[@class='css-1rynq56 r-bcqeeo r-qvutc0 r-37j5jr r-a023e6 r-rjixqe r-b88u0q r-1bymd8e']")
    # print(type(elms))
    for elm in elms:
        title = elm.text
        print("Trending: " + title)
        trending_title_list.append(title)
    print("crawling trending finish")
    return trending_title_list


def GetCookie(driver):
    driver.get('https://twitter.com/i/flow/login')
    while 1:
        if driver.current_url == "https://twitter.com/home":
            pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
            break


def SetCookie(driver):
    driver.get("https://twitter.com/home")
    time.sleep(3)
    print("setting cookie")
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    time.sleep(1)
    print("setting cookie success -> redirect to the login page")
    driver.get("https://twitter.com/home")


def Tweet(driver, post):
    print("insert post to tweet")
    elem = driver.find_element(By.XPATH, __input_tweet)
    time.sleep(1)
    elem.send_keys(post)


async def main():
    SetCookie(driver)
    GetTrend(driver)
    trending_title_list = GetTrend(driver)
    loop_count = len(trending_title_list)
    for trending_title in trending_title_list:
        print(f"loop: {loop_count}")
        loop_count += 1
        task_1 = asyncio.create_task(Scroll(driver))
        task_2 = asyncio.create_task(copilot.GetGeneratedPost(driver_2, __post_prompt + trending_title))
        tasks = [task_1, task_2]
        # wait for all task are complete
        done, pending = await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)

        # iterator finished task
        for future in pending:
            print("pending task")
            result = future.get_name()

        # iterator finished task
        for future in done:
            result = future.result()
            if result is not None:
                Tweet(driver, 'test')


if __name__ == "__main__":
    driver = webdriver.Chrome()
    # use for copilot.py
    driver_2 = webdriver.Chrome()
    asyncio.run(main())
    # Scroll(driver)
    while 1:
        pass
