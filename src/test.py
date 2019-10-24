import os
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time

link = "https://playvidto.com/ti20z3lydqop"

options = Options()
options.headless = True
# driver = webdriver.Firefox(options=options)
driver = webdriver.Firefox()
driver.get(link)
time.sleep(9)
bu = driver.find_elements_by_class_name("vjs-big-play-button")
driver.execute_script("arguments[0].click();", bu[0])
vid = driver.find_elements_by_class_name("vjs-tech")
print(vid[0].get_attribute("src"))
print("---")
"""
time.sleep(0.5)
btns = driver.find_elements_by_class_name("btn-go")
dwn_but = btns[0]
print(btns[0].get_attribute("href"))
"""
driver.quit()