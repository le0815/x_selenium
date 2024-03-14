import time
import json
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

post_prompt = "create twitter post  related to the hashtag: "
img_prompt = "create a image with hashtag: "
default_download_path = "/home/ha/PycharmProjects/x_selenium/generated_img"


def ClickBtn(driver, div_type, text, time_sleep=3):
    elem = driver.find_element(By.XPATH, f"//{div_type}[text()='{text}']")
    elem.click()
    time.sleep(time_sleep)


def WriteInput(driver, div_inp_type, class_inp_name, div_submit_type, text_submit_name, text, time_sleep=3):
    elem = driver.find_element(By.XPATH, f"//{div_inp_type}[@class='{class_inp_name}']")
    elem.send_keys(text)
    time.sleep(time_sleep)
    ClickBtn(driver, div_submit_type, text_submit_name)


def SendInput(driver, input_content):
    # shadow_root -> https://www.youtube.com/watch?v=OhGY_ZNBsu0
    shadow_root = driver.find_element(By.CSS_SELECTOR, "cib-serp.cib-serp-main").shadow_root.find_element(
        By.CSS_SELECTOR, "cib-action-bar").shadow_root.find_element(By.CSS_SELECTOR, "cib-text-input").shadow_root
    # get input form
    elem = shadow_root.find_element(By.CLASS_NAME, "text-area")
    elem.send_keys(input_content)
    time.sleep(1)
    elem.send_keys(Keys.ENTER)
    time.sleep(3)
    # GetGeneratedPost(driver)
    GetGeneratedImage(driver)

def GetGeneratedPost(driver):
    shadow_root = driver.find_element(By.CSS_SELECTOR, "cib-serp.cib-serp-main").shadow_root.find_element(
        By.CSS_SELECTOR, "cib-action-bar").shadow_root
    try:
        elem = shadow_root.find_element(By.CSS_SELECTOR, "cib-typing-indicator[disabled]")
        print("post generated, getting post")
        post_generated = driver.execute_script("return document.querySelector('cib-serp.cib-serp-main').shadowRoot"
                                               ".querySelector("
                                               "'cib-conversation#cib-conversation-main').shadowRoot.querySelector("
                                               "'cib-chat-turn').shadowRoot.querySelector("
                                               "'cib-message-group.response-message-group').shadowRoot.querySelector("
                                               "'cib-message').shadowRoot.querySelector('cib-code-block').getAttribute("
                                               "'clipboard-data')")

        print(f"text generated: {post_generated}")
    except:
        print("post generating")
        time.sleep(2)
        GetGeneratedPost(driver)


def GetGeneratedImage(driver):
    # shadow_root -> https://www.youtube.com/watch?v=OhGY_ZNBsu0
    # switch to designer mode
    print("switch to designer mode")
    shadow_root = (driver.find_element(By.CSS_SELECTOR, "cib-serp.cib-serp-main").shadow_root.
                   find_element(By.CSS_SELECTOR, "cib-conversation#cib-conversation-main").
                   find_element(By.CSS_SELECTOR, "cib-side-panel").shadow_root.
                   find_element(By.CSS_SELECTOR, "cib-free-sydney-persona").shadow_root
                   )
    elem = shadow_root.find_element(By.CSS_SELECTOR, "button")
    elem.click()


if __name__ == "__main__":
    # set default download path
    option = webdriver.ChromeOptions()
    prefs = {"download.default_directory": default_download_path}
    option.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(options=option)

    driver.get("https://copilot.microsoft.com/")
    time.sleep(3)
    # SendInput(driver, post_prompt)
    GetGeneratedImage(driver)
    while 1:
        pass
