from ssllabs import ssllabsscanner


cached_data = ssllabsscanner.resultsFromCache("www.baidu.com")

print(cached_data)
print(cached_data['endpoints'][0]['grade'])

# data = ssllabsscanner.newScan("www.baidu.com")
#
# print(data)

