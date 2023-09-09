import requests
from concurrent.futures import ThreadPoolExecutor

from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter, Retry

url = "https://zfwzxx.www.gov.cn/check_web/databaseInfo/download"

# Set the cookies
cookies = {
    'JSESSIONID': '15DAAEDF6D6F9EB9DD3535E503668252.tomcat-gongkai-b01',
    'Hm_lvt_3a125f686abed6dc0209db1fb2efac2b': '1693879772',
    'Hm_lpvt_3a125f686abed6dc0209db1fb2efac2b': '1693895491'
}

# Function to download a file
def download_file(item):
    payload = {
        "downames": item[0]
    }
    print(payload)
    print(item)
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
    # Make the GET request with cookies
    # response = requests.get(url)
    # html_content = response.text

    file_path = "../government.html"
    with open(file_path, 'r') as file:
        html_content = file.read()

    # Create a BeautifulSoup object to parse the HTML
    # soup = BeautifulSoup(response.text, "html.parser")
    soup = BeautifulSoup(html_content, "html.parser")
    # Find the <ul> element with the class 'dpage_ul'
    ul_element = soup.find("ul", class_="dpage_ul")

    # Extract the id and text values from the <li> elements within the <ul>
    li_elements = ul_element.find_all("li")
    data = []
    for li in li_elements:
        div_element = li.find("div", class_="dpage_btn_click")
        id_value = div_element.get("id")
        text_value = div_element.get_text()
        data.append((id_value, text_value))

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