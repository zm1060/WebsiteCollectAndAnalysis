import re
import time

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

# Specify the path to the GeckoDriver executable
gecko_driver_path = "E:\selenium\geckodriver-v0.34.0-win64\geckodriver.exe"

firefox_options = Options()
# firefox_options.add_argument('-headless')  # Uncomment this line if you want to run Firefox in headless mode

# Specify the user agent
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/120.0.0.0"
firefox_options.add_argument(f'user-agent={user_agent}')

# Specify the path to the GeckoDriver executable using Service
web = Firefox(service=Service(gecko_driver_path), options=firefox_options)

url = "https://zfgjj.xa.gov.cn/"

# First request
web.get(url)
print(web.page_source)
time.sleep(1)
# Second request
web.get(url)
print(web.page_source)
time.sleep(1)
# Third request
web.get(url)
print(web.page_source)
time.sleep(1)
# Fourth request
cooki = web.get_cookies()
web.get(url, cooki)
print(cooki)
print(web.page_source)
time.sleep(1)

cooki = web.get_cookies()
web.get(url, cooki)
print(cooki)
web.implicitly_wait(4)
print(web.page_source)

# Close the browser
web.quit()
# from webbrowser import Chrome
#
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
#
#
# def driver_chrome():
#     chrome_options = webdriver.ChromeOptions()
#
#     chrome_options.add_argument('headless')
#     chrome_options.add_argument('disable-infobars')
#     chrome_options.add_argument("--disable-extensions")
#     chrome_options.add_argument("--disable-gpu")
#     chrome_options.add_argument(
#         'user-agent="MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"')
#     chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
#     chrome_options.add_experimental_option("useAutomationExtension", False)
#     driver = webdriver.Chrome(options=chrome_options)
#     return driver
#
# def get_cookies(surl):
#     session = {}
#     driver = driver_chrome()
#     driver.get(surl)
#     cookies = driver.get_cookies()
#     for i in cookies:
#         session[i.get('name')] = i.get('value')
#     driver.close()
#     driver.quit()
#     return session
#
# get_cookies("https://zfgjj.xa.gov.cn/")
# import time
#
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# # https://cdwater.chengdu.gov.cn/
# url = "https://zfgjj.xa.gov.cn/"
# #"https://cdcz.chengdu.gov.cn/"
#
# # chrome.exe --remote-debugging-port=9222 --user-data-dir="E:\data_info\selenium_data"
# options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/120.0.0.0')
# options.add_argument('--disable-gpu')  # Disable GPU acceleration
# options.add_argument('--disable-infobars')  # Disable infobars (notifications)
# options.add_argument('--disable-extensions')  # Disable extensions
# options.add_argument('--disable-dev-shm-usage')  # Disable the /dev/shm usage
# options.add_argument('--disable-browser-side-navigation')  # Disable browser side navigation
# options.add_argument('--no-sandbox')  # Disable sandboxing for Linux
# # options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option("useAutomationExtension", False)
#
#
#
# browser = webdriver.Chrome(options=options)
# wait = WebDriverWait(browser, 10)  # Timeout duration is set to 10 seconds
#
# browser.get(url)
# # This call might return 521-related anti-crawling JavaScript code
# # cookies = browser.get_cookies()
# # print(cookies)
# # # Adding cookies obtained from the first request to the browser
# # for cookie in cookies:
# #     browser.add_cookie(cookie)
#
# # Now the browser has the cookies from the first request when making the second request
# time.sleep(2)
# # print(browser.page_source)
# # print(browser.get_cookies())
# browser.get(url)
# time.sleep(1)
# browser.get(url)
# time.sleep(1)
# browser.get(url)
# html = browser.page_source
# print(html)
# print(browser.get_cookies())
#
# # Close the browser
# browser.quit()


# import re
# import requests
# import execjs
#
#
#
#
# class YiDaiYiLuSpider(object):
#     """
#     中国一带一路网（521反爬）
#     """
#     url = r'https://zfgjj.xa.gov.cn/'
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/120.0.0.0"
#     }
#
#     @classmethod
#     def get_text521(cls):
#         """
#
#         :return:
#         """
#
#         rs = requests.session()
#         resp = rs.get(url=cls.url, headers=cls.headers)
#         text_521 = ''.join(re.findall('<script>(.*?)</script>', resp.text))
#         cookie_id = '; '.join(['='.join(item) for item in resp.cookies.items()])
#         return cookie_id, text_521
#
#     @classmethod
#     def generate_cookies(cls, func, url):
#         func_return = func.replace('eval', 'return').replace('document.cookie=', 'return ').replace('location.href=location.pathname+location.search', '' )
#         content = execjs.compile(func_return)
#         eval_func = content.call('f')
#         print(eval_func)
#         __jsl_clearance = eval_func.split(';')[0]
#         # var = str(eval_func.split('=')[0]).split(' ')[1]
#         # rex = r">(.*?)</a>"
#         # rex_var = re.findall(rex, eval_func)[0]
#         # mode_func = eval_func.replace('document.cookie=', 'return ').replace(';if((function(){try{return !!window.addEventListener;}', ''). \
#         #     replace("catch(e){return false;}})()){document.addEventListener('DOMContentLoaded'," + var + ",false)}", ''). \
#         #     replace("else{document.attachEvent('onreadystatechange'," + var + ")}", '').\
#         #     replace(r"setTimeout('location.href=location.pathname+location.search.replace(/[\?|&]captcha-challenge/,\'\')',1500);", '').\
#         #     replace('return return', 'return').\
#         #     replace("document.createElement('div')", '"https://zfgjj.xa.gov.cn/"').\
#         #     replace(r"{0}.innerHTML='<a href=\'/\'>{1}</a>';{0}={0}.firstChild.href;".format(var, rex_var), '')
#         # content = execjs.compile(mode_func)
#         # cookies_js = content.call(var)
#         # __jsl_clearance = cookies_js.split(';')[0]
#         return __jsl_clearance
#
#     @classmethod
#     def crawler(cls):
#         url = r'https://zfgjj.xa.gov.cn/'
#         cookie_id, text_521 = cls.get_text521()
#         __jsl_clearance = cls.generate_cookies(text_521, url)
#         cookies = "{0};{1};".format(cookie_id, __jsl_clearance)
#         cls.headers["Cookie"] = cookies
#         print(cls.headers)
#         res = requests.get(url=url, headers=cls.headers)
#         res.encoding = 'utf-8'
#         print(res.text)
#
#
# if __name__ == '__main__':
#
#     YiDaiYiLuSpider.crawler()
