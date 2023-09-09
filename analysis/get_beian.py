import time

from selenium import webdriver

def check_beian_info(url):
    driver = webdriver.Chrome()

    try:
        # 加载网站
        driver.get(url)
        time.sleep(5)

        # 获取整个页面的源代码
        page_source = driver.page_source

        # 在源代码中搜索备案信息、ICP备案信息和公安备案信息
        beian_info_present = '备案' in page_source
        icp_beian_info_present = 'ICP' in page_source
        police_beian_info_present = '公安备案' in page_source

        # 返回检查结果
        data = {
            '域名': url,
            '备案信息': beian_info_present,
            'ICP备案信息': icp_beian_info_present,
            '公安备案信息': police_beian_info_present
        }
        return data
    finally:
        # 关闭WebDriver
        driver.quit()


# Example usage
url = 'https://www.baidu.com'
result = check_beian_info(url)
print(result)
