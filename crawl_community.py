import pickle
import time
import os
import pyperclip
import numpy as np
import copilot
import json
import asyncio
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import asyncio


class CrawlCommunity:

    def __init__(self, driver, name):
        self.driver = driver
        self.name = name

    def MakeAlert(self):
        duration = 1  # seconds
        freq = 440  # Hz
        os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))

    async def LoginWithCookie(self, cookie_path):
        print(f'Login with cookie - ({self.name})')
        self.driver.get("https://x.com/home")
        await asyncio.sleep(3)
        print(f"setting cookie - ({self.name})")
        cookies = pickle.load(open(f"{cookie_path}", "rb"))
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        await asyncio.sleep(1)
        print(f"setting cookie success -> redirect to the login page - ({self.name})")
        self.driver.get("https://x.com/home")
        await asyncio.sleep(3)

        if 'https://x.com/home' not in self.driver.current_url:
            raise ValueError(
                f'general exceptions not caught by specific handling - {self.name}, current url: {self.driver.current_url}')

    def Login(self, email, _email_pwd):
        self.driver.get("https://x.com/home")
        time.sleep(3)

        # login with google
        elem = self.driver.find_element(By.CSS_SELECTOR, "div.S9gUrf-YoZ4jf")
        elem.click()
        time.sleep(3)

        # input email
        # switch to login window
        print(f"switching to login form - ({self.name})")
        self.driver.switch_to.window(self.driver.window_handles[1])
        time.sleep(1)
        email_inp = ActionChains(self.driver)
        email = email
        print(f"entering email - ({self.name})")
        email_inp.send_keys(email).perform()
        time.sleep(1)
        email_inp.send_keys(Keys.ENTER).perform()
        time.sleep(3)
        print(f"entering pwd - ({self.name})")
        email_inp.send_keys(_email_pwd).perform()
        time.sleep(1)
        email_inp.send_keys(Keys.ENTER).perform()
        # WriteEmailLogged(email)
        time.sleep(2)
        try:
            # click accept btn
            print(f"clicking accept btn - ({self.name})")
            elem = self.driver.find_element(By.CSS_SELECTOR, "div#confirm_yes")
            elem.click()
        except:
            print(f"no accept btn - ({self.name})")

        # switch back to main window
        print(f"switching to main window - ({self.name})")
        self.driver.switch_to.window(self.driver.window_handles[0])
        time.sleep(5)

        # check access
        while 'https://x.com/account/access?' in self.driver.current_url:
            print(f'solve the captcha - ({self.name})')
            self.MakeAlert()
            time.sleep(3)

    # crawl list community
    def Crawl(self):
        print(f'directing to communities page - ({self.name})')
        self.driver.get("https://x.com/i/communities/suggested?q=crypto")
        time.sleep(5)

        # while 1:
        #     pass

        # create 2d arr
        list_community_arr = np.zeros((2, 2))

        # loop util get 1000 community
        while len(list_community_arr[0]) < 2000:
            # get list community
            print(f'getting list community - ({self.name})')
            list_community_css = (
                'html > body > div#react-root > div.css-175oi2r > div.css-175oi2r > div.css-175oi2r > '
                'main.css-175oi2r > div.css-175oi2r > div.css-175oi2r > div.css-175oi2r > div.css-175oi2r > '
                'div.css-175oi2r > div > div.css-175oi2r > a.css-175oi2r')
            elems = self.driver.find_elements(By.CSS_SELECTOR, list_community_css)

            for elem in elems:

                # scroll to last community
                print(f'scrolling to last community - ({self.name})')
                try:
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", elem)
                    time.sleep(1)
                except:
                    print(f"can't scroll to community - ({self.name})")
                    continue

                print(elem.text)

                # get link of community and member
                community_link = elem.get_attribute("href")

                # get number of member
                members_num = elem.text[elem.text.find('\n') + 1:elem.text.find('Member')]

                # preproc data
                if 'K' in members_num:
                    members_num = float(members_num[:members_num.find('K')]) * 1000

                members_num = int(members_num)

                print(f'community_link: {community_link}\nmembers_num - {members_num} - ({self.name})')

                # if link of community doesn't exist in arr
                if np.any(list_community_arr == community_link):
                    print(f'the community link has already exits - ({self.name})')
                else:
                    # add community to arr
                    print(f'adding community to arr - ({self.name})')
                    new_col = np.array([[community_link], [members_num]])
                    list_community_arr = np.hstack((list_community_arr, new_col))

                print(f'current number of community: {len(list_community_arr[0])} - ({self.name})')

                # write log file
                print(f'writing log - ({self.name})')
                with open('top_500_community.txt', 'w+') as file:
                    # get element by 'link - members' format
                    for col in range(len(list_community_arr[0])):
                        file.write(f"{list_community_arr[0][col]} - {list_community_arr[1][col]}\n")

        # sort arr
        print(f'sorting communities arr - ({self.name})')
        list_community_arr[1] = list_community_arr[1].astype(int)
        sorted_indices = np.argsort(list_community_arr[1])[::-1]
        sorted_list_community_arr = list_community_arr[:, sorted_indices]

        # write log file
        print(f'writing log - ({self.name})')
        with open('top_500_community.txt', 'w+') as file:
            # get element by 'link - members' format
            for col in range(len(sorted_list_community_arr[0])):
                file.write(f"{sorted_list_community_arr[0][col]} - {sorted_list_community_arr[1][col]}\n")

    async def Comment(self, comment_link, community_link, _ad_link_comment, _input_tweet):

        # open community link
        self.driver.get(community_link)
        await asyncio.sleep(3)
        print(f'start commenting - ({self.name})')

        # check 'try it out' popups
        try:
            print(f'finding /try it out/ popups - ({self.name})')
            elem = self.driver.find_elements(By.CSS_SELECTOR,
                                             "button.css-175oi2r.r-sdzlij.r-1phboty.r-rs99b7.r-lrvibr.r-1mnahxq.r-19yznuf.r-64el8z.r-1fkl15p.r-1loqt21.r-o7ynqc.r-6416eg.r-1ny4l3l")

            if 'Try it out' in elem[1].text:
                print(f'have Try it out popups - ({self.name})')
                print(f'clicking /try it out/ popups - ({self.name})')
                elem[1].click()
                await asyncio.sleep(1)

                if 'Check it out' in elem[0].text:
                    print(f'have popups - ({self.name})')
                    print(f'clicking /Check it out/ popups - ({self.name})')
                    elem[0].click()
                    await asyncio.sleep(1)

        except:
            print(f'no /try it out/ popups - ({self.name})')

        # check join community
        try:
            print(f'check join community - ({self.name})')
            elem = self.driver.find_element(By.CSS_SELECTOR,
                                            "button.css-175oi2r.r-sdzlij.r-1phboty.r-rs99b7.r-lrvibr.r-2yi16.r-1qi8awa.r-3pj75a.r-1loqt21.r-o7ynqc.r-6416eg.r-1ny4l3l")
            if 'Join' == elem.text:
                print(f'joining community - ({self.name})')
                elem.click()
                await asyncio.sleep(2)

                # clicking popups
                elem = self.driver.find_element(By.CSS_SELECTOR,
                                                "button.css-175oi2r.r-sdzlij.r-1phboty.r-rs99b7.r-lrvibr.r-15ysp7h.r-4wgw6l.r-3pj75a.r-1loqt21.r-o7ynqc.r-6416eg.r-1ny4l3l")
                elem.click()

        except:
            print(f'joined - ({self.name})')

        await asyncio.sleep(2)

        # # open comment tab
        # print('opening new tab')
        # self.driver.execute_script("window.open('');")
        #
        # # switch to new tab
        # print('switching to new tab')
        # self.driver.switch_to.window(self.driver.window_handles[1])

        # direct to comment link
        print(f'redirecting to comment link - ({self.name})')
        self.driver.get(comment_link)
        await asyncio.sleep(5)

        # check popups
        # try:
        #     elem = self.driver.find_element()

        # click on comment icon
        print(f'click on comment icon - ({self.name})')
        elems = self.driver.find_elements(By.CSS_SELECTOR,
                                          "button.css-175oi2r.r-1777fci.r-bt1l66.r-bztko3.r-lrvibr.r-1loqt21.r-1ny4l3l")
        elems[1].click()

        await asyncio.sleep(2)
        # if have popups
        try:
            print(f'finding popups - ({self.name})')
            self.driver.find_elements(By.CSS_SELECTOR,
                                      "div.css-175oi2r.r-kemksi.r-16y2uox.r-1dqxon3.r-16wqof.r-11nfnuw")
            print(f'have popups - ({self.name})')
            elem = self.driver.find_elements(By.CSS_SELECTOR,
                                             "button.css-175oi2r.r-sdzlij.r-1phboty.r-rs99b7.r-lrvibr.r-1mnahxq.r-19yznuf.r-64el8z.r-1fkl15p.r-1loqt21.r-o7ynqc.r-6416eg.r-1ny4l3l")
            print(f'clicking popups - ({self.name})')
        except:
            print(f'no popups - ({self.name})')

        await asyncio.sleep(1)
        print(f'finding input - ({self.name})')
        comment_input = self.driver.find_element(By.CSS_SELECTOR, _input_tweet)
        await asyncio.sleep(2)
        print(f'commenting - ({self.name})')
        comment_input.send_keys(_ad_link_comment)

        # use shortcut to submit
        print(f"sending key stroke to submit - ({self.name})")
        comment_input.send_keys(Keys.CONTROL + Keys.ENTER)
        await asyncio.sleep(3)

        # # close new post tab
        # self.driver.close()
        # print("new tab closed")
        #
        # # switch self.driver to main tab
        # print("switch to main tab")
        # self.driver.switch_to.window(self.driver.window_handles[0])

        print(f'commenting finished - ({self.name})')

    def CrawlMostViewComment(self, community_link, number_of_comment_link):

        self.driver.get(community_link)
        time.sleep(5)

        print(f"start crawling comment - ({self.name})")

        # create arr
        post_arr = []

        # loop util get 20 post
        while len(post_arr) < number_of_comment_link:
            # get list community
            print(f'getting list post - ({self.name})')
            comment_css = ('div.css-175oi2r.r-1iusvr4.r-16y2uox.r-1777fci.r-kzbkwu')
            elems = self.driver.find_elements(By.CSS_SELECTOR, comment_css)

            for elem in elems:

                # scroll to current comment
                print(f'scrolling to current post - ({self.name})')
                try:
                    if elem is elems[len(elems) - 1]:
                        print(f'sroll to end page - ({self.name})')
                        ActionChains(self.driver).send_keys(Keys.END).perform()

                    self.driver.execute_script("arguments[0].scrollIntoView(true);", elem)
                    time.sleep(1)
                except:
                    print(f"can't scroll to post - ({self.name})")
                    continue

                # get number of view
                try:
                    print(f'try getting link of post - ({self.name})')
                    text = self.driver.execute_script(
                        "elm = arguments[0].lastElementChild.childNodes[0].childNodes[0].childNodes[3].lastChild;"
                        "return String(elm.getAttribute('aria-label')) + ' - ' + String(elm.getAttribute('href'));"
                        , elem)
                    print(text + f' - ({self.name})')
                except:
                    print(f'cannot get link of post - ({self.name})')
                    continue

                # extract the link from text
                post_link = 'https://x.com' + text[text.find('/'):-9]

                # check if the link has existed in arr
                if post_arr.count(post_link) != 0:
                    print(f"the link has already existed - ({self.name})")
                    continue

                if len(post_arr) > number_of_comment_link:
                    break

                print(f"adding link to arr - ({self.name})")
                post_arr.append(post_link)
                print(f'post arr size: {len(post_arr)} - ({self.name})')

        print(f"crawling finished - ({self.name})")
        return post_arr

    # def main(email):
    #     driver = webdriver.Chrome()
    #     Login(email)
    #
    #     driver.get('https://x.com/i/communities/1506800881525829633')
    #
    #     while 1:
    #         pass
    #
    #     Comment('https://x.com/FluentInFinance/status/1687135672757272576',
    #             'https://x.com/i/communities/1508567430188126209')
    # CrawlMostViewComment(driver)

    # if __name__ == "__main__":
    #     # driver = webdriver.Chrome()
    #
    #     # use for copilot.py
    #     # driver_2 = webdriver.Chrome()
    #     main('lcurlis9ha1a@amachadoespera.com')
    #     # asyncio.run(test(driver))
    #     # Scroll(driver)
    #     while 1:
    #         pass
