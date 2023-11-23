from zoomeye.sdk import ZoomEye

api_key="9D5F4EFD-Aa9B-7abEE-7B7d-e02db06a79c"

zm = ZoomEye(api_key)

target_ip = '114.114.114.114'

# Define your query, e.g., 'ip:YOUR_TARGET_IP'
query = ('ip ' + target_ip)

# Perform the search
try:
    result = zm.dork_search(query)
    print(result)
except Exception as e:
    print(f"An error occurred: {e}")