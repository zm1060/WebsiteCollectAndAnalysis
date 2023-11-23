import os
from time import sleep
from urllib.parse import urlparse
import requests
import concurrent.futures
import urllib3
import chardet
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


# <script>window.location='/dzsggzy/'</script>
# <script>
# document.location="/platform/tjkj/index.html"
# </script>
# <meta http-equiv="refresh" content="0;url=./index.html">
# <meta http-equiv='refresh' content='1;URL="./ZJ/"'>
# <meta http-equiv="refresh" content="0.1;url=https://hlj.tobacco.gov.cn/portal/index.htm">
# <script type="text/javascript">
#             window.location.href = "https://hlj.tobacco.gov.cn/portal/index.htm"
# </script>
# <script type="text/javascript">document.location.href='/site/default.aspx'</script>
# <script type="text/javascript">
# 	initPage();
# 	function initPage(){
# 		location.href='home/home.html';
# 	}
# </script>
# 南京在这方面做的比较好
# <script>setTimeout('window.location.reload();', 1000 )</script>
#    <script type="text/javascript">
# 		var yd = "/zgnjsjb/index.html";//移动端地址
# 		var pc = "/index.html";//PC端地址
# 		var userAgentInfo = navigator.userAgent;
# 		var Agents = ["Android","iPhone","SymbianOS","Windows Phone","iPad","iPod"];
# 		var tags = false;
# 		for (var v = 0; v < Agents.length; v++) {
# 			if (userAgentInfo.indexOf(Agents[v]) > 0){
# 				tags =true;
# 				break;
# 			}
# 		}
# 		if(tags){
# 			window.location.href=yd;
# 		}else{
# 			window.location.href=pc;
# 		}
# </script>


# some website use 81 port not default 80 port:
# it means if you just input the domain, you can not have access to the website, if the operaator did not provide any redirection options or tips.
# 江西  perform so bad
# http://credit.zglh.gov.cn/
# http://credit.zglh.gov.cn:81/
# http://credit.wugongshan.gov.cn:81/
def process_url(url):
    return urlparse(url).netloc


def get_domain():
    directory = '../domain_txt'
    all_domain = []
    failed_domains = []

    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                urls = [line.strip() for line in file if line.strip()]

            for url in urls:
                sdomain = process_domain(url)
                if sdomain:
                    all_domain.append(sdomain)
                    print(sdomain)
                    # store_response(sdomain)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(store_response, all_domain))

    failed_domains = [domain for domain, result in zip(all_domain, results) if not result]
    save_failed_domains(failed_domains)
    return all_domain


def process_domain(domain):
    if not domain.startswith("http"):
        domain = "http://" + domain
    parsed_url = urlparse(domain)
    return parsed_url.geturl() if parsed_url.scheme and parsed_url.netloc else None


# def store_response(domain):
#     filename = f"./response/{domain.split('//')[1]}.txt"
#     if os.path.isfile(filename):
#         print(f"File already exists: {filename}")
#         return True
#
#     try:
#         headers = {
#             'Content-Type': 'text/html;charset=utf-8',
#             'Connection': 'close',
#             'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
#         }
#
#         response = requests.get(domain, headers=headers, verify=False, timeout=10, allow_redirects=True)
#         response.encoding = "utf-8"
#
#         if response.status_code == 200 and 'Content-Type' in response.headers and 'text' in response.headers['Content-Type']:
#             filename = f"./response/{process_url(domain)}.txt"
#             with open(filename, "w", encoding="utf-8") as file:
#                 file.write(response.text)
#             print(f"Response stored: {filename}")
#             return True
#         else:
#             print(f"Failed to request website: {domain} (Status code: {response.status_code})")
#             if domain.startswith("http://"):
#                 return store_response(domain.replace("http://", "https://"))
#             return False
#
#     except requests.exceptions.RequestException as e:
#         print(f"Failed to request website: {domain} ({str(e)})")
#         return False


# 河南    访问被云平台拦截     云平台WAF防护规则

def store_response(domain):
    sdomain = urlparse(domain).netloc
    filename = f"./response/{sdomain}.txt"
    if os.path.isfile(filename):
        print(f"File already exists: {filename}")
        # Check if the file contains "ICP备案"
        with open(filename, "r", encoding="utf-8") as file:
            file_content = file.read()
            if "ICP备" in file_content or "icp" in file_content or "ICP" in file_content:
                print(f"File contains 'ICP备案': {filename}")
                return True
            else:
                print(f"File does not contain 'ICP备案': {filename}")
    try:
        options = Options()
        options.add_argument("--headless")  # Run Chrome in headless mode
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(options=options)  # Provide the path to your Chrome driver executable
        # Check the URL scheme
        if domain.startswith("http://") or domain.startswith("https://"):
            driver.get(domain)
            sleep(6)
            # Find the <html> element and get its text
            page_source = driver.execute_script("return document.documentElement.outerHTML")
            response_text = page_source

            with open(filename, "w", encoding="utf-8") as file:
                file.write(response_text)

            print(f"Response stored: {filename}")
            driver.quit()
            return True
        else:
            # Invalid URL scheme
            print(f"Invalid URL scheme for domain: {domain}")
            return False
    except Exception as e:
        print(f"Failed to request website: {domain} ({str(e)})")
        with open(f"{str(type(e).__name__)}.txt", "a") as file:
            file.write(domain + "\n")
        return False


def save_failed_domains(failed_domains):
    with open('failed_domains.txt', 'w', encoding="utf-8") as file:
        for domain in failed_domains:
            file.write(f"{domain}\n")


# Suppress only the single InsecureRequestWarning from urllib3 needed when verify=False in requests.get()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# Call get_domain() to start the process
get_domain()
