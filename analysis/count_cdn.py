import os


# 判断目标是否存在CDN
def detectCDN(domain):
    parm = 'nslookup ' + domain
    result = os.popen(parm).read()
    print(result)
    return result


def main():
    ####################################################################################################################
    #  Check   CDN
    ####################################################################################################################
    root_directory = '../xdns/class'
    result_list = []
    for province_directory in os.listdir(root_directory):
        province_directory_path = f"{root_directory}/{province_directory}"
        if not os.path.isdir(province_directory_path):
            continue
        cdn_count = 0
        ncdn_count = 0
        for filename in os.listdir(province_directory_path):
            if not filename.endswith('.txt'):
                continue
            domain = filename.split('.txt')[0]

            try:
                cdn_info = detectCDN(domain)
                if cdn_info.count(".") > 10:
                    print(domain + " 存在CDN")
                    cdn_count += 1
                else:
                    print(domain + " 不存在CDN")
                    ncdn_count += 1
                result_list.append(cdn_info)
            except Exception:
                print(f"Failed to run nslookup for domain: {domain}")
                with open('./failed_nslookup.txt', 'w', encoding='utf-8') as file:
                    file.write(f"{domain}\n")
                continue
        
        os.makedirs(f'./cdn/{province_directory}', exist_ok=True)

        with open(f'./cdn/{province_directory}/ip_cdn_info.txt', 'w', encoding='utf-8') as file:
            for info in result_list:
                file.write(f"{info}\n")
            file.write("\n")

            file.write(f"Province: {province_directory}")
            file.write(f"CDN count: {cdn_count}")
            file.write(f"NoneCDN count: {ncdn_count}")
        result_list = []


main()
