import asyncio
import threading
import time

from x_functions import X_Functions
from selenium.webdriver import ActionChains, Keys
from selenium import webdriver

_ad_link_comment = "Looking for lucrative investment opportunities? Don't miss out! Simply click the link below, and we'll both receive 5 Doge coins if it's your first time signing up. Don't hesitate, this is your chance! https://reemebal.com/4/7335440"
_ad_link_comment = "📷📷HAMSTER KOMBAT is a very interesting event. It's truly a case of getting something for nothing."
"📷Those of you who don't know how to open and start working now: https://reemebal.com/4/7335440"
"📷Register to receive 5k coins immediately"
"📷$HAMTER KOMBAT is world cooperated"
_input_tweet = "div.public-DraftStyleDefault-block.public-DraftStyleDefault-ltr"


# def between_callback(email):
#
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     loop.run_until_complete(join_community_x.main(email))
#     loop.close()

async def MultiComment(cookie_path, community_link, comment_link, _ad_link_comment, _input_tweet, name):
    driver_comment_acc = webdriver.Chrome()

    comment_acc = X_Functions.Login(driver=driver_comment_acc, name=name)

    await comment_acc.LoginWithCookie(cookie_path=cookie_path)

    await comment_acc.Comment(comment_link=comment_link, community_link=community_link,
                              _ad_link_comment=_ad_link_comment,
                              _input_tweet=_input_tweet)

    # close driver after finish
    driver_comment_acc.quit()


async def main(comment_link_list, community_link, len):
    await asyncio.gather(
        *[MultiComment(f'cookies/comment_acc_{i}.pkl', community_link, comment_link_list[i], _ad_link_comment,
                       _input_tweet, f'acc_{i}') for i in range(len)]
    )


if __name__ == "__main__":
    driver = webdriver.Chrome()
    main_acc = X_Functions(driver, 'main')
    main_acc.Login('lcurlis9ha1a@amachadoespera.com')
    # post_list = main_acc.GetComment(number_of_comment=3, link='https://x.com/UyenNhi3x')
    main_acc.CommentWithImage(comment_link='https://x.com/wilfong255kv/status/1807253256764317810/', _input_tweet=_input_tweet, text='adfdsaf', img_path='asdf')
    main_acc.GetCommentLink(usr_name='LulitaC36489')
    while 1:
        pass

    # asyncio.run(craw_acc.LoginWithCookie('cookies/wraisbeckbja1a@amachadoespera_WRaisbeck53282.pkl'))
    #
    # while 1:
    #     pass
    # community_link = 'https://x.com/cogiaomoon69'
    # comment_link_list = craw_acc.CrawlMostViewComment(community_link=community_link, number_of_comment_link=20)
    #
    # with open('link_list/co_giao_lon_ton.txt', 'w') as file:
    #     for link in comment_link_list:
    #         file.writelines(link+'\n')

    # i = 0
    # print('starting async')
    # while i < len(comment_link_list):
    #     asyncio.run(main(community_link=community_link, comment_link_list=comment_link_list, len=i))
    #     i += 5
    #
    # while 1:
    #     pass

    # community_list = craw_acc.CrawlMostViewComment('https://x.com/i/communities/1506800881525829633')
    # print(community_list)

    # p1 = threading.Thread(target=between_callback, args=('jemanuele99a1a@amachadoespera.com',))
    # p1.start()

    # p2 = threading.Thread(target=between_callback, args=(cookie_path_2,))
    # p2.start()
    #
    # p3 = threading.Thread(target=between_callback, args=(cookie_path_3,))
    # p3.start()
    #
    # p4 = threading.Thread(target=between_callback, args=(cookie_path_4,))
    # p4.start()
