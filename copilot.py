import time
import json
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


def ClickBtn(driver, div_type, text, time_sleep=3):
    elem = driver.find_element(By.XPATH, f"//{div_type}[text()='{text}']")
    elem.click()
    time.sleep(time_sleep)


def WriteInput(driver, div_inp_type, class_inp_name, div_submit_type, text_submit_name, text, time_sleep=3):
    elem = driver.find_element(By.XPATH, f"//{div_inp_type}[@class='{class_inp_name}']")
    elem.send_keys(text)
    time.sleep(time_sleep)
    ClickBtn(driver, div_submit_type, text_submit_name)


def SendInput(driver, title):
    # shadow_root -> https://www.youtube.com/watch?v=OhGY_ZNBsu0
    shadow_root = driver.find_element(By.CSS_SELECTOR, "cib-serp.cib-serp-main").shadow_root.find_element(
        By.CSS_SELECTOR, "cib-action-bar").shadow_root.find_element(By.CSS_SELECTOR, "cib-text-input").shadow_root
    # get input form
    elem = shadow_root.find_element(By.CLASS_NAME, "text-area")
    elem.send_keys(title)
    time.sleep(3)
    elem.send_keys(Keys.ENTER)
    time.sleep(3)
    GetGeneratedPost(driver)

def GetGeneratedPost(driver):
    shadow_root = driver.find_element(By.CSS_SELECTOR, "cib-serp.cib-serp-main").shadow_root.find_element(
        By.CSS_SELECTOR, "cib-action-bar").shadow_root
    try:
        elem = shadow_root.find_element(By.CSS_SELECTOR, "cib-typing-indicator[disabled]")
    except:
        print("post generating")
        time.sleep(1)
        GetGeneratedPost(driver)
    print("post generated, getting post")


if __name__ == "__main__":
    driver = webdriver.Chrome()
    driver.get("https://copilot.microsoft.com/")
    time.sleep(3)
    SendInput(driver, 'tell me about ww2')

    while 1:
        pass
