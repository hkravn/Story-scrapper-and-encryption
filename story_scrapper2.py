from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from cryptography.fernet import Fernet
import time
import re
import random

file = open('key.key', 'rb')
key = file.read()
file.close()

Options = Options()
Options.headless = True

def story_name(s1):
    fern = Fernet(key)
    encrypted = fern.encrypt(s1)
    return encrypted


def update_story_file(url, prox):
    
    webdriver.DesiredCapabilities.FIREFOX['proxy']={
    "httpProxy":prox,
    "ftpProxy":prox,
    "sslProxy":prox,
    "proxyType":"MANUAL",
    }
    
    p = 1
    current_url = []
    browser = webdriver.Firefox(options=Options)
    story = ""
    try:
        browser.get(url)
    except WebDriverException as err:
        print(err)
        return False
    
    WebDriverWait(browser, 5)
    try:
        head = browser.find_element_by_class_name('b-story-header').text.partition("by")[0]
    except NoSuchElementException as err:
        print(err)
        return False
    
    pages = browser.find_element_by_class_name('b-pager-pages').text[0]
    while p <= int(pages):
        current_url.append(url + "?page=" + str(p))
        browser.get(current_url[p-1])
        try:
            temp = browser.find_element_by_class_name('b-story-body-x').text
        except NoSuchElementException as err:
            print(err)
            return False
        
        story = story + "\n" + temp
        p = p + 1

    head = head.partition("\n")[0]
    head = re.sub(r"[^a-zA-Z0-9 ]", "",  head)
    saveas = open("stories\\%s.txt" % head, "w+", encoding='utf-8')
    saveas.write(f"{head} \n")
    for i in story:
        saveas.write(str(i))
    saveas.close()
    browser.quit()
    print("Done!")
    return True


def update_info(url):
    time.sleep(random.randint(1, 15))
    print(url)
    return True
