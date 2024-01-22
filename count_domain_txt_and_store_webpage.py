import os
import json
import time

import requests

from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor

import ssl
import urllib3
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# 关闭https证书验证
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE
# 关闭http不安全警告
urllib3.disable_warnings()

active_url_count = {}
dead_url_count = {}
province_count = {}
results = {}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Connection': 'keep-alive',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'sec-ch-ua-platform': 'windows'

}
chrome_options = webdriver.ChromeOptions()

chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-infobars')
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"')
# chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)


def process_response(province, url, response, status):
    result_entry = {"domain": url, "status": status, "source": "requests"}
    results[province]["domains"].append(result_entry)
    response_info = {
        "is_redirect": response.is_redirect,
        "is_permanent_redirect": response.is_permanent_redirect,
        "elapsed_time": response.elapsed.total_seconds()
    }
    results[province]["domains"][-1]["response_info"] = response_info


def process_url(url, protocol, province):
    original_url = url
    try:
        response = requests.get(url, headers=headers, timeout=20, verify=False, allow_redirects=True)
        response.encoding = "utf-8"

        print(f"{url}: {protocol} Status Code - {response.status_code}")

        if province not in results:
            results[province] = {"province_name": province, "domains": []}

        if response.status_code == 200:
            province_count[province] += 1
            active_url_count[province] += 1

            save_html_content(province, url, response.text)
            process_response(province, url, response, "active")
            return
        else:
            # if url.startswith("http://"):
            #     url = url.replace("http://", "https://")
            # if url.startswith("https://"):
            #     url = url.replace("https://", "http://")
            # 使用原始url再请求一次
            # Use a context manager to ensure the driver is properly closed
            file_size = 0
            with webdriver.Chrome(options=chrome_options) as driver:
                try:
                    # Load the website
                    driver.get(url)
                    driver.implicitly_wait(3)
                    driver.get(url)
                    driver.implicitly_wait(3)

                    # Check if there was a redirect
                    is_redirect = driver.current_url != url

                    webpage = driver.page_source

                    file_size = save_html_content(province, url, webpage)
                    if file_size < 10240:  # 10KB = 10 * 1024 bytes
                        raise ValueError('Too Small')
                    province_count[province] += 1
                    active_url_count[province] += 1
                    result_entry = {"domain": url, "status": "active", "source": "selenium"}
                    results[province]["domains"].append(result_entry)

                    # Include response properties in the JSON output
                    response_info = {
                        "is_redirect": is_redirect,
                        "is_permanent_redirect": False,  # Selenium doesn't provide this directly
                        "elapsed_time": 0  # Selenium doesn't provide this directly
                    }
                    results[province]["domains"][-1]["response_info"] = response_info
                    return
                except Exception as e:
                    if url.startswith("http://") and not file_size < 10240:
                        url = url.replace("http://", "https://")
                    if url.startswith("https://") and not file_size < 1040:
                        url = url.replace("https://", "http://")
                    # # Use a context manager to ensure the driver is properly closed
                    with webdriver.Chrome(options=chrome_options) as driver:
                        try:
                            # Load the website
                            driver.get(url)
                            driver.implicitly_wait(3)
                            driver.get(url)
                            driver.implicitly_wait(3)

                            # Check if there was a redirect
                            is_redirect = url not in driver.current_url

                            if is_redirect:
                                print(f"{url}: Redirected to {driver.current_url}")

                            webpage = driver.page_source
                            province_count[province] += 1
                            active_url_count[province] += 1

                            save_html_content(province, url, webpage)
                            result_entry = {"domain": urlparse(url).netloc, "status": "active", "source": "selenium", "success_url": url}
                            results[province]["domains"].append(result_entry)
                            # Include response properties in the JSON output
                            response_info = {
                                "is_redirect": is_redirect,
                                "is_permanent_redirect": False,  # Selenium doesn't provide this directly
                                "elapsed_ime": 0  # Selenium doesn't provide this directly
                            }
                            results[province]["domains"][-1]["response_info"] = response_info
                            return
                        except Exception as e:
                            province_count[province] += 1
                            dead_url_count[province] += 1
                            result_entry = {"domain": urlparse(url).netloc, "status": "dead", "source": "selenium"}
                            results[province]["domains"].append(result_entry)
            # try:
            #
            #     response = requests.get(url, headers=headers, timeout=10, verify=False, allow_redirects=True)
            #     response.encoding = "utf-8"
            #     print(f"{url}: https Status Code - {response.status_code}")
            #     if response.status_code == 200:
            #         province_count[province] += 1
            #         active_url_count[province] += 1
            #         save_html_content(province, url, response.text)
            #         process_response(province, url, response, "active")
            #         return
            #     else:
            #         province_count[province] += 1
            #         dead_url_count[province] += 1
            #         process_response(province, url, response, response.status_code)
            #         return
            #
            # except Exception as e:
            #     # Use a context manager to ensure the driver is properly closed
            #     with webdriver.Chrome(options=chrome_options) as driver:
            #         try:
            #             # Load the website
            #             driver.get(url)
            #             time.sleep(3)
            #             # Check if there was a redirect
            #             is_redirect = driver.current_url != url
            #
            #             webpage = driver.page_source
            #             province_count[province] += 1
            #             active_url_count[province] += 1
            #             save_html_content(province, url, webpage)
            #             result_entry = {"domain": url, "status": "active", "source": "selenium"}
            #             results[province]["domains"].append(result_entry)
            #
            #             # Include response properties in the JSON output
            #             response_info = {
            #                 "is_redirect": is_redirect,
            #                 "is_permanent_redirect": False,  # Selenium doesn't provide this directly
            #                 "elapsed_time": 0  # Selenium doesn't provide this directly
            #             }
            #             results[province]["domains"][-1]["response_info"] = response_info
            #             return
            #         except Exception as e:
            #             province_count[province] += 1
            #             dead_url_count[province] += 1
            #             result_entry = {"domain": url, "status": "dead", "source": "selenium"}
            #             results[province]["domains"].append(result_entry)
    except Exception as e:
        # # Use a context manager to ensure the driver is properly closed
        with webdriver.Chrome(options=chrome_options) as driver:
            try:
                # Load the website
                driver.get(url)
                driver.implicitly_wait(3)
                driver.get(url)
                driver.implicitly_wait(3)

                # Check if there was a redirect
                is_redirect = url not in driver.current_url

                if is_redirect:
                    print(f"{url}: Redirected to {driver.current_url}")


                webpage = driver.page_source
                province_count[province] += 1
                active_url_count[province] += 1

                save_html_content(province, url, webpage)
                result_entry = {"domain": urlparse(url).netloc, "status": "active", "source": "selenium", "success_url": url}
                results[province]["domains"].append(result_entry)
                # Include response properties in the JSON output
                response_info = {
                    "is_redirect": is_redirect,
                    "is_permanent_redirect": False,  # Selenium doesn't provide this directly
                    "elapsed_ime": 0  # Selenium doesn't provide this directly
                }
                results[province]["domains"][-1]["response_info"] = response_info
                return
            except Exception as e:
                province_count[province] += 1
                dead_url_count[province] += 1
                result_entry = {"domain": urlparse(url).netloc, "status": "dead", "source": "selenium"}
                results[province]["domains"].append(result_entry)

        #
        # try:
        #
        #     again_response = requests.get(url, headers=headers, timeout=20, verify=False,
        #                                   allow_redirects=True)
        #     again_response.encoding = "utf-8"
        #
        #     print(f"{url}: https Status Code - {again_response.status_code}")
        #
        #     if province not in results:
        #         results[province] = {"province_name": province, "domains": []}
        #
        #     if again_response.status_code == 200 and 'Content-Type' in again_response.headers and 'text' in \
        #             again_response.headers[
        #                 'Content-Type']:
        #         province_count[province] += 1
        #         save_html_content(province, url, again_response.text)
        #         result_entry = {"domain": url, "status": "active"}
        #         results[province]["domains"].append(result_entry)
        #         active_url_count[province] += 1
        #     else:
        #         province_count[province] += 1
        #         result_entry = {"domain": url, "status": again_response.status_code, }
        #         results[province]["domains"].append(result_entry)
        #         dead_url_count[province] += 1
        #
        #     # Include response properties in the JSON output
        #     response_info = {
        #         "is_redirect": again_response.is_redirect,
        #         "is_permanent_redirect": again_response.is_permanent_redirect,
        #         "elapsed_time": again_response.elapsed.total_seconds()
        #     }
        #     results[province]["domains"][-1]["response_info"] = response_info
        # except Exception as e:
        #     province_count[province] += 1
        #     print(f"{url}: https Status Code - Error: {e}")
        #     result_entry = {"domain": url, "status": "dead"}
        #     results[province]["domains"].append(result_entry)
        #     dead_url_count[province] += 1


def save_html_content(province, url, content):
    province_dir = f"new_response/{province}"
    os.makedirs(province_dir, exist_ok=True)

    u = urlparse(url)
    domain_path = u.netloc
    file_name = f"{domain_path}.html"
    file_path = os.path.join(province_dir, file_name)

    # Convert content from the original encoding to UTF-8
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

    # Get the size of the written file
    file_size = os.path.getsize(file_path)

    return file_size


def process_line(line, province):
    line = line.strip()
    u = urlparse(line)

    domain = u.netloc

    if u.scheme == "https":
        https_url = f"https://{domain}"
        process_url(https_url, "https", province)
    else:
        http_url = f"http://{domain}"
        process_url(http_url, "http", province)


def process_file(file_name, province):
    file_path = f"domain_txt/{file_name}"

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        active_url_count[province] = 0
        dead_url_count[province] = 0
        province_count[province] = 0

        with ThreadPoolExecutor(max_workers=20) as executor:
            executor.map(lambda line: process_line(line, province), lines)

    except Exception as e:
        print(f"Error processing file {file_name}: {e}")


if __name__ == "__main__":
    dir_entries = os.listdir("domain_txt")

    for entry in dir_entries:
        if not entry.endswith(".txt"):
            continue
        province = entry.split(".txt")[0]

        # Check if JSON file already exists for the province
        json_filename = f"{province}_results.json"
        if os.path.exists(json_filename):
            print(f"JSON file already exists for {province}. Skipping...")
            continue

        print(province)
        process_file(entry, province)

        # Store results in a JSON file for each province
        output_province = {
            "active_url_count": active_url_count[province],
            "dead_url_count": dead_url_count[province],
            "total_url_count": active_url_count[province] + dead_url_count[province],
            "domains": results[province]["domains"]
        }

        with open(json_filename, 'w', encoding='utf-8') as json_file:
            json.dump(output_province, json_file, indent=4)

    print(f"Results written to {json_filename}")
