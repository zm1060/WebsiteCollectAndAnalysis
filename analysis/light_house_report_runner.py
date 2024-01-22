# import json
# import os
# import time
# from asyncio import subprocess
# from urllib.parse import urlparse
#
#
# def process_url(url):
#     parsed_url = urlparse(url)
#     domains = parsed_url.netloc
#     return domains
#
#
# # under the directory, has many directory, under these directories are files, which contains many urls.
# def run_lighthouse_with_directory(directory):
#     all_domain = []
#
#     for filename in os.listdir(directory):
#         if filename.endswith('.txt'):
#             unit_name = filename.split('.txt')[0]
#             urls = []
#             with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
#                 urls = file.readlines()
#             for url in urls:
#                 url = url.strip()  # Remove leading/trailing whitespace and newlines
#                 if url:
#                     sdomain = process_domain(url)
#                     dom = urlparse(sdomain).netloc
#                     if sdomain:
#                         all_domain.append(sdomain)
#                         print(sdomain)
#                         output_directory = './lighthouse/' + unit_name + '/'
#                         os.makedirs(output_directory, exist_ok=True)
#                         json_filename = f'./lighthouse/{unit_name}/{dom}.json'
#                         if os.path.exists(json_filename):
#                             continue
#                         try:
#                             stream = os.popen(
#                             'lighthouse --quiet --no-update-notifier --no-enable-error-reporting --output=json ' + '--output-path=' + json_filename +' --chrome-flags="--headless" ' + sdomain)
#                             # lighthouse --quiet --no-update-notifier --no-enable-error-reporting --output=json --output-path=./lighthouse/上海市/stcsm.sh.gov.cn.json --chrome-flags="--headless" https://stcsm.sh.gov.cn
#                             time.sleep(120)
#                             process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
#                                                        stderr=subprocess.PIPE)
#
#                             # 等待进程完成或者超时（以秒为单位，这里设置为120秒）
#                             stdout, stderr = process.communicate(timeout=120)
#
#                             # 检查进程是否仍在运行（超时未发生）
#                             if process.poll() is None:
#                                 # 进程仍在运行，终止它
#                                 process.terminate()
#                                 print("Process terminated due to timeout.")
#                             else:
#                                 # 进程已完成
#                                 print("Process completed.")
#
#                             # 处理输出（stdout 和 stderr）
#                             print("stdout:", stdout.decode())
#                             print("stderr:", stderr.decode())
#
#                         except subprocess.TimeoutExpired:
#                             # 超时发生
#                             process.terminate()
#                             print("Process terminated due to timeout.")
#                         except Exception as e:
#                             print(str(e))
#
#
# def process_domain(domain):
#     # Add "http://" to domain names that don't have it
#     if not domain.startswith("http"):
#         domain = "http://" + domain
#
#     # Parse the URL and extract the base domain
#     parsed_url = urlparse(domain)
#     base_url = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path
#     if  not parsed_url.scheme or not parsed_url.netloc:
#         return
#     return base_url
#
#
# run_lighthouse_with_directory("../domain_txt")

##########################################################################################
# Actual run version
##########################################################################################
# import os
# import subprocess
# import concurrent.futures
# from urllib.parse import urlparse
# import time
#
#
# def process_domain(domain):
#     if not domain.startswith("http"):
#         domain = "http://" + domain
#
#     parsed_url = urlparse(domain)
#     base_url = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path + parsed_url.query + parsed_url.fragment
#     if not parsed_url.scheme or not parsed_url.netloc:
#         return
#     return base_url
#
#
# def lighthouse_task(url, unit_name):
#     try:
#         sdomain = process_domain(url)
#         dom = urlparse(sdomain).netloc
#         if sdomain:
#             all_domain.append(sdomain)
#             print(sdomain)
#             output_directory = f'./new_lighthouse/{unit_name}/'
#             os.makedirs(output_directory, exist_ok=True)
#             json_filename = f'./new_lighthouse/{unit_name}/{dom}.json'
#
#             if os.path.exists(json_filename):
#                 return
#
#             command = f'lighthouse --quiet --no-update-notifier --no-enable-error-reporting --screenEmulation.disabled --output=json ' \
#                       f'--output-path={json_filename} --chrome-flags="--headless" {sdomain}'
#
#             process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#
#             stdout, stderr = process.communicate(timeout=120)
#
#             if process.poll() is None:
#                 process.terminate()
#                 print("Process terminated due to timeout.")
#             else:
#                 print("Process completed.")
#
#             print("stdout:", stdout.decode())
#             print("stderr:", stderr.decode())
#
#     except subprocess.TimeoutExpired:
#         process.terminate()
#         print("Process terminated due to timeout.")
#     except Exception as e:
#         print(str(e))
#
#
# def run_lighthouse_with_directory(directory):
#     global all_domain
#     all_domain = []
#
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         futures = []
#         for filename in os.listdir(directory):
#             if filename.endswith('.txt'):
#                 unit_name = filename.split('.txt')[0]
#                 urls = []
#                 with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
#                     urls = file.readlines()
#                 futures.extend([executor.submit(lighthouse_task, url.strip(), unit_name) for url in urls])
#
#         concurrent.futures.wait(futures)
#
#
# # 替换为你的目录路径
# run_lighthouse_with_directory("../domain_txt")



import os
import subprocess
import concurrent.futures
from urllib.parse import urlparse
from pathlib import Path


def process_domain(domain):
    parsed_url = urlparse(domain)
    if parsed_url.scheme and parsed_url.netloc:
        return parsed_url.geturl()  # Construct complete URL


def lighthouse_task(url, unit_name):
    try:
        sdomain = process_domain(url)
        if sdomain:
            output_dir = Path(f'./new_lighthouse/{unit_name}')
            output_dir.mkdir(parents=True, exist_ok=True)  # Create directory if needed
            json_filename = output_dir / f'{urlparse(sdomain).netloc}.json'

            if json_filename.exists():
                return  # Skip if output already exists

            command = (
                f'lighthouse --quiet --no-update-notifier --no-enable-error-reporting '
                f'--screenEmulation.disabled --chrome-flags="--window-size=1,1" --output=json --output-path="{json_filename}" '
                f'--chrome-flags="--headless" {sdomain}'
            )

            process = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=120)

            if process.returncode == 0:
                print(f"Lighthouse completed for {sdomain}")
            else:
                print(f"Lighthouse failed for {sdomain}: {process.stderr}")

    except subprocess.TimeoutExpired:
        print(f"Lighthouse timed out for {url}")
    except Exception as e:
        print(f"Error processing {url}: {str(e)}")


def run_lighthouse_with_directory(directory):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for filename in os.listdir(directory):
            if filename.endswith('.txt'):
                unit_name = filename.split('.txt')[0]
                with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                    urls = [url.strip() for url in file.readlines()]
                futures.extend(executor.submit(lighthouse_task, url, unit_name) for url in urls)

        concurrent.futures.wait(futures)


# Replace with your directory path
run_lighthouse_with_directory("../domain_txt")
