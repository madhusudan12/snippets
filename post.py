# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from  selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def get_clear_browsing_button(driver):
    """Find the "CLEAR BROWSING BUTTON" on the Chrome settings page."""
    return driver.find_element_by_css_selector('* /deep/ #clearBrowsingDataConfirm')


def clear_cache(driver, timeout=60):
    """Clear the cookies and cache for the ChromeDriver instance."""
    # navigate to the settings page
    driver.get('chrome://settings/clearBrowserData')

    # wait for the button to appear
    wait = WebDriverWait(driver, timeout)
    wait.until(get_clear_browsing_button)

    # click the button to clear the cache
    get_clear_browsing_button(driver).click()

    # wait for the button to be gone before returning
    wait.until_not(get_clear_browsing_button)



profile = 'https://www.youtube.com/channel/UC_K7yepQXxO-83DpAc1gZlg'
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")
options.add_argument('disable-infobars')
options.binary_location = "/usr/bin/chromium-browser"
driver = webdriver.Chrome(chrome_options=options)
driver.get(profile + '/about')
driver.delete_all_cookies()
#clear_cache(driver)

time.sleep(5)
email_button = driver.find_element_by_css_selector \
    ('#details-container > table > tbody > tr:nth-child(1) > td:nth-child(2) > ytd-button-renderer > a')
email_button.click()

time.sleep(5)
captcha_button = WebDriverWait(driver, 10).until \
    (EC.presence_of_element_located((By.CSS_SELECTOR, "#captcha-container > form > div")))
captcha_button.click()


time.sleep(1)
submit_button = WebDriverWait(driver, 10).until \
    (EC.presence_of_element_located((By.CSS_SELECTOR ,"#captcha-container > form > button")))
submit_button.click()


