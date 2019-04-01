# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from  selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

data = requests.get('https://www.channelcrawler.com/eng/results/390306')
soup = BeautifulSoup(data.content)
divs = soup.find_all('div', {'class': 'row'})
links = divs[1].find_all('a', {'target': '_blank'})
links = list(set(links))
profiles = []
for link in links:
    profiles.append(link['href'])
for profile in profiles:
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--test-type")
    options.binary_location = "/usr/bin/chromium-browser"
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(profile + '/about')

    email_button = driver.find_element_by_css_selector('#details-container > table > tbody > tr:nth-child(1) > td:nth-child(2) > ytd-button-renderer > a')
    email_button.click()

    # captcha_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#recaptcha-anchor > div.recaptcha-checkbox-checkmark")))

    # time.sleep(1)

    captcha_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#captcha-container > form > div")))
    captcha_button.click()


    time.sleep(1)
    submit_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#captcha-container > form > button")))
    submit_button.click()
    break


