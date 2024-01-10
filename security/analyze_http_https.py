import json

with open('./protocol_result.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
    http_data = data[0]['urls']
    https_data = data[1]['urls']
    htpp_count = 0
    https_count = 0
