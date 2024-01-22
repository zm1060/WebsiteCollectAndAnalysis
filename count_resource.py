import os
import json
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import InvalidArgumentException, TimeoutException, WebDriverException


# Function to load existing data from all_resources.json
def load_existing_data():
    existing_data = {}
    if os.path.exists('all_resources.json'):
        with open('all_resources.json', 'r', encoding='utf-8') as json_file:
            try:
                existing_data = json.load(json_file)
            except json.decoder.JSONDecodeError:
                print("Error loading existing data. File might be malformed.")
    return existing_data


def process_url(url):
    try:
        # 打开网站
        driver.get(url)

        # 等待页面加载完成
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # 获取页面加载的所有资源
        resources = driver.execute_script("return window.performance.getEntries();")

        # 存储资源信息的列表
        resource_list = []

        # 定义视频文件扩展名列表
        video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.wmv']

        # 处理每个资源
        for resource in resources:
            # 检查资源类型是否为视频
            if 'video' in resource.get('resourceType', '').lower():
                print(f"Skipping video resource for URL '{url}'")
                continue

            # 检查资源名称是否包含视频文件扩展名
            if any(extension in resource.get('name', '').lower() for extension in video_extensions):
                print(f"Skipping video resource for URL '{url}'")
                continue

            # 构建资源信息字典
            resource_info = {
                'Resource Type': resource.get('initiatorType', 'N/A'),
                'Resource Name': resource.get('name', 'N/A'),
                'Resource Size': resource.get('transferSize', 'N/A'),
                'Resource Duration': resource.get('duration', 'N/A'),
                'URL': url
            }

            # 添加到资源列表
            resource_list.append(resource_info)

        # 将资源信息实时写入文件
        with open('all_resources.json', 'a', encoding='utf-8') as json_file:
            json.dump({url: resource_list}, json_file, ensure_ascii=False, indent=2)
            json_file.write('\n')

    except TimeoutException as te:
        print(f"Timeout processing URL '{url}': {te}")
        # Retry logic goes here
    except WebDriverException as e:
        # 异常处理逻辑...
        print(f"Error processing URL '{url}': {e}")
    except Exception as e:
        # 异常处理逻辑...
        print(f"Error processing URL '{url}': {e}")


def main():
    # Load existing data
    existing_data = load_existing_data()

    # 从total.txt读取URL列表
    with open('total.txt', 'r', encoding='utf-8') as file:
        urls = file.readlines()

    # Initialize WebDriver, enable Headless mode
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)

    # 使用ThreadPoolExecutor实现多线程并发处理
    with ThreadPoolExecutor(max_workers=5) as executor:
        # 提交每个URL的处理任务
        futures = [executor.submit(process_url, url.strip()) for url in urls]

        # 等待所有任务完成
        for future in futures:
            future.result()

    # 关闭浏览器窗口
    driver.quit()
    print("All resource information saved to all_resources.json")


if __name__ == "__main__":
    # Initialize WebDriver, enable Headless mode
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    main()
