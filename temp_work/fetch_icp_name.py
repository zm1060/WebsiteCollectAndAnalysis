import re
import time
from urllib.parse import urlparse

import pandas as pd
import requests

# Load the CSV file
df = pd.read_csv('./current.csv')


# Function to fetch the name from the API
def fetch_name_from_api(domain):
    try:
        response = requests.get(f'https://v.api.aa1.cn/api/icp/index.php?url={domain}')
        data = response.json()
        time.sleep(2)
        return data.get('name', '')
    except Exception as e:
        print(f"Error fetching data from API for {domain}: {e}")
        return ''


def clean_url(url):
    return re.sub(r'\*.', '', url)


# Process the dataframe
for index, row in df.iterrows():
    column_four_value = row[3]  # Assuming the fourth column is at index 3
    # Check if column_four_value is a string
    if isinstance(column_four_value, str):
        if not (column_four_value.endswith('公司') or
                column_four_value.endswith('中心') or
                column_four_value.endswith('学校') or
                column_four_value.endswith('院') or
                column_four_value.endswith('园')):
            domain = row[1]  # Assuming the second column is at index 1
            if isinstance(domain, str):
                url = clean_url(domain)
                url = urlparse(url).geturl()
                new_name = fetch_name_from_api(domain)
                if new_name:
                    df.at[index, 3] = new_name  # Update the fourth column with the new name
                print(new_name)

# Save the modified dataframe to a new CSV file
df.to_csv('./updated_current.csv', index=False)
