import os
import json
import requests
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

active_url_count = {}
dead_url_count = {}
province_count = {}
results = {}


def process_url(url, protocol, province):
    global headers
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Connection': 'keep-alive',
        }
        response = requests.get(url, headers=headers, timeout=10, verify=False, allow_redirects=True, stream=True, proxies={"http": None, "https": None})
        response.encoding = "utf-8"

        print(f"{url}: {protocol} Status Code - {response.status_code}")

        if province not in results:
            results[province] = {"province_name": province, "domains": []}

        if response.status_code == 200 and 'Content-Type' in response.headers and 'text' in response.headers['Content-Type']:
            province_count[province] += 1
            save_html_content(province, url, response.text)
            result_entry = {"domain": url, "status": "active"}
            results[province]["domains"].append(result_entry)
            active_url_count[province] += 1
        else:
            province_count[province] += 1
            dead_url_count[province] += 1
            result_entry = {"domain": url, "status": response.status_code}
            results[province]["domains"].append(result_entry)

        # Include response properties in the JSON output
        response_info = {
            "is_redirect": response.is_redirect,
            "is_permanent_redirect": response.is_permanent_redirect,
            "elapsed_time": response.elapsed.total_seconds()
        }

        # Include response properties in the JSON output
        # response_info = {
        #    "is_redirect": len(response.history) > 0,
        #    "is_permanent_redirect": response.status_code == 301 if len(response.history) > 0 else False,
        #    "elapsed_time": response.elapsed.total_seconds()
        # }

        results[province]["domains"][-1]["response_info"] = response_info

    except Exception as e:
        if "HTTP" in str(e) and url.startswith("http://"):
            https_url = url.replace("http://", "https://")
            try:

                again_response = requests.get(https_url, headers=headers, timeout=10, verify=False, allow_redirects=True,
                                              stream=True,
                                              proxies={"http": None, "https": None})
                again_response.encoding = "utf-8"

                print(f"{https_url}: https Status Code - {again_response.status_code}")

                if province not in results:
                    results[province] = {"province_name": province, "domains": []}

                if again_response.status_code == 200 and 'Content-Type' in again_response.headers and 'text' in \
                        again_response.headers[
                            'Content-Type']:
                    province_count[province] += 1
                    save_html_content(province, https_url, again_response.text)
                    result_entry = {"domain": https_url, "status": "active"}
                    results[province]["domains"].append(result_entry)
                    active_url_count[province] += 1
                else:
                    province_count[province] += 1
                    result_entry = {"domain": https_url, "status": again_response.status_code,}
                    results[province]["domains"].append(result_entry)
                    dead_url_count[province] += 1

                # Include response properties in the JSON output
                response_info = {
                    "is_redirect": again_response.is_redirect,
                    "is_permanent_redirect": again_response.is_permanent_redirect,
                    "elapsed_time": again_response.elapsed.total_seconds()
                }
                results[province]["domains"][-1]["response_info"] = response_info
            except Exception as e:
                province_count[province] += 1
                print(f"{https_url}: https Status Code - Error: {e}")
                result_entry = {"domain": https_url, "status": "dead"}
                results[province]["domains"].append(result_entry)
                dead_url_count[province] += 1
        else:
            province_count[province] += 1
            print(f"{url}: {protocol} Status Code - Error: {e}")
            result_entry = {"domain": url, "status": "dead"}
            results[province]["domains"].append(result_entry)
            dead_url_count[province] += 1


def save_html_content(province, url, content):
    province_dir = f"new_response/{province}"
    os.makedirs(province_dir, exist_ok=True)

    u = urlparse(url)
    domain_path = u.scheme + '/' + u.netloc + u.path + u.query + u.fragment
    file_name = f"{domain_path.replace('/', '_')}.html"
    file_path = os.path.join(province_dir, file_name)
    # Convert content from the original encoding to UTF-8

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)


def process_line(line, province):
    line = line.strip()
    u = urlparse(line)

    domain = u.netloc + u.path + u.query + u.fragment

    if u.scheme == "https":
        https_url = f"https://{domain}"
        process_url(https_url, "https", province)
    else:
        http_url = f"http://{domain}"
        process_url(http_url, "http", province)


def process_file(file_name, province):
    file_path = f"domain_txt/{file_name}"

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        active_url_count[province] = 0
        dead_url_count[province] = 0
        province_count[province] = 0

        with ThreadPoolExecutor(max_workers=20) as executor:
            executor.map(lambda line: process_line(line, province), lines)

    except Exception as e:
        print(f"Error processing file {file_name}: {e}")


if __name__ == "__main__":
    dir_entries = os.listdir("domain_txt")

    for entry in dir_entries:
        if not entry.endswith(".txt"):
            continue
        province = entry.split(".txt")[0]

        # Check if JSON file already exists for the province
        json_filename = f"{province}_results.json"
        if os.path.exists(json_filename):
            print(f"JSON file already exists for {province}. Skipping...")
            continue

        print(province)
        process_file(entry, province)

        # Store results in a JSON file for each province
        output_province = {
            "active_url_count": active_url_count[province],
            "dead_url_count": dead_url_count[province],
            "total_url_count":  active_url_count[province] + dead_url_count[province],
            "domains": results[province]["domains"]
        }

        with open(json_filename, 'w', encoding='utf-8') as json_file:
            json.dump(output_province, json_file, indent=4)

    print(f"Results written to {json_filename}")
