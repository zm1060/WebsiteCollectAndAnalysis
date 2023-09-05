import json

import requests
from concurrent.futures import ThreadPoolExecutor

from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter, Retry

# Set the cookies
cookies = {
    'JSESSIONID': '15DAAEDF6D6F9EB9DD3535E503668252.tomcat-gongkai-b01',
    'Hm_lvt_3a125f686abed6dc0209db1fb2efac2b': '1693879772',
    'Hm_lpvt_3a125f686abed6dc0209db1fb2efac2b': '1693895491'
}


# Function to download a file
def download_file(item):
    payload = {
        'downames': item[0]
    }
    download_url = "https://zfwzxx.www.gov.cn/check_web/downloadTemp_downFile.action"

    headers = {
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://zfwzxx.www.gov.cn',
        'Referer': 'https://zfwzxx.www.gov.cn/check_web/databaseInfo/download',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    }

    # Create a session with connection pooling and retry mechanism
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))

    # Send a POST request to download the content
    response = session.post(download_url, data=payload, cookies=cookies, headers=headers)

    # Save the content to a file
    download_name = item[1] + '.zip'
    with open(download_name, 'wb') as file:
        print("Downloading", download_name)
        file.write(response.content)


# Main function
def main():
    with open('result.json', "r") as f:
        data_from_json = json.load(f)
    print(data_from_json)
    data = [("alldistrict", "地方所属网站"), ("shengmh", "省级门户")]

    for record in data_from_json:
        print(record)
        if record['cityName'] == record['province']:
            data.append((record['siteCode'], record['province']+"_"+"市级单位"))
        else:
            if record['cityCode'] == record['siteCode']:
                # xxx + "区县级单位"
                data.append((record['siteCode'], record['province']+"_"+record['cityName']))
            else:
                data.append((record['cityCode'], record['province']+"_"+record['cityName']+"_"+"市级单位"))
                data.append((record['siteCode'], record['province']+"_"+record['cityName']+"_"+"区县级单位"))
    # Print the extracted data
    for id_value, text_value in data:
        print("ID:", id_value)
        print("Text:", text_value)

    if len(data) > 0:
        # Use a thread pool executor for concurrent requests
        with ThreadPoolExecutor() as executor:
            # Submit download tasks to the executor
            executor.map(download_file, data)
    else:
        print("No active elements selected for download.")


# Execute the main function
if __name__ == "__main__":
    main()
