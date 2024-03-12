import time
import json
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

usr_name = "@NgCHn22001358"
pwd = "quyetdoanlen"


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
    time.sleep(3)
    # input usr_name and submit
    print("write usr_name")
    WriteInput(driver, "input",
               "r-30o5oe r-1dz5y72 r-13qz1uu r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-t60dpp r-fdjqy7",
               "span",
               "Next",
               text=usr_name)
    # input pwd and login
    print("write pwd")
    WriteInput(driver, "input",
               "r-30o5oe r-1dz5y72 r-13qz1uu r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-t60dpp r-fdjqy7",
               "span",
               "Log in",
               text=pwd)


if __name__ == "__main__":
    driver = webdriver.Chrome()
    driver.get("https://copilot.microsoft.com/")
    time.sleep(3)
    # elems = driver.find_element(By.XPATH, "/html[1]/body[1]/div[1]/cib-serp[1]")
    # time.sleep(3)
    # elem = driver.execute_script("return document.querySelector('textarea#text-area').sh")
    # shadow_root -> https://stackoverflow.com/questions/69585279/unable-to-click-on-shadow-root-element-using-selenium
    elem = driver.execute_script("document.querySelector('cib-serp.cib-serp-main').shadowRoot.querySelector('cib-action-bar').shadowRoot.querySelector('cib-text-input').shadowRoot.querySelector('textarea')")

    print("ok")
    while 1:
        pass

