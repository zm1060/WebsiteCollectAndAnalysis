import os
import time

from urllib.parse import urlparse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def process_url(url):
    parsed_url = urlparse(url)
    domains = parsed_url.netloc
    if not domains:
        return
    return domains


def process_domain(domain):
    # Add "http://" to domain names that don't have it
    if not domain.startswith("http"):
        domain = "http://" + domain

    # Parse the URL and extract the base domain
    parsed_url = urlparse(domain)
    base_url = parsed_url.scheme + "://" + parsed_url.netloc
    if not parsed_url.scheme or not parsed_url.netloc:
        return
    return base_url


def check_beian_info(url):

    domain = process_url(url)
    if domain:
        filename = f"../xdns/response/{process_url(url)}.txt"
    else:
        return
    if os.path.isfile(filename):
        print(f"File already exists: {filename}")
        return

    options = webdriver.ChromeOptions()
    options.add_argument("--enable-javascript")
    driver = webdriver.Chrome(options=options)
    try:
        # 加载网站
        driver.get(url)
        driver.execute_script()
        # Wait for the dynamic content to load (using an explicit wait)
        wait = WebDriverWait(driver, 10)  # Maximum wait time of 10 seconds
        dynamic_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#dynamic-element")))

        time.sleep(5)
        # 获取整个页面的源代码
        page_source = driver.page_source

        with open(filename, "w", encoding="utf-8") as file:
            file.write(page_source)
        print(f"Response stored: {filename}")
    except Exception:
        print(f"Some errors!")
        with open("../xdns/rfailed_domains.txt", "a", encoding="utf-8") as file:
            file.write("\n".join(domain))
    finally:
        # 关闭WebDriver
        driver.quit()


with open('../xdns/failed_domains.txt', 'r', encoding='utf-8') as file:
    urls = file.readlines()

for url in urls:
    url = url.strip()  # Remove leading/trailing whitespace and newlines
    print(url)
    url = process_domain(url)
    # url = 'http://www.jp.hh.gov.cn'
    check_beian_info(url)
