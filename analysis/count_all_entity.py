import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 从total.txt读取URL列表
with open('total.txt', 'r', encoding='utf-8') as file:
    urls = file.readlines()

# 初始化WebDriver，启用Headless模式
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

# 存储所有网站的资源信息
all_resources = []

# 逐个访问网站并获取资源信息
for url in urls:
    # 清理URL，去除换行符等
    url = url.strip()

    # 打开网站
    driver.get(url)

    # 等待页面加载完成
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # 获取页面加载的所有资源
    resources = driver.execute_script("return window.performance.getEntries();")

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

    # 将资源信息添加到总资源列表
    all_resources.append({url: resource_list})

# 关闭浏览器窗口
driver.quit()

# 将所有网站的资源信息以JSON格式写入文件
with open('all_resources.json', 'w', encoding='utf-8') as json_file:
    json.dump(all_resources, json_file, ensure_ascii=False, indent=2)

print("All resource information saved to all_resources.json")
