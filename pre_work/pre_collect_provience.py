import json
import glob

# List all the JSON files in the directory
json_files = glob.glob("sheng/*.json")

city_info = []

# Process each JSON file
for file in json_files:
    with open(file, "r") as f:
        data = json.load(f)

        if "cityDownload" in data:
            city_data = data["cityDownload"]

            for city in city_data:
                city_info.append({
                    "cityCode": city["cityCode"],
                    "cityName": city["cityName"],
                    "province": city["countyInfo"][0]["sheng"],
                    "siteCode": city["countyInfo"][0]["siteCode"]
                })

        if "directCityDownload" in data:
            direct_city_data = data["directCityDownload"]

            for city in direct_city_data:
                if city["shi"] == "":
                    city_info.append({
                        "cityCode": city["siteCode"],
                        "cityName": city["sheng"],
                        "province": city["sheng"],
                        "siteCode": city["siteCode"]
                    })
                else:
                    city_info.append({
                        "cityCode": city["siteCode"],
                        "cityName": city["shi"],
                        "province": city["sheng"],
                        "siteCode": city["siteCode"]
                    })

print(city_info)
# Save city_info to result.json with Chinese characters displayed properly
with open("../result.json", "w", encoding="utf-8") as outfile:
    json.dump(city_info, outfile, ensure_ascii=False)