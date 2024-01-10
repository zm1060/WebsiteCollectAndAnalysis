import os
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import InvalidArgumentException, TimeoutException, WebDriverException  # Import WebDriverException

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

# 逐个访问网站并获取资源信息
for url in urls:
    # 清理URL，去除换行符等
    url = url.strip()

    # Check if data for this URL already exists
    if url in existing_data:
        print(f"Data for URL '{url}' already exists. Skipping...")
        continue

    try:
        # 打开网站
        driver.get(url)

        # 等待页面加载完成
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # 获取页面加载的所有资源
        resources = driver.execute_script("return window.performance.getEntries();")

        # 计算总资源大小
        total_size = sum(resource.get('transferSize', 0) for resource in resources)

        # 检查总资源大小是否超过阈值（例如，不加载超过10 MB的资源）
        if total_size <= 10 * 1024 * 1024:  # 10 MB in bytes
            # 继续处理资源
            # 存储资源信息的列表
            resource_list = []

            # 处理每个资源
            for resource in resources:
                # 构建资源信息字典
                resource_info = {
                    'Resource Type': resource.get('initiatorType', 'N/A'),
                    'Resource Name': resource.get('name', 'N/A'),
                    'Resource Size': resource.get('transferSize', 'N/A'),
                    'Resource Duration': resource.get('duration', 'N/A'),
                }
                # 添加URL作为键值对
                resource_info['URL'] = url
                print(resource_info)
                # 添加到资源列表
                resource_list.append(resource_info)

            # 将资源信息实时写入文件
            with open('all_resources.json', 'a', encoding='utf-8') as json_file:
                json.dump({url: resource_list}, json_file, ensure_ascii=False, indent=2)
                json_file.write('\n')

        else:
            # 将资源信息实时写入大文件表
            with open('large_resources.json', 'a', encoding='utf-8') as json_file:
                json.dump({url: resource_list}, json_file, ensure_ascii=False, indent=2)
                json_file.write('\n')
            print(f"Skipping URL '{url}' as total resource size exceeds 10 MB.")

    except WebDriverException as e:
        if 'disconnected: not connected to DevTools' in str(e).lower():
            print(f"WebDriver disconnected error for URL '{url}'. Continuing...")
            continue
        elif 'invalid session id' in str(e).lower():
            print(f"Session ID error for URL '{url}'. Refreshing browser and continuing...")
            driver.refresh()
            continue
        else:
            print(f"Error processing URL '{url}': {e}")
            continue


    except (InvalidArgumentException, TimeoutException) as e:
        print(f"Error processing URL '{url}': {e}")
        driver.refresh()
        continue

    except Exception as e:
        print(f"URL '{url}': {e}")
        driver.refresh()
        continue

# 关闭浏览器窗口
driver.quit()

print("All resource information saved to all_resources.json")