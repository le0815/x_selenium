import pickle
import time

import pyperclip

import copilot
import json
import asyncio
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

__usr_name = "@NgCHn22001358"
__pwd = "quyetdoanlen"
# edge version
# _input_tweet = "//html/body/div/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div/div/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/div/label/div/div/div/div/div/div/div[2]/div/div/div/div"
# chrome version
_input_tweet = "div.public-DraftStyleDefault-block.public-DraftStyleDefault-ltr"
_post_prompt = "make a tweet with hashtags: %s. The output is place in code div"
_img_prompt = "create a image with hashtag: tiktok"
_ad_link_post = "\n Click now to get 5 Doge FREE: https://doostozoa.net/4/7335440"
_ad_link_comment = "\n Click now to get 5 Doge FREE: https://domuipan.com/4/7335444"
_comment_prompt = "ok"
post_commented = []


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


async def Scroll(driver):
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
    while scroll_times <= 2:
        # Scroll down to bottom
        for i in range(8, 0, -1):
            print(f"scroll time: {scroll_times}")
            driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight/{i});")
            # comment
            if i == 4:
                Comment(driver)
            # Wait to load page
            await asyncio.sleep(2)
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
    print('refreshing page')
    driver.refresh()
    await asyncio.sleep(5)


async def GetTrend(driver):
    # get list trends
    print("redirect to trending page")
    driver.get("https://twitter.com/i/trends")
    print("crawling trending")
    # wait for page loading
    await asyncio.sleep(5)
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


async def SetCookie(driver, cookie_path):
    driver.get("https://twitter.com/home")
    await asyncio.sleep(3)
    print("setting cookie")
    cookies = pickle.load(open(f"{cookie_path}", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    await asyncio.sleep(1)
    print("setting cookie success -> redirect to the login page")
    driver.get("https://twitter.com/home")
    await asyncio.sleep(3)


def Comment(driver):
    print('commenting')

    # get list current post
    elems = driver.find_elements(By.CSS_SELECTOR, "div.css-175oi2r.r-1iusvr4.r-16y2uox.r-1777fci.r-kzbkwu")
    for elem in elems:
        try:
            poster = elem.text[:elem.text.find('·')]
        except:
            print('getting post err')
            continue
        print(f"poster: {poster}")
        if poster in post_commented:
            print("post was commented")
            continue

        # scroll to element
        try:
            print("scrolling to post")
            ActionChains(driver).scroll_to_element(elem).perform()
        except:
            print("cannot scroll to post")
            continue

        # open post in new tab
        try:
            print("clicking to post")
            new_post = ActionChains(driver)
            new_post.key_down(Keys.CONTROL).click(elem).key_up(Keys.CONTROL).perform()
        except:
            print("cannot open post to new tab")
            continue

        # switch to new post tab
        try:
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(5)
        except:
            print("cannot switch to new tab")
            continue

        # find comment icon
        try:
            print("commenting")
            comment_input = driver.find_element(By.CSS_SELECTOR, _input_tweet)
            time.sleep(2)
            comment_input.send_keys(_ad_link_comment)
        except:
            scroll_down = ActionChains(driver)
            scroll_down.send_keys(Keys.PAGE_DOWN)
            time.sleep(1)
            scroll_down.send_keys(Keys.PAGE_DOWN)
            try:
                comment_input = driver.find_element(By.CSS_SELECTOR, _input_tweet)
                time.sleep(2)
                comment_input.send_keys(_ad_link_comment)
            except:
                print("cannot scroll, try again")

                # close new post tab
                driver.close()
                print("new tab closed")

                # switch driver to main tab
                print("switch to main tab")
                driver.switch_to.window(driver.window_handles[0])

                continue

        # use shortcut to submit
        print("sending key stroke to submit")
        comment_input.send_keys(Keys.CONTROL + Keys.ENTER)
        time.sleep(3)
        # add usr_acc to list
        post_commented.append(poster)
        print(f"commented for post: {post_commented}")
        print(f"post_commented: {post_commented}")

        # close new post tab
        driver.close()
        print("new tab closed")

        # switch driver to main tab
        print("switch to main tab")
        driver.switch_to.window(driver.window_handles[0])

        break


async def Tweet(driver, post):
    await asyncio.sleep(3)
    print("insert post to tweet")
    elem = driver.find_element(By.CSS_SELECTOR, _input_tweet)
    await asyncio.sleep(1)
    pyperclip.copy(post)
    elem.send_keys(Keys.CONTROL + 'v')
    await asyncio.sleep(1)
    elem.send_keys(Keys.CONTROL + Keys.ENTER)
    await asyncio.sleep(5)
    print('posted')


async def main(cookie_path):
    driver = webdriver.Chrome()
    driver_2 = webdriver.Chrome()
    await SetCookie(driver, cookie_path)
    trending_title_list = await GetTrend(driver)
    loop_count = len(trending_title_list)
    for trending_title in trending_title_list:
        print(f"loop for tweet: {loop_count}")
        loop_count -= 1
        task_1 = asyncio.create_task(Scroll(driver))
        task_2 = asyncio.create_task(copilot.GetGeneratedPost(driver_2, _post_prompt % trending_title))
        tasks = [task_1, task_2]

        # wait for all task are complete
        # await asyncio.gather(*asyncio.all_tasks())
        done, pending = await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)

        # iterator finished task
        for future in done:
            result = future.result()
            print(f"async result type: {result} \n name: {future.get_name()}")
            if result is not None:
                await Tweet(driver, f"{result}\n{_ad_link_post}")

    print(f"posted {loop_count}: tweet")


async def test(driver):
    await SetCookie(driver)
    loop_count = 20
    for trending_title in range(20):
        print(f"loop for tweet: {loop_count}")
        loop_count -= 1
        task_1 = asyncio.create_task(Scroll(driver))

        # wait for all task are complete
        # await asyncio.gather(*asyncio.all_tasks())
        done, pending = await asyncio.wait(task_1, return_when=asyncio.ALL_COMPLETED)

        # iterator finished task
        for future in done:
            result = future.result()
            print(f"async result type: {result} \n name: {future.get_name()}")
            if result is not None:
                await Tweet(driver, result)

# if __name__ == "__main__":
#     driver = webdriver.Chrome()
#
#     # use for copilot.py
#     driver_2 = webdriver.Chrome()
#
#     asyncio.run(main())
#     # asyncio.run(test(driver))
#     # Scroll(driver)
#     while 1:
#         pass
