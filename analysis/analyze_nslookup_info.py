import json
import sys
import seaborn as sns

import numpy as np
from aiohttp.helpers import is_ipv4_address
from fuzzywuzzy import fuzz
from math import radians, sin, cos, sqrt, atan2

from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties

from ip_location import awdb


def my_ip_query(ip):
    ip_info = dict()

    filename = r'../ip_location/IP_city_single_WGS84.awdb'
    # filename = os.path.dirname(__file__) + os.sep + 'IP_city_single_WGS84.awdb' #使用绝对路径
    reader = awdb.open_database(filename)
    try:
        (record, prefix_len) = reader.get_with_prefix_len(ip)

        continent = record.get("continent", b'').decode("utf-8")  # 大州
        owner = record.get("owner", b'').decode("utf-8")
        country = record.get("country", b'').decode("utf-8")  # 国家
        province = record.get("province", b'').decode("utf-8")  # 省份
        city = record.get("city", b'').decode("utf-8")  # 城市
        isp = record.get("isp", b'').decode("utf-8")  # 提供商，运营商
        asnumber = record.get("asnumber", b'').decode("utf-8")  # AS编号
        latwgs = record.get("latwgs", b'').decode("utf-8") if sys.version_info[0] == 3 else record.get("latwgs", '')
        lngwgs = record.get("lngwgs", b'').decode("utf-8") if sys.version_info[0] == 3 else record.get("lngwgs", '')
        radius = record.get("radius", b'').decode("utf-8") if sys.version_info[0] == 3 else record.get("radius", '')
        ip_info = {
            'continent': continent,
            'owner': owner,
            'country': country,
            'country_prov_city': '_'.join([country, province, city]),
            'isp': isp,
            'asn': asnumber,
            'latwgs': latwgs,
            'lngwgs': lngwgs,
            'radius': radius,
            'prefix_len': str(prefix_len)
        }

        return ip_info
    except Exception as e:
        return ip_info


def generate_result_nslookup_info():
    # Load nslookup_info.json
    with open('nslookup_info.json', 'r', encoding='utf-8') as file:
        nslookup_info = json.load(file)

    # Initialize a list to store results
    results = {}
    unique_domains = set()
    # Iterate through each domain entry
    for entry in nslookup_info:
        domain = entry['Name']
        domain_info = []
        if domain:
            unique_domains.add(domain)
            # Iterate through each IP address for the domain
            for ip_address in entry['Addresses']:
                record_info = {'ip_address': ip_address, 'ip_info': {}}
                ip_info = {}
                if is_ipv4_address(ip_address):
                    ip_info = my_ip_query(ip_address)
                    record_info['ip_info'] = ip_info
                else:
                    continue
                    # print("IPV6 IP address: " + ip_address)
                # Add IP information to the domain entry
                domain_info.append(record_info)
            # Append the domain entry to the results list
            results[domain] = domain_info
        else:
            print(entry)
    # Save the results to result_nslookup_info.json
    with open('result_nslookup_info.json', 'w', encoding='utf-8') as result_file:
        json.dump(results, result_file, ensure_ascii=False, indent=2)
    print(len(unique_domains))
    print("Results saved to result_nslookup_info.json.")


# Function to calculate Haversine distance between two lat-lng points
def haversine_distance(lat_lng1, lat_lng2):
    # Radius of the Earth in kilometers
    R = 6371.0

    # Convert latitude and longitude from degrees to radians
    lat1, lng1 = map(radians, lat_lng1)
    lat2, lng2 = map(radians, lat_lng2)

    # Calculate differences
    dlat = lat2 - lat1
    dlng = lng2 - lng1

    # Haversine formula
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlng / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Distance in kilometers
    distance = R * c

    return distance


# Function to check if a new 'lat_lng' is similar to existing ones based on distance
def is_similar_lat_lng(new_lat_lng, existing_lat_lngs, distance_threshold):
    if len(existing_lat_lngs) == 0:
        return False
    return all(haversine_distance(new_lat_lng, existing_lat_lng) < distance_threshold for existing_lat_lng in
               existing_lat_lngs)


# Function to check if a new 'country_prov_city' is similar to existing ones
def is_similar_to_existing(new_value, existing_values):
    if len(existing_values) == 0:
        return False
    # 定义相似度阈值（根据需要调整）
    similarity_threshold = 80
    # 使用fuzzywuzzy库的ratio函数计算相似度
    similarities = [fuzz.ratio(new_value, existing_value) for existing_value in existing_values]
    # 如果任何一个相似度超过阈值，返回True
    return any(similarity > similarity_threshold for similarity in similarities)


def calculate_diversity_score(ip_entries):
    # Track unique values for diversity calculation
    unique_asns = set()
    unique_isps = set()
    unique_lat_lng = set()
    unique_country_prov_city = set()

    if len(ip_entries) == 0:
        return {
            'overall_diversity_score': -1,
            'asn_diversity_score': -1,
            'isp_diversity_score': -1,
            'lat_lng_diversity_score': -1,
            'country_prov_city_score': -1,
            'ip_address_score': -1,
            'unique_country_prov_city': [],
            'unique_asns': [],
            'unique_isps': [],
            'unique_lat_lng': [],
            'unique_ips': [],
        }  # Avoid division by zero

    # Iterate through each IP entry
    for entry in ip_entries:
        ip_info = entry['ip_info']

        # Geographic Distribution Score based on 'country_prov_city'
        country_prov_city = ip_info['country_prov_city']

        # Check similarity to existing values
        if not is_similar_to_existing(country_prov_city, unique_country_prov_city):
            unique_country_prov_city.add(country_prov_city)

        # ASN Diversity Score (Proportion of unique ASNs)
        unique_asns.add(ip_info['asn'])

        # ISP Diversity Score (Proportion of unique ISPs)
        unique_isps.add(ip_info['isp'])
        distance_threshold = 500
        # Lat-Lng Diversity Score (Proportion of unique lat-lng combinations based on distance)
        lat_str = ip_info.get('latwgs', '')
        lng_str = ip_info.get('lngwgs', '')

        if lat_str and lng_str:
            lat_lng = (float(lat_str), float(lng_str))
        else:
            # 处理缺失经纬度的情况，例如将 lat_lng 设置为默认值或者抛出异常等
            lat_lng = (0.0, 0.0)  # 默认值示例
        if not is_similar_lat_lng(lat_lng, unique_lat_lng, distance_threshold):
            unique_lat_lng.add(lat_lng)

    # Calculate normalized diversity scores
    asn_diversity_score = len(unique_asns)
    isp_diversity_score = len(unique_isps)
    lat_lng_diversity_score = len(unique_lat_lng)
    print(unique_lat_lng)
    print(lat_lng_diversity_score)
    country_prov_city_score = len(unique_country_prov_city)
    print(unique_country_prov_city)
    print(country_prov_city_score)
    ip_address_score = len(ip_entries)
    # Calculate overall diversity score
    overall_diversity_score = (
                                      asn_diversity_score +
                                      isp_diversity_score +
                                      lat_lng_diversity_score +
                                      country_prov_city_score +
                                      ip_address_score
                              ) / 5.0

    caculated_result = {
        'overall_diversity_score': overall_diversity_score,
        'asn_diversity_score': asn_diversity_score,
        'isp_diversity_score': isp_diversity_score,
        'lat_lng_diversity_score': lat_lng_diversity_score,
        'country_prov_city_score': country_prov_city_score,
        'ip_address_score': ip_address_score,
        'unique_country_prov_city': list(unique_country_prov_city),
        'unique_asns': list(unique_asns),
        'unique_isps': list(unique_isps),
        'unique_lat_lng': list(unique_lat_lng),
        'unique_ips': list(ip_entries),
    }
    return caculated_result


def analyze_isp_distribution(ip_entries):
    isp_distribution = {}

    for entry in ip_entries:
        isp = entry['ip_info']['isp']
        isp_distribution[isp] = isp_distribution.get(isp, 0) + 1

    return isp_distribution


def analyze_asn_distribution(ip_entries):
    asn_distribution = {}

    for entry in ip_entries:
        asn = entry['ip_info']['asn']
        asn_distribution[asn] = asn_distribution.get(asn, 0) + 1

    return asn_distribution


def analyze_results_nslookup_info():
    with open('result_nslookup_info.json', 'r', encoding='utf-8') as f:
        ip_info = json.load(f)

    domain_results = []  # List to store results for each domain

    for domain, ip_entries in ip_info.items():
        print(f"\nDomain: {domain}")
        if len(ip_entries) == 0:
            print("No IP entries found for this domain")
            continue
        # Calculate diversity score for the given data
        caculated_results = calculate_diversity_score(ip_entries)

        diversity_score = caculated_results['overall_diversity_score']
        asn_diversity_score = caculated_results['asn_diversity_score']
        isp_diversity_score = caculated_results['isp_diversity_score']
        lat_lng_diversity_score = caculated_results['lat_lng_diversity_score']
        country_prov_city_score = caculated_results['country_prov_city_score']
        ip_address_score = caculated_results['ip_address_score']
        unique_asns = caculated_results['unique_asns']
        unique_isps = caculated_results['unique_isps']
        unique_lat_lng = caculated_results['unique_lat_lng']
        unique_country_prov_city = caculated_results['unique_country_prov_city']

        print(f"Diversity Score: {diversity_score}")

        # Analyze ISP Distribution
        isp_distribution = analyze_isp_distribution(ip_entries)
        print("ISP Distribution:")
        for isp, count in isp_distribution.items():
            print(f"{isp}: {count}")

        # Analyze ASN Distribution
        asn_distribution = analyze_asn_distribution(ip_entries)
        print("\nASN Distribution:")
        for asn, count in asn_distribution.items():
            print(f"{asn}: {count}")

        # Store results for the current domain
        domain_results.append({
            'domain': domain,
            'diversity_score': diversity_score,
            'isp_distribution': isp_distribution,
            'asn_distribution': asn_distribution,
            'unique_asns': unique_asns,
            'unique_isps': unique_isps,
            'unique_lat_lng': unique_lat_lng,
            'unique_country_prov_city': unique_country_prov_city,
            'ip_address_score': ip_address_score,
            'asn_diversity_score': asn_diversity_score,
            'isp_diversity_score': isp_diversity_score,
            'lat_lng_diversity_score': lat_lng_diversity_score,
            'country_prov_city_score': country_prov_city_score,
        })
    print(domain_results)
    # Save all results to a file (e.g., analysis_results.json)
    with open('domain_ip_analysis_results.json', 'w', encoding='utf-8') as results_file:
        json.dump(domain_results, results_file, ensure_ascii=False, indent=2)


def plot_figure():
    # Specify the font properties with SimHei
    font_properties = FontProperties(fname="../SimHei.ttf")

    with open('domain_ip_analysis_results.json', 'r', encoding='utf-8') as f:
        domain_results = json.load(f)

    # Aggregate overall statistics
    overall_diversity_scores = []
    overall_ip_address_scores = []  # To store ip_address_score values
    overall_unique_lat_lng_sizes = []  # To store sizes of unique_lat_lng sets
    overall_unique_country_prov_city_sizes = []  # To store sizes of unique_country_prov_city sets

    overall_isp_distribution = {}
    overall_asn_distribution = {}

    for result in domain_results:
        overall_diversity_scores.append(result['diversity_score'])

        # Aggregate ISP distribution
        for isp, count in result['isp_distribution'].items():
            overall_isp_distribution[isp] = overall_isp_distribution.get(isp, 0) + count

        # Aggregate ASN distribution
        for asn, count in result['asn_distribution'].items():
            overall_asn_distribution[asn] = overall_asn_distribution.get(asn, 0) + count

        # Aggregate ip_address_score values
        overall_ip_address_scores.append(result['ip_address_score'])

        # Aggregate sizes of unique_lat_lng and unique_country_prov_city sets
        overall_unique_lat_lng_sizes.append(len(result['unique_lat_lng']))
        overall_unique_country_prov_city_sizes.append(len(result['unique_country_prov_city']))

    data_en = {'China Mobile': 6696, 'China E-Government Network': 21, 'Tencent': 8, 'CERNET': 2,
               'Ministry of Science and Technology Information Center': 3, 'China Unicom': 3138, 'China Telecom': 5129,
               'Alibaba Cloud': 621, 'National Network Exchange Center': 50, 'Vnet Group, Inc.': 1,
               'CSTNET': 32, 'CASS': 2, 'Dr. Peng': 2,
               'Shanghai Information Network Co., Ltd.': 1,
               'CETC': 58,
               'Huawei': 36, 'China Cultural Relics Information Consulting Center': 1,
               'Beijing Fortune Public Information Platform': 5, 'State Information Center': 29, 'Sharktech': 1,
               'UCLOUD INFORMATION TECHNOLOGY (HK) LIMITED': 1, 'Baidu': 6,
               'Ucloud Technology Co.,ltd.': 1,
               '': 6, 'GUANGDONG WEIYI NETWORK TECHNOLOGY CO., LTD.': 1,
               'Shaanxi Broadcast&Tv Network Intermediary(Group)Co.,ltd.': 4,
               'DingFeng XinHui (Hongkong) Technology Limited': 1}

    # Plot overall ISP distribution for the top 10 ISPs
    top_isps = dict(sorted(data_en.items(), key=lambda x: x[1], reverse=True)[:10])
    top_asns = dict(sorted(overall_asn_distribution.items(), key=lambda x: x[1], reverse=True)[:10])

    # Function to convert counts to percentages
    def counts_to_percentages(counts):
        total = sum(counts.values())
        percentages = {key: (value / total) * 100 for key, value in counts.items()}
        return percentages

    def counts_to_percentage(top_counts, overall_counts):
        total_top = sum(top_counts.values())
        total_overall = sum(overall_counts.values())

        percentages = {key: (value / total_overall) * 100 for key, value in top_counts.items()}
        return percentages

    percentages_top_isps = counts_to_percentage(top_isps, overall_isp_distribution)
    unique_country_prov_city_sizes_int = [int(size) for size in overall_unique_country_prov_city_sizes]
    unique_country_prov_city_counts = {size: unique_country_prov_city_sizes_int.count(size) for size in
                                       set(unique_country_prov_city_sizes_int)}
    percentages_country_prov_city = counts_to_percentages(unique_country_prov_city_counts)
    percentages_top_asns = counts_to_percentage(top_asns, overall_asn_distribution)

    global_size = 18
    # Set DPI to 500
    plt.rcParams['figure.dpi'] = 500
    # Set font size
    plt.rcParams['font.size'] = global_size

    # Define the provided color palette
    custom_colors = ["#2878b5", "#9ac9db", "#f8ac8c", "#c82423", "#ff8884", "#8ECFC9", "#FFBE7A",
                     "#FA7F6F", "#82B0D2", "#BEB8DC", "#E7DAD2", "#F27970", "#BB9727", "#54B345",
                     "#32B897", "#05B9E2", "#8983BF", "#C76DA2", "#A1A9D0", "#F0988C", "#B883D4",
                     "#9E9E9E", "#CFEAF1", "#C4A5DE", "#F6CAE5", "#96CCCB"]

    # Use a more diverse color palette
    sns.set_palette(custom_colors)
    #
    # Plot histogram of overall diversity scores with multiple colors
    plt.figure(figsize=(10, 6), dpi=500)
    hist, bins, _ = plt.hist(overall_diversity_scores, bins=10, edgecolor='black', density=False)
    # Iterate through bars and assign different colors
    for i, patch in enumerate(plt.gca().patches):
        plt.setp(patch, 'facecolor', custom_colors[(i + 1) % len(custom_colors)])

    plt.xlabel('Diversity Score', fontproperties=font_properties, fontsize=global_size)  # Increase font size
    plt.ylabel('Percentage', fontproperties=font_properties, fontsize=global_size)  # Increase font size
    plt.xticks(bins, fontsize=global_size)  # Increase font size
    # Adding specific value labels
    total = 0
    for i, number in enumerate(hist):
        total += number
    print(total)
    for i, percent in enumerate(hist):
        plt.text(bins[i] + 0.5 * (bins[1] - bins[0]), percent, f'{(percent / total) * 100:.2f}%', ha='center',
                 va='bottom',
                 fontsize=global_size)  # Increase font size

    plt.tight_layout()
    plt.show()

    # Plot histogram of ip_address_score values with percentages
    plt.figure(figsize=(10, 6), dpi=500)
    hist, bins, _ = plt.hist(overall_ip_address_scores, bins=10, edgecolor='black',
                             density=False)
    for i, patch in enumerate(plt.gca().patches):
        plt.setp(patch, 'facecolor', custom_colors[(i + 2) % len(custom_colors)])
    plt.xlabel('IP Address Score', fontproperties=font_properties, fontsize=global_size)
    plt.ylabel('Percentage', fontproperties=font_properties, fontsize=global_size)
    plt.xticks(bins, fontsize=global_size)  # Set the x-axis ticks to match the bin edges
    total = 0
    for i, number in enumerate(hist):
        total += number
    print(total)
    # Adding specific value labels
    for i, percent in enumerate(hist):
        plt.text(bins[i] + 0.5 * (bins[1] - bins[0]), percent, f'{(percent / total) * 100:.2f}%', ha='center',
                 va='bottom', fontsize=global_size)

    plt.tight_layout()
    plt.show()


    plt.figure(figsize=(10, 6), dpi=500)
    plt.bar(percentages_country_prov_city.keys(), percentages_country_prov_city.values(), edgecolor='black')
    plt.xlabel('Number of different cities where the server is deployed', fontproperties=font_properties,
               fontsize=global_size)
    plt.ylabel('Percentage', fontproperties=font_properties, fontsize=global_size)
    # Set explicit x-axis ticks based on your data range
    plt.xticks(range(min(percentages_country_prov_city.keys()), max(percentages_country_prov_city.keys()) + 1),
               fontsize=global_size)
    for i, patch in enumerate(plt.gca().patches):
        plt.setp(patch, 'facecolor', custom_colors[(i + 4) % len(custom_colors)])
    # Adding specific value labels
    for size, percent in percentages_country_prov_city.items():
        plt.text(size, percent, f'{percent:.2f}%', ha='center', va='bottom', fontsize=global_size)
    plt.tight_layout()
    plt.show()

    # # For the histogram of sizes of unique_lat_lng sets
    # plt.figure(figsize=(10, 6), dpi=500)
    # unique_lat_lng_sizes_int = [int(size) for size in overall_unique_lat_lng_sizes]
    # unique_lat_lng_counts = {size: unique_lat_lng_sizes_int.count(size) for size in set(unique_lat_lng_sizes_int)}
    # percentages = counts_to_percentages(unique_lat_lng_counts)
    # plt.bar(percentages.keys(), percentages.values(), edgecolor='black')
    # plt.xlabel('The number of geographical locations of the server', fontproperties=font_properties)
    # plt.ylabel('Percentage', fontproperties=font_properties)
    #
    # # Set explicit x-axis ticks based on your data range
    # plt.xticks(range(min(percentages.keys()), max(percentages.keys()) + 1))
    #
    # for i, patch in enumerate(plt.gca().patches):
    #     plt.setp(patch, 'facecolor', custom_colors[(i + 3) % len(custom_colors)])
    #
    # # Adding specific value labels
    # for size, percent in percentages.items():
    #     plt.text(size, percent, f'{percent:.2f}%', ha='center', va='bottom')
    #
    # plt.tight_layout()
    # plt.show()
    # For the histogram of sizes of unique_country_prov_city sets

    # Plot top 10 ASNs in Overall Distribution with percentages
    plt.figure(figsize=(12, 6), dpi=500)
    plt.bar(percentages_top_asns.keys(), percentages_top_asns.values())
    plt.xlabel('ASN', fontproperties=font_properties, fontsize=global_size)
    plt.ylabel('Percentage', fontproperties=font_properties, fontsize=global_size)
    plt.xticks(rotation=45, fontproperties=font_properties, fontsize=global_size)
    for i, patch in enumerate(plt.gca().patches):
        plt.setp(patch, 'facecolor', custom_colors[(i + 2) % len(custom_colors)])
    # Add values on top of the bars
    for asn, percent in percentages_top_asns.items():
        plt.text(asn, percent, f'{percent:.2f}%', ha='center', va='bottom', fontsize=global_size)

    plt.tight_layout()
    plt.show()
    # Plot top 10 ASNs in Overall Distribution with percentages

    # Plot top 10 ISPs in Overall Distribution with percentages
    plt.figure(figsize=(12, 6), dpi=500)
    plt.barh(list(percentages_top_isps.keys()), list(percentages_top_isps.values()))  # Change bar to barh
    plt.ylabel('ISP', fontproperties=font_properties, fontsize=global_size)  # Swap x and y labels
    plt.xlabel('Percentage', fontproperties=font_properties, fontsize=global_size)  # Swap x and y labels
    plt.yticks(rotation=0, fontproperties=font_properties, fontsize=global_size)  # Rotate y-axis ticks
    for i, patch in enumerate(plt.gca().patches):
        plt.setp(patch, 'facecolor', custom_colors[(i + 3) % len(custom_colors)])
    # Add values on the right side of the bars
    for isp, percent in percentages_top_isps.items():
        plt.text(percent, isp, f'{percent:.2f}%', ha='left', va='center', fontsize=global_size)

    plt.tight_layout()
    plt.show()
    # plt.figure(figsize=(12, 6), dpi=500)
    # percentages_top_isps = counts_to_percentage(top_isps, overall_isp_distribution)
    # plt.bar(percentages_top_isps.keys(), percentages_top_isps.values())
    # plt.xlabel('ISP', fontproperties=font_properties, fontsize=global_size)
    # plt.ylabel('Percentage', fontproperties=font_properties, fontsize=global_size)
    # plt.xticks(rotation=90, fontproperties=font_properties, fontsize=global_size)
    # for i, patch in enumerate(plt.gca().patches):
    #     plt.setp(patch, 'facecolor', custom_colors[(i + 3) % len(custom_colors)])
    # # Add values on top of the bars
    # for isp, percent in percentages_top_isps.items():
    #     plt.text(isp, percent, f'{percent:.2f}%', ha='center', va='bottom', fontsize=global_size)
    #
    # plt.tight_layout()
    # plt.show()
    # Plot top 10 ISPs in Overall Distribution with percentages




    # # Create a figure with subplots
    # fig1, axs = plt.subplots(2, 2, figsize=(20, 12), dpi=500)
    #
    # # Plot 1: Histogram of overall diversity scores
    # axs[0, 0].hist(overall_diversity_scores, bins=10, edgecolor='black', density=False)
    # axs[0, 0].set_title('Overall Diversity Scores', fontsize=global_size)
    # axs[0, 0].set_xlabel('Diversity Score', fontsize=global_size)
    # axs[0, 0].set_ylabel('Percentage', fontsize=global_size)
    #
    # # Plot 2: Histogram of IP address scores
    # axs[0, 1].hist(overall_ip_address_scores, bins=10, edgecolor='black', density=False)
    # axs[0, 1].set_title('IP Address Scores', fontsize=global_size)
    # axs[0, 1].set_xlabel('IP Address Score', fontsize=global_size)
    # axs[0, 1].set_ylabel('Percentage', fontsize=global_size)
    #
    # # Plot 3: Bar chart of the number of different cities
    # axs[1, 0].bar(percentages_country_prov_city.keys(), percentages_country_prov_city.values(), edgecolor='black')
    # axs[1, 0].set_title('Number of Different Cities', fontsize=global_size)
    # axs[1, 0].set_xlabel('Number of Cities', fontsize=global_size)
    # axs[1, 0].set_ylabel('Percentage', fontsize=global_size)
    #
    # # Plot 4: Bar chart of top 10 ASNs
    # axs[1, 1].bar(percentages_top_asns.keys(), percentages_top_asns.values())
    # axs[1, 1].set_title('Top 10 ASNs', fontsize=global_size)
    # axs[1, 1].set_xlabel('ASN', fontsize=global_size)
    # axs[1, 1].set_ylabel('Percentage', fontsize=global_size)
    #
    # # Add numbering to subplots
    # for i, ax in enumerate(axs.flat):
    #     ax.text(0.5, 1.02, f'({chr(97 + i)})', transform=ax.transAxes, fontsize=global_size + 2, va='center',
    #             ha='center')
    #
    # # Adjust layout
    # plt.tight_layout()
    # plt.show()

if __name__ == '__main__':
    # generate_result_nslookup_info()
    # analyze_results_nslookup_info()
    plot_figure()

