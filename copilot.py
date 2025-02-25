import asyncio
import pickle
import time
import json
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

_default_download_path_ = "/home/ha/PycharmProjects/x_selenium/generated_img"
_home_page_ = 'https://copilot.microsoft.com/'
_signin_page_ = "https://copilot.microsoft.com/?wlexpsignin=1"
def ClickBtn(driver, div_type, text, time_sleep=3):
    elem = driver.find_element(By.XPATH, f"//{div_type}[text()='{text}']")
    elem.click()
    time.sleep(time_sleep)


def WriteInput(driver, div_inp_type, class_inp_name, div_submit_type, text_submit_name, text, time_sleep=3):
    elem = driver.find_element(By.XPATH, f"//{div_inp_type}[@class='{class_inp_name}']")
    elem.send_keys(text)
    time.sleep(time_sleep)
    ClickBtn(driver, div_submit_type, text_submit_name)


async def SendInput(driver, prompt):

    print(f"input prompt for: {prompt}")

    # shadow_root -> https://www.youtube.com/watch?v=OhGY_ZNBsu0
    # if page load not correctly -> try reload
    try:
        print("getting input form for copilot")
        shadow_root = driver.find_element(By.CSS_SELECTOR, "cib-serp.cib-serp-main").shadow_root.find_element(
            By.CSS_SELECTOR, "cib-action-bar").shadow_root.find_element(By.CSS_SELECTOR, "cib-text-input").shadow_root

        # get input form
        elem = shadow_root.find_element(By.CLASS_NAME, "text-area")
        elem.send_keys(prompt)
        await asyncio.sleep(1)
        elem.send_keys(Keys.ENTER)
        await asyncio.sleep(3)

    except:
        print('error while sending prompt for copilot')


async def GetGeneratedPost(driver, prompt):
    await SetCookie(driver)
    await asyncio.sleep(3)
    await SendInput(driver, prompt)
    # get text generated
    shadow_root = driver.find_element(By.CSS_SELECTOR, "cib-serp.cib-serp-main").shadow_root.find_element(
        By.CSS_SELECTOR, "cib-action-bar#cib-action-bar-main").shadow_root

    while 1:
        try:
            elem = shadow_root.find_element(By.CSS_SELECTOR, "cib-typing-indicator[disabled]")
            print("post generated, getting post")
            break
        except:
            print("post generating")
            await asyncio.sleep(2)
    # signin version
    try:
        post_generated = driver.execute_script("return document.querySelector('cib-serp.cib-serp-main').shadowRoot"
                                       ".querySelector("
                                       "'cib-conversation#cib-conversation-main').shadowRoot.querySelector("
                                       "'cib-chat-turn').shadowRoot.querySelector("
                                       "'cib-message-group.response-message-group').shadowRoot.querySelector("
                                       "'cib-message').shadowRoot.querySelector('cib-code-block').getAttribute("
                                       "'clipboard-data')")
    except:
        print('cannot get tweet')
        post_generated = None
    # not signin version
    # shadow_root = (driver.find_element(By.CSS_SELECTOR, "cib-serp.cib-serp-main").shadow_root.
    #                find_element(By.CSS_SELECTOR, "cib-conversation#cib-conversation-main").shadow_root.
    #                find_element(By.CSS_SELECTOR, "cib-chat-turn").shadow_root.
    #                find_element(By.CSS_SELECTOR, "cib-message-group.response-message-group").shadow_root.
    #                find_element(By.CSS_SELECTOR, "cib-message").shadow_root
    #                )
    # elem = shadow_root.find_element(By.CSS_SELECTOR, "div.ac-textBlock")
    # post_generated = elem.text

    print(f"text generated: {post_generated}")
    return post_generated


def GetGeneratedImage(driver, prompt):
    # shadow_root -> https://www.youtube.com/watch?v=OhGY_ZNBsu0
    # switch to designer mode
    print("switch to designer mode")
    shadow_root = (driver.find_element(By.CSS_SELECTOR, "cib-serp.cib-serp-main").shadow_root.
                   find_element(By.CSS_SELECTOR, "cib-conversation#cib-conversation-main").
                   find_element(By.CSS_SELECTOR, "cib-side-panel").shadow_root.
                   find_element(By.CSS_SELECTOR, "cib-free-sydney-persona[personatype='Designer']").shadow_root
                   )
    elem = shadow_root.find_element(By.CSS_SELECTOR, "button")
    elem.click()
    # insert prompt to generate text
    SendInput(driver, prompt)


def GetCookie(driver):
    driver.get(_home_page_)
    while 1:
        if driver.current_url == _signin_page_:
            pickle.dump(driver.get_cookies(), open("cookies/copilot_cookies.pkl", "wb"))
            print('got cookie')
            break


async def SetCookie(driver):
    driver.get(_home_page_)
    await asyncio.sleep(3)
    print("setting cookie for copilot")
    cookies = pickle.load(open("cookies/copilot_cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    await asyncio.sleep(1)
    print("setting cookie for copilot success -> redirect to the login page")
    driver.get(_home_page_)


# if __name__ == "__main__":
#     # set default download path
#     option = webdriver.ChromeOptions()
#     prefs = {"download.default_directory": default_download_path}
#     option.add_experimental_option('prefs', prefs)
#     driver = webdriver.Chrome(options=option)
#     asyncio.run(GetGeneratedPost(driver, 'make a tweet with hashtags: St Patrick. The output is place in code tag.'))
#     # GetCookie(driver)
#
#     while 1:
#         pass
