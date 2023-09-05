import requests
from bs4 import BeautifulSoup

url = "https://zfwzxx.www.gov.cn/check_web/databaseInfo/download"

# Set the cookies
cookies = {
    'JSESSIONID': '78665C94E87D6AFC69C5D888D4536307.tomcat-gongkai-b01',
    'Hm_lvt_3a125f686abed6dc0209db1fb2efac2b': '1693879772',
    'Hm_lpvt_3a125f686abed6dc0209db1fb2efac2b': '1693880547'
}

# Make the GET request with cookies
# response = requests.get(url, cookies=cookies)
# html_conten = response.text
file_path = "government.html"
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

# Find the active elements within the .dpage_ul class and extract their ids
# the below commented code is how download.js works, but we do not use it.
# active_elements = soup.select(".dpage_ul .active")


if len(data) > 0:
    for item in data:
        # Prepare the payload for the download request
        payload = {
            "downames": item[0]
        }
        print(payload)
        # Send a POST request to download the content
        download_url = "https://zfwzxx.www.gov.cn/check_web/downloadTemp_downFile.action"
        response = requests.post(download_url, data=payload)

        # Save the content to a file
        download_name = item[1]
        with open(download_name, 'wb') as file:
            file.write(response.content)
else:
    print("No active elements selected for download.")




# Perform the download by simulating the onclick event of the download button
# You need to extract the relevant information from the onclick attribute value
# and make a request accordingly to download the desired content.

# Example code to extract the relevant information from the onclick attribute value:
# onclick_value = "_trackData.push(['addaction','全国政府网站基本信息数据库', '部门下载按钮'])"
# Extract the URL or any other necessary information from the onclick value and use it to download the content.

# Make sure to handle any necessary authentication or form submission if required.

# Example code to download the content using requests:
# download_url = "DOWNLOAD_URL"
# response = requests.get(download_url)
# content = response.content
# Save the content to a file or process it according to your needs.

# Note: Remember to add necessary error handling and customize the code as per your requirements.