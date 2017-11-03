import os
import unittest
import time
import sys
import re
import datetime
from HtmlTestRunner import HTMLTestRunner
from selenium import webdriver
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
#----------------------------------------------------------------------------
# I have to say that this program is not for "snatch" and compete your speed,
# but to run a program smoothly.
# Therefore, if you want to use this program to "snatch red envelops",
# Please change some values of function time.sleep().
# Enjoy it!
# Su Yiran, SYSU
#----------------------------------------------------------------------------
# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


desired_caps = {}
desired_caps['reportDirectory'] = 'reports'
desired_caps['reportFormat'] = 'xml'
desired_caps['"fastReset"'] = False
desired_caps['fullReset'] = False
desired_caps['noReset'] = True
desired_caps['platformName'] = 'Android'
desired_caps['deviceName'] = 'KYV7N15C14000510'
desired_caps['appPackage'] = 'com.tencent.mm'
desired_caps['appActivity'] = '.ui.LauncherUI'
desired_caps['noSign'] = True
desired_caps["unicodeKeyboard"] = True
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
window_size = driver.get_window_size()
width = window_size.get("width")
height = window_size.get("height")
main_page_swipe = False
time.sleep(5)
while True:
    try:
        driver.find_element_by_android_uiautomator('new UiSelector().textContains("[微信红包]")').click()
    except:
        #downward
        if main_page_swipe == False:
            driver.swipe(width/2,height*3/4,width/2,height/4,650)
            main_page_swipe = True
            time.sleep(0.3)
        #upward
        elif main_page_swipe == True:
            driver.swipe(width/2,height/4,width/2,height*3/4,450)
            main_page_swipe = False
            time.sleep(0.3)
    else:
        message_page_swipe = False
        still_need_to_check_message_page = True
        while still_need_to_check_message_page == True:
            time.sleep(1.5)
            try:
                #still need to check again if there are any red envelopes missed. 
                driver.find_element_by_android_uiautomator('new UiSelector().textContains("领取红包")').click()
            except:
                if message_page_swipe == False:
                    driver.swipe(width/2,height/4,width/2,height*3/4,750)
                    message_page_swipe = True
                    time.sleep(0.2)
                elif message_page_swipe == True:
                    still_need_to_check_message_page = False
            else:
                time.sleep(5.75)
                #open a red envelope.
                driver.tap([((width * (715/1440)), (height * (1448/2560)))],1)
                time.sleep(1.5)
                #judge if enter the snatching red envelope already.
                try:
                    driver.find_element_by_id('tj')
                #if not rounding, which means OK.
                except:
                    time.sleep(12.5)
                    #judge if still openning the envelope.
                    try:
                        driver.find_element_by_id('iy')
                    #OK, no exception actually
                    except:
                        #if successfully open the red envelope.                    
                        #exit red envelope. 
                        driver.press_keycode(4)
                        time.sleep(0.75)
                        #automatic reply. 
                        desired_caps["unicodeKeyboard"] = True
                        time.sleep(0.3)
                        if_thanks_boss = False
                        while if_thanks_boss == False:
                            try:
                                driver.find_element_by_id('a71').send_keys('谢谢老板！')
                            except:
                                continue
                            else:
                                if_thanks_boss = True
                                driver.find_element_by_id('a77').click()
                                #TODO: emoji reply
                                #driver.find_element_by_id('a73').click()
                                #time.sleep(1)
                                #driver.tap([(735, 2330)], 1)
                                #time.sleep(0.5)
                                #driver.swipe(75, 1884, 1000, 1884, 800)
                                #time.sleep(1)
                                #driver.tap([(540, 1624)],1)
                                #time.sleep(0.2)
                                #driver.tap([(540, 1624)],1)
                                #time.sleep(0.2)
                                #driver.tap([(540, 1624)],1)
                                #exit emoji
                                #driver.press_keycode(4)
                                time.sleep(0.75)
                            finally:
                                print('finish thanks_boss')
                    #FAILED, something went wrong. 
                    else:
                        still_need_to_check_message_page = False
                    finally:
                        print('finish find_message')
                #if rounding, which means FAILED.
                else:
                    still_need_to_check_message_page = False
                    #waiting to exit wating page
                    driver.press_keycode(4)
                    #I've found a very interesting phenomenon.
                    #If you click on the round, it will end sooner.
                    time.sleep(0.5)
                finally:
                    print('finish find_rounding')
            finally:
                print('finish find_red_envelope_in_message_page')
        #exit message page
        driver.press_keycode(4)
        time.sleep(0.75)
        #return top of main page
        driver.swipe(width/2,height/4,width/2,height*3/4,650)
        time.sleep(0.5)
    finally:
        print('finish_find_red_envelope_in_main_page')
driver.quit()