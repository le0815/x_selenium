import pickle
import asyncio
import threading
import time

from selenium.webdriver.common.by import By

from reg_x import RegX
from selenium.webdriver import ActionChains, Keys
from selenium import webdriver


def GetCookie(driver, email, usr_name):
    pickle.dump(driver.get_cookies(), open(f"cookies/{email[:email.find('.')]}_{usr_name}.pkl", "wb"))
    print('get cookies success')


with open('../email/logged_email.txt', 'r') as file:
    emails = file.readlines()

_email_pwd = '13579thanG$'
# _usr_name_input = 'r-30o5oe.r-1dz5y72.r-13qz1uu.r-1niwhzg.r-17gur6a.r-1yadl64.r-deolkf.r-homxoj.r-poiln3.r-7cikom.r-1ny4l3l.r-t60dpp.r-fdjqy7'
count = 0

for email in emails:
    if email == '\n':
        break
    print(f'getting cookie for: {email}')
    cookie_driver = webdriver.Chrome()
    x_driver = RegX(driver=cookie_driver)
    login = x_driver.Login(email=email)
    usr_name = ''
    for value in login:
        usr_name = value
    GetCookie(cookie_driver, email, usr_name)
    cookie_driver.close()
    print(f'count: {count}')
    count += 1
