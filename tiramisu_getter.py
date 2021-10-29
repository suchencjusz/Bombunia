import json
import time
from selenium import webdriver

def catch():
    with open('config.json') as f: 
        config = json.load(f)
        f.close()

    driver = webdriver.Firefox()
    # driver.set_window_size(1120, 550)

    driver.set_page_load_timeout(30)
    driver.get(config['school_url'])

    driver.find_element_by_class_name('loginButton').click()

    element = driver.find_element_by_name("LoginName")
    element.send_keys(config['email'])
    element = driver.find_element_by_name("Password")
    element.send_keys(config['password'])
    element.send_keys(u'\ue007')

    time.sleep(7)

    button = driver.find_element_by_xpath("/html[1]/body[1]/div[1]/main[1]/div[2]/div[3]/div[1]/a[1]/div[1]/div[1]/div[2]")
    button.click()

    time.sleep(7)

    button = driver.find_element_by_xpath("/html[1]/body[1]/div[2]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[8]/button[1]")
    button.click()

    time.sleep(7)

    cookies = driver.get_cookies()

    flush()
    
    with open("cookies.json", "w") as f: 
        json.dump(cookies,f)
        f.close()

    driver.close()

def flush():
    with open("cookies.json", "w") as f: f.flush