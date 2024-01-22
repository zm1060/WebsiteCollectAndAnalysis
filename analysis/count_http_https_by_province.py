import json
import requests
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import time

http_count = 0
https_count = 0
results = []


def process_url(url):
    global http_count, https_count, results

    def make_request(scheme):
        global http_count, https_count, results

        try:
            parsed_url = urlparse(url)
            modified_url = scheme + '://' + parsed_url.netloc + parsed_url.path
            response = requests.get(modified_url, timeout=10, headers=headers, allow_redirects=True,
                                    stream=True)
            status_code = response.status_code
            print(f"{url}: {scheme.upper()} Status Code - {status_code}")

            result_entry = {
                'url': url,
                f'{scheme}_support': status_code == 200,
                'error': None if status_code == 200 else str(status_code)
            }

            results.append(result_entry)

            if status_code == 200:
                if scheme == 'http':
                    http_count += 1
                elif scheme == 'https':
                    https_count += 1

        except requests.exceptions.RequestException as e:
            print(f"Warning processing {url} ({scheme}): {e}")
            result_entry = {
                'url': url,
                f'{scheme}_support': False,
                'error': str(e)
            }
            results.append(result_entry)
        except Exception as e:
            print(f"Warning processing {url} ({scheme}): {e}")
            result_entry = {
                'url': url,
                f'{scheme}_support': False,
                'error': str(e)
            }
            results.append(result_entry)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Referer': 'https://www.baidu.com/'
    }

    make_request('http')
    make_request('https')


def main():
    global http_count, https_count, results

    # with ThreadPoolExecutor() as executor, tqdm(
    #         total=len(open('../temp.txt', 'r', encoding='utf-8').readlines())) as pbar:
    #     with open('../temp.txt', 'r', encoding='utf-8') as file:
    #         for line in file:
    #             executor.submit(process_url, line.strip())
    #             pbar.update(1)
    #             time.sleep(0.1)
    # with open('./http_https_other_results.json', 'w', encoding='utf-8') as json_file:
    #     json.dump(results, json_file, ensure_ascii=False, indent=2)
    with ThreadPoolExecutor() as executor, tqdm(
            total=len(open('../total.txt', 'r', encoding='utf-8').readlines())) as pbar:
        with open('../total.txt', 'r', encoding='utf-8') as file:
            for line in file:
                url = line.strip()
                if not url.startswith("http"):
                    url = f"http://{url}"
                executor.submit(process_url, url)
                pbar.update(1)
                time.sleep(0.1)
    with open('./http_https_results.json', 'w', encoding='utf-8') as json_file:
        json.dump(results, json_file, ensure_ascii=False, indent=2)

    print(f"Total HTTP-supported URLs: {http_count}")
    print(f"Total HTTPS-supported URLs: {https_count}")


if __name__ == "__main__":
    main()
# import csv
# import json
# import time
# from concurrent.futures import ThreadPoolExecutor
# from tqdm import tqdm
# from selenium import webdriver
# from selenium.common.exceptions import WebDriverException
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from urllib.parse import urlparse
#
#
# def process_url(url, browser):
#     global http_count, https_count, results
#
#     try:
#         parsed_url = urlparse(url)
#         modified_url = parsed_url.scheme + '://' + parsed_url.netloc + parsed_url.path
#
#         browser.get(modified_url)
#
#         # Wait until the page is loaded completely
#         WebDriverWait(browser, 10).until(
#             EC.presence_of_element_located((By.TAG_NAME, 'body'))
#         )
#
#         status_code = browser.execute_script("return window.performance.timing.responseEnd - window.performance.timing.requestStart;")
#
#         print(f"{url}: {status_code}")
#
#         result_entry = {
#             'url': url,
#             'status_code': status_code,
#         }
#         print(result_entry)
#         results.append(result_entry)
#
#         if status_code in (200, 301, 302):
#             if parsed_url.scheme == 'http':
#                 http_count += 1
#             elif parsed_url.scheme == 'https':
#                 https_count += 1
#
#     except WebDriverException as e:
#         print(f"Warning processing {url}: {e}")
#         result_entry = {
#             'url': url,
#             'error': str(e),
#         }
#         print(result_entry)
#         results.append(result_entry)
#     except TimeoutError as e:
#         print(f"Warning processing {url}: {e}")
#         result_entry = {
#             'url': url,
#             'error': str(e),
#         }
#         print(result_entry)
#         results.append(result_entry)
#
#
# def main():
#     global http_count, https_count, results
#
#     chrome_options = webdriver.ChromeOptions()
#     # Add any additional options you need, e.g., proxy settings, headless mode, etc.
#     chrome_options.add_argument('--headless')
#
#     with ThreadPoolExecutor(max_workers=10) as executor, tqdm(
#             total=len(open('../total.txt', 'r', encoding='utf-8').readlines())) as pbar:
#         with open('../total.txt', 'r', encoding='utf-8') as file:
#             for line in file:
#                 executor.submit(process_url, line.strip(), chrome_options)
#                 pbar.update(1)
#                 time.sleep(0.1)
#
#     with open('./http_https_results.csv', 'w', encoding='utf-8', newline='') as csv_file:
#         writer = csv.writer(csv_file)
#         writer.writerow(['url', 'status_code'])
#         for result in results:
#             writer.writerow([result['url'], result['status_code']])
#
#     print(f"Total HTTP-supported URLs: {http_count}")
#     print(f"Total HTTPS-supported URLs: {https_count}")
#
#
# if __name__ == "__main__":
#     main()
#
#
#

#
# 403 94
# 412 161   all https
# 404 6个,经过检查发现,其url中包含了请求参数和非法路径，https://12345.zhangzhou.gov.cn/public/index/index.jsp?loginflag=false
# 422 3个
# 421 1个
# 500 1个
# 521 61个
# getaddrinfo failed 172
# timedout 67
# has expired 6
# get local issuer certificate 28
# self signed certificate in certificate chain 8
# self signed certificate 48
# 由于目标计算机积极拒绝，无法连接 10
# 远程主机强迫关闭了一个现有的连接 1
# doesn\'t match  27
# Remote end closed connection without response 1
# SSLV3 1   http not https
# OSError 1 http not https