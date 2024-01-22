import json

import matplotlib.pyplot as plt
import pandas as pd


def analye_nslookup_domain_and_ips():
    data = {1: 607, 2: 9433, 3: 1509, 4: 1691, 5: 84, 6: 102, 7: 56, 8: 184, 9: 44, 10: 11, 12: 94, 15: 1, 18: 1, 19: 2,
            20: 1, 22: 1}

    # Create a DataFrame
    df = pd.DataFrame(list(data.items()), columns=['Server Numbers', 'Domain Counts'])

    # Calculate percentage
    total_domains = df['Domain Counts'].sum()
    df['Percentage'] = (df['Domain Counts'] / total_domains) * 100

    # Define a custom sci-fi style color palette
    sci_fi_palette = ['#00FFD4', '#FF00FF', '#FFA500', '#800080', '#00CED1', '#FF6347', '#4B0082', '#7FFFD4', '#8A2BE2',
                      '#00FA9A', '#FFD700', '#FF4500', '#9932CC', '#FF1493', '#7FFF00', '#20B2AA']

    # Plotting using Matplotlib bar chart with percentages and sci-fi style color palette
    fig, ax1 = plt.subplots(figsize=(10, 6), dpi=500)
    bars = ax1.bar(df['Server Numbers'], df['Domain Counts'], color=sci_fi_palette, width=1.0, )

    # Add labels and title
    ax1.set_xlabel('Server Numbers')
    ax1.set_ylabel('Domain Counts', color='black')
    # ax1.set_title('Distribution of Domain Counts across Server Numbers')

    # Rotate x-axis labels for better readability
    ax1.set_xticks(df['Server Numbers'])
    ax1.set_xticklabels(df['Server Numbers'], rotation=45, ha='right')

    # Create a second y-axis for percentages
    ax2 = ax1.twinx()
    ax2.set_ylabel('Percentage', color='black')
    ax2.set_ylim(0, 100)

    # Add percentages on top of the bars
    for bar, percentage in zip(bars, df['Percentage']):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2, height, f'{percentage:.2f}%', ha='center', va='bottom',
                 color='black', fontsize=8)

    plt.savefig('cdn_distribution_sci.png', dpi=500)
    # Show the plot
    plt.show()


def is_ipv4(ip):
    return ip.count('.') == 3


def is_ipv6(ip):
    return ip.count(':') == 7


def analyze_4_and_6():
    with open('./nslookup_info.json', 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    ipv4_count = 0
    ipv6_count = 0
    for record in json_data:
        addresses = record['Addresses']
        for address in addresses:
            if is_ipv4(address):
                ipv4_count += 1
            if is_ipv6(address):
                ipv6_count += 1
                break
    print(ipv4_count)
    print(ipv6_count)


analyze_4_and_6()