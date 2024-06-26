import pickle
import shutil
import signal
import sys
import time
import os
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.proxy import *

__usr_name = "@NgCHn22001358"
__pwd = "quyetdoanlen"
_email_pwd = "13579thanG$"


# edge version
# _input_tweet = "//html/body/div/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div/div/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/div/label/div/div/div/div/div/div/div[2]/div/div/div/div"
# chrome version

class RegX:
    def __init__(self, driver):
        self.driver = driver
    def WriteInput(self, div_inp_type, class_inp_name, div_submit_type, text_submit_name, text, time_sleep=3):
        elem = self.driver.find_element(By.XPATH, f"//{div_inp_type}[@class='{class_inp_name}']")
        elem.send_keys(text)
        time.sleep(time_sleep)

    def CopyGuestProfile(self):
        guest_profile_path = "/home/ha/PycharmProjects/x_selenium/chrome_profile/Profile 2"
        copy_guest_profile_path = "/home/ha/PycharmProjects/x_selenium/chrome_profile/Profile 3"

        try:
            shutil.copytree(guest_profile_path, copy_guest_profile_path)
            print("create profile 3 success")
        except:
            print("profile 3 has exist")
            print("removing...")
            shutil.rmtree(copy_guest_profile_path)

        print("recreate profile 3")
        shutil.copytree(guest_profile_path, copy_guest_profile_path)
        print("create profile 3 success")

    def Login(self, email):
        self.driver.get("https://twitter.com/")
        time.sleep(3)

        # while 1:
        #     pass

        # login with google
        elem = self.driver.find_element(By.CSS_SELECTOR, "div.S9gUrf-YoZ4jf")
        elem.click()
        time.sleep(3)

        # input email
        # switch to login window
        print("switching to login form")
        self.driver.switch_to.window(self.driver.window_handles[1])
        time.sleep(3)
        email_inp = ActionChains(self.driver)
        print("entering email")
        email_inp.send_keys(email).perform()
        time.sleep(1)
        email_inp.send_keys(Keys.ENTER).perform()
        time.sleep(3)
        print("entering pwd")
        email_inp.send_keys(_email_pwd).perform()
        time.sleep(1)
        email_inp.send_keys(Keys.ENTER).perform()
        # WriteEmailLogged(email)
        time.sleep(2)
        try:
            # click accept btn
            print("clicking accept btn")
            elem = self.driver.find_element(By.CSS_SELECTOR, "div#confirm_yes")
            elem.click()
        except:
            print("no accept btn")

        # switch back to main window
        print("switching to main window")
        self.driver.switch_to.window(self.driver.window_handles[0])
        time.sleep(5)

        # select month
        print('select month')
        Select(self.driver.find_element(By.ID, "SELECTOR_1")).select_by_value("8")

        # select day
        print('select day')
        Select(self.driver.find_element(By.ID, "SELECTOR_2")).select_by_value("15")

        # select year
        print('select year')
        Select(self.driver.find_element(By.ID, "SELECTOR_3")).select_by_value("2000")

        # submit
        time.sleep(1)
        print('submit')
        elem = self.driver.find_element(By.CSS_SELECTOR, "button[data-testid='ocfEnterDateNextLink']")
        elem.click()

        # redirect to community
        time.sleep(3)
        print('redirect to community')
        self.driver.get("https://x.com/i/communities/1506800881525829633")
        time.sleep(2)

        # check 'try it out' popups
        try:
            print('finding /try it out/ popups')
            elem = self.driver.find_elements(By.CSS_SELECTOR,
                                             "button.css-175oi2r.r-sdzlij.r-1phboty.r-rs99b7.r-lrvibr.r-1mnahxq.r-19yznuf.r-64el8z.r-1fkl15p.r-1loqt21.r-o7ynqc.r-6416eg.r-1ny4l3l")

            if 'Try it out' in elem[1].text:
                print('have Try it out popups')
                print('clicking /try it out/ popups')
                elem[1].click()

                if 'Check it out' in elem[0].text:
                    print('have popups')
                    print('clicking /Check it out/ popups')
                    elem[0].click()

        except:
            print('no /try it out/ popups')

        print('ok')

        while 1:
            pass

    def SetupAcc(self):
        pass

    def FllowPage(self):
        time.sleep(5)
        print("redirect to following page")
        self.driver.get("https://twitter.com/__XHotNews/following")
        time.sleep(3)
        print("selecting follow btn")
        elems = self.driver.find_elements(By.CSS_SELECTOR,
                                     "div.css-175oi2r.r-sdzlij.r-1phboty.r-rs99b7.r-lrvibr.r-15ysp7h.r-4wgw6l.r-ymttw5.r-1loqt21.r-o7ynqc.r-6416eg.r-1ny4l3l")
        for elm in elems:
            print("follow page")
            elm.click()
            time.sleep(3)

    def GetEmail(self):
        print('getting email')
        with open("email/mailTemp.txt", "r") as file:
            email = file.readline()
            print("email: " + email)
        return "phumbeyrka1a@amachadoespera.com"

    def WriteEmailLogged(email):
        # remove email used
        print("removing email")
        with open("email/mailTemp.txt", "r") as file:
            lines = file.readlines()
        with open("email/mailTemp.txt", "w") as file:
            for line in lines:
                if email not in line:
                    file.write(line)
                else:
                    print("removed email from mailTemp")

        # transfer them to logged file
        print("adding to logged_emil file")
        with open("email/logged_email.txt", "a") as file:
            file.write(email + '\n')


# def main():
#     # CopyGuestProfile()
#
#     # setup proxy
#     myProxy = "171.231.29.94:31516"
#     proxy = Proxy({
#         'proxyType': ProxyType.MANUAL,
#         'httpProxy': myProxy,
#         'sslProxy': myProxy,
#         'noProxy': ''})
#
#     options = webdriver.ChromeOptions()
#     options.proxy = proxy
#     options.add_argument(r"user-data-dir=chrome_profile/")
#     options.add_argument("profile-directory=Profile 3")
#
#     # set chrome as Headless
#     # options.add_argument("--headless=new")
#
#     driver = webdriver.Chrome(options=options)
#
#     Login(driver)

# if __name__ == "__main__":
#     # add options to chrome
#     options = webdriver.ChromeOptions()
#
#     # setup proxy
#     # myProxy = "171.231.29.94:31516"
#     # proxy = Proxy({
#     #     'proxyType': ProxyType.MANUAL,
#     #     'httpProxy': myProxy,
#     #     'sslProxy': myProxy,
#     #     'noProxy': ''})
#     # options.proxy = proxy
#
#     # add usr profile
#     # CopyGuestProfile()
#     # options.add_argument(r"user-data-dir=chrome_profile/")
#     # options.add_argument("profile-directory=Profile 3")
#
#     driver = webdriver.Chrome(options=options)
#
#     Login(driver)
