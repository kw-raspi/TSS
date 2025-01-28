from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

def get_page_title(url: str, driver_path: str) -> str:
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)
    
    try:
        driver.get(url)
        return driver.title
    finally:
        driver.quit()

driver_path = "/usr/bin/chromedriver"
url = "https://blog.naver.com/ranto28"
title = get_page_title(url, driver_path)
print(title)


