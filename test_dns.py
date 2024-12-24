# import json
# import subprocess
# import re
#
#
# def read_json_file(file_path):
#     with open(file_path, 'r') as file:
#         data = json.load(file)
#     return data
#
#
# def extract_ips(data):
#     ips = set()
#     for entry in data:
#         ips.update(entry.get('ips', []))
#     return ips
#
#
# def test_dnssec_support(domain, dns_server):
#     try:
#         # Run dig command
#         command = f"dig +dnssec {domain} @{dns_server}"
#         result = subprocess.run(command, shell=True, capture_output=True, text=True)
#
#         # Check for RRSIG in the output
#         dnssec_supported = bool(re.search(r'\bRRSIG\b', result.stdout))
#         print(f"{domain} on {dns_server} supports DNSSEC: {dnssec_supported}")
#         return {"dns_server": dns_server, "domain": domain, "dnssec_supported": dnssec_supported}
#
#     except Exception as e:
#         return {"dns_server": dns_server, "domain": domain, "error": str(e)}
#
#
# if __name__ == "__main__":
#     file_path = "./analysis/namerserver_ip.json"
#     json_data = read_json_file(file_path)
#     dns_servers = extract_ips(json_data)
#
#     # Domains to test
#     domains_to_test = [
#         ('dxs.sg.gov.cn', 'CNAME'), ('water.sg.gov.cn', 'CNAME'), ('jy.sg.gov.cn', 'CNAME'),
#         ('rsj.sg.gov.cn', 'CNAME'), ('zgj.sg.gov.cn', 'CNAME'), ('www.sg.gov.cn', 'CNAME'),
#         ('gxq.sg.gov.cn', 'CNAME'), ('gjj.sg.gov.cn', 'CNAME'), ('credit.sg.gov.cn', 'CNAME'),
#         ('www.ruyuan.gov.cn', 'CNAME'), ('www.ziyuan.gov.cn', 'A'), ('wzmz.wenzhou.gov.cn', 'CNAME'),
#         ('zwfwj.wenzhou.gov.cn', 'CNAME'), ('www.wenzhou.gov.cn', 'CNAME'), ('nyncj.wenzhou.gov.cn', 'CNAME'),
#         ('wzkj.wenzhou.gov.cn', 'CNAME'), ('zfgjj.wenzhou.gov.cn', 'CNAME'), ('wzjt.wenzhou.gov.cn', 'CNAME'),
#         ('sthjj.wenzhou.gov.cn', 'CNAME'), ('lscbj.wenzhou.gov.cn', 'CNAME'), ('wzsl.wenzhou.gov.cn', 'CNAME'),
#         ('ojk.wenzhou.gov.cn', 'CNAME'), ('wztjj.wenzhou.gov.cn', 'CNAME'), ('wzsj.wenzhou.gov.cn', 'CNAME'),
#         ('wzmsa.wenzhou.gov.cn', 'CNAME'), ('ftec.wenzhou.gov.cn', 'CNAME'), ('wzgzw.wenzhou.gov.cn', 'CNAME'),
#         ('wzga.wenzhou.gov.cn', 'CNAME'), ('gxs.wenzhou.gov.cn', 'CNAME'), ('zjj.wenzhou.gov.cn', 'CNAME'),
#         ('yds.wenzhou.gov.cn', 'CNAME'), ('wzjgswj.wenzhou.gov.cn', 'CNAME'), ('wzjrb.wenzhou.gov.cn', 'CNAME'),
#         ('czj.wenzhou.gov.cn', 'CNAME'), ('wzzhzfj.wenzhou.gov.cn', 'CNAME'), ('wjw.wenzhou.gov.cn', 'CNAME'),
#         ('hrss.wenzhou.gov.cn', 'CNAME'), ('wzstyj.wenzhou.gov.cn', 'CNAME'), ('tzcjj.wenzhou.gov.cn', 'CNAME'),
#         ('yjglj.wenzhou.gov.cn', 'CNAME'), ('zrzyj.wenzhou.gov.cn', 'CNAME'), ('wl.wenzhou.gov.cn', 'CNAME'),
#         ('mzzj.wenzhou.gov.cn', 'CNAME'), ('wzrf.wenzhou.gov.cn', 'CNAME'), ('wzjxj.wenzhou.gov.cn', 'CNAME'),
#         ('fao.wenzhou.gov.cn', 'CNAME'), ('wzjj.wenzhou.gov.cn', 'CNAME'), ('sifa.wenzhou.gov.cn', 'CNAME'),
#         ('wzfgw.wenzhou.gov.cn', 'CNAME'), ('sty.wenzhou.gov.cn', 'CNAME'), ('edu.wenzhou.gov.cn', 'CNAME'),
#         ('ybj.wenzhou.gov.cn', 'CNAME'), ('dsjj.wenzhou.gov.cn', 'CNAME'), ('wztyjr.wenzhou.gov.cn', 'CNAME'),
#         ('ggzyjy-eweb.wenzhou.gov.cn', 'CNAME'), ('credit.wenzhou.gov.cn', 'CNAME'), ('www.zjhy.gov.cn', 'CNAME'),
#         ('www.shiyan.gov.cn', 'A'), ('wjw.shiyan.gov.cn', 'A'), ('njj.shiyan.gov.cn', 'A'),
#         ('gzw.shiyan.gov.cn', 'A'), ('cgzf.shiyan.gov.cn', 'A'), ('yjglj.shiyan.gov.cn', 'A'),
#         ('keji.shiyan.gov.cn', 'A'), ('zwfw.shiyan.gov.cn', 'A'), ('ggzyjy.shiyan.gov.cn', 'A'),
#         ('wsjsjd.shiyan.gov.cn', 'A'), ('zjj.shiyan.gov.cn', 'A'), ('gaj.shiyan.gov.cn', 'A'),
#         ('gtzy.shiyan.gov.cn', 'A'), ('sc.shiyan.gov.cn', 'A'), ('xczx.shiyan.gov.cn', 'A'),
#         ('gjj.shiyan.gov.cn', 'A'), ('forestry.shiyan.gov.cn', 'A'), ('wlj.shiyan.gov.cn', 'A'),
#         ('nyj.shiyan.gov.cn', 'A'), ('fgw.shiyan.gov.cn', 'A'), ('mzj.shiyan.gov.cn', 'A'),
#         ('jgswj.shiyan.gov.cn', 'A'), ('jgj.shiyan.gov.cn', 'A'), ('czj.shiyan.gov.cn', 'A'),
#         ('sthjj.shiyan.gov.cn', 'A'), ('slj.shiyan.gov.cn', 'A'), ('jxw.shiyan.gov.cn', 'A'),
#         ('swj.shiyan.gov.cn', 'A'), ('sfj.shiyan.gov.cn', 'A'), ('xmsy.shiyan.gov.cn', 'A'),
#         ('sjj.shiyan.gov.cn', 'A'), ('tjj.shiyan.gov.cn', 'A'), ('jtys.shiyan.gov.cn', 'A'),
#         ('jyj.shiyan.gov.cn', 'A'), ('gxs.shiyan.gov.cn', 'A'), ('rsj.shiyan.gov.cn', 'A'),
#         ('rfb.shiyan.gov.cn', 'A'), ('zsj.shiyan.gov.cn', 'A'), ('tyjrswj.shiyan.gov.cn', 'A'),
#         ('scjg.shiyan.gov.cn', 'A'), ('ybj.shiyan.gov.cn', 'A'), ('maojian.shiyan.gov.cn', 'A'),
#         ('yunyang.shiyan.gov.cn', 'A'), ('www.cili.gov.cn', 'A')
#     ]
#
#     results = []
#
#     for domain, _ in domains_to_test:
#         for dns_server in dns_servers:
#             result = test_dnssec_support(domain, dns_server)
#             results.append(result)
#
#     # Write results to JSON file
#     output_file_path = "./analysis/dnssec_results.json"
#     with open(output_file_path, 'w') as output_file:
#         json.dump(results, output_file, indent=2)
#
#     print(f"Results written to {output_file_path}")
#
#
# # 读取 JSON 文件
# with open("./analysis/dnssec_results.json", "r") as file:
#     results = json.load(file)
#
# # 统计支持 DNSSEC 的结果数量
# dnssec_supported_count = sum(1 for result in results if result["dnssec_supported"])
#
# print("支持 DNSSEC 的结果数量:", dnssec_supported_count)
import concurrent
import json
import subprocess
import re
from concurrent.futures import ThreadPoolExecutor


def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def extract_ips(data):
    ips = set()
    for entry in data:
        ips.update(entry.get('ips', []))
    return ips


def test_dnssec_support(domain, dns_server):
    try:
        # Run dig command
        command = f"dig +dnssec {domain} @{dns_server}"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        # Check for RRSIG in the output
        dnssec_supported = bool(re.search(r'\bRRSIG\b', result.stdout))
        print(f"{domain} on {dns_server} supports DNSSEC: {dnssec_supported}")
        return {"dns_server": dns_server, "domain": domain, "dnssec_supported": dnssec_supported}

    except Exception as e:
        return {"dns_server": dns_server, "domain": domain, "error": str(e)}


# if __name__ == "__main__":
#     file_path = "./analysis/namerserver_ip.json"
#     json_data = read_json_file(file_path)
#     dns_servers = extract_ips(json_data)
#
#     # Domains to test
#     domains_to_test = [
#         ('dxs.sg.gov.cn', 'CNAME'), ('water.sg.gov.cn', 'CNAME'), ('jy.sg.gov.cn', 'CNAME'),
#         ('rsj.sg.gov.cn', 'CNAME'), ('zgj.sg.gov.cn', 'CNAME'), ('www.sg.gov.cn', 'CNAME'),
#         ('gxq.sg.gov.cn', 'CNAME'), ('gjj.sg.gov.cn', 'CNAME'), ('credit.sg.gov.cn', 'CNAME'),
#         ('www.ruyuan.gov.cn', 'CNAME'), ('www.ziyuan.gov.cn', 'A'), ('wzmz.wenzhou.gov.cn', 'CNAME'),
#         ('zwfwj.wenzhou.gov.cn', 'CNAME'), ('www.wenzhou.gov.cn', 'CNAME'), ('nyncj.wenzhou.gov.cn', 'CNAME'),
#         ('wzkj.wenzhou.gov.cn', 'CNAME'), ('zfgjj.wenzhou.gov.cn', 'CNAME'), ('wzjt.wenzhou.gov.cn', 'CNAME'),
#         ('sthjj.wenzhou.gov.cn', 'CNAME'), ('lscbj.wenzhou.gov.cn', 'CNAME'), ('wzsl.wenzhou.gov.cn', 'CNAME'),
#         ('ojk.wenzhou.gov.cn', 'CNAME'), ('wztjj.wenzhou.gov.cn', 'CNAME'), ('wzsj.wenzhou.gov.cn', 'CNAME'),
#         ('wzmsa.wenzhou.gov.cn', 'CNAME'), ('ftec.wenzhou.gov.cn', 'CNAME'), ('wzgzw.wenzhou.gov.cn', 'CNAME'),
#         ('wzga.wenzhou.gov.cn', 'CNAME'), ('gxs.wenzhou.gov.cn', 'CNAME'), ('zjj.wenzhou.gov.cn', 'CNAME'),
#         ('yds.wenzhou.gov.cn', 'CNAME'), ('wzjgswj.wenzhou.gov.cn', 'CNAME'), ('wzjrb.wenzhou.gov.cn', 'CNAME'),
#         ('czj.wenzhou.gov.cn', 'CNAME'), ('wzzhzfj.wenzhou.gov.cn', 'CNAME'), ('wjw.wenzhou.gov.cn', 'CNAME'),
#         ('hrss.wenzhou.gov.cn', 'CNAME'), ('wzstyj.wenzhou.gov.cn', 'CNAME'), ('tzcjj.wenzhou.gov.cn', 'CNAME'),
#         ('yjglj.wenzhou.gov.cn', 'CNAME'), ('zrzyj.wenzhou.gov.cn', 'CNAME'), ('wl.wenzhou.gov.cn', 'CNAME'),
#         ('mzzj.wenzhou.gov.cn', 'CNAME'), ('wzrf.wenzhou.gov.cn', 'CNAME'), ('wzjxj.wenzhou.gov.cn', 'CNAME'),
#         ('fao.wenzhou.gov.cn', 'CNAME'), ('wzjj.wenzhou.gov.cn', 'CNAME'), ('sifa.wenzhou.gov.cn', 'CNAME'),
#         ('wzfgw.wenzhou.gov.cn', 'CNAME'), ('sty.wenzhou.gov.cn', 'CNAME'), ('edu.wenzhou.gov.cn', 'CNAME'),
#         ('ybj.wenzhou.gov.cn', 'CNAME'), ('dsjj.wenzhou.gov.cn', 'CNAME'), ('wztyjr.wenzhou.gov.cn', 'CNAME'),
#         ('ggzyjy-eweb.wenzhou.gov.cn', 'CNAME'), ('credit.wenzhou.gov.cn', 'CNAME'), ('www.zjhy.gov.cn', 'CNAME'),
#         ('www.shiyan.gov.cn', 'A'), ('wjw.shiyan.gov.cn', 'A'), ('njj.shiyan.gov.cn', 'A'),
#         ('gzw.shiyan.gov.cn', 'A'), ('cgzf.shiyan.gov.cn', 'A'), ('yjglj.shiyan.gov.cn', 'A'),
#         ('keji.shiyan.gov.cn', 'A'), ('zwfw.shiyan.gov.cn', 'A'), ('ggzyjy.shiyan.gov.cn', 'A'),
#         ('wsjsjd.shiyan.gov.cn', 'A'), ('zjj.shiyan.gov.cn', 'A'), ('gaj.shiyan.gov.cn', 'A'),
#         ('gtzy.shiyan.gov.cn', 'A'), ('sc.shiyan.gov.cn', 'A'), ('xczx.shiyan.gov.cn', 'A'),
#         ('gjj.shiyan.gov.cn', 'A'), ('forestry.shiyan.gov.cn', 'A'), ('wlj.shiyan.gov.cn', 'A'),
#         ('nyj.shiyan.gov.cn', 'A'), ('fgw.shiyan.gov.cn', 'A'), ('mzj.shiyan.gov.cn', 'A'),
#         ('jgswj.shiyan.gov.cn', 'A'), ('jgj.shiyan.gov.cn', 'A'), ('czj.shiyan.gov.cn', 'A'),
#         ('sthjj.shiyan.gov.cn', 'A'), ('slj.shiyan.gov.cn', 'A'), ('jxw.shiyan.gov.cn', 'A'),
#         ('swj.shiyan.gov.cn', 'A'), ('sfj.shiyan.gov.cn', 'A'), ('xmsy.shiyan.gov.cn', 'A'),
#         ('sjj.shiyan.gov.cn', 'A'), ('tjj.shiyan.gov.cn', 'A'), ('jtys.shiyan.gov.cn', 'A'),
#         ('jyj.shiyan.gov.cn', 'A'), ('gxs.shiyan.gov.cn', 'A'), ('rsj.shiyan.gov.cn', 'A'),
#         ('rfb.shiyan.gov.cn', 'A'), ('zsj.shiyan.gov.cn', 'A'), ('tyjrswj.shiyan.gov.cn', 'A'),
#         ('scjg.shiyan.gov.cn', 'A'), ('ybj.shiyan.gov.cn', 'A'), ('maojian.shiyan.gov.cn', 'A'),
#         ('yunyang.shiyan.gov.cn', 'A'), ('www.cili.gov.cn', 'A')
#     ]
#
#     results = []
#
#     # 使用 ThreadPoolExecutor 并发执行 DNS 测试任务
#     with ThreadPoolExecutor() as executor:
#         future_to_domain = {executor.submit(test_dnssec_support, domain, dns_server): (domain, dns_server) for
#                             domain, _ in domains_to_test for dns_server in dns_servers}
#         for future in concurrent.futures.as_completed(future_to_domain):
#             domain, dns_server = future_to_domain[future]
#             try:
#                 result = future.result()
#                 results.append(result)
#             except Exception as e:
#                 print(f"Error occurred while testing {domain} on {dns_server}: {e}")
#
#     # Write results to JSON file
#     output_file_path = "./analysis/dnssec_results.json"
#     with open(output_file_path, 'w') as output_file:
#         json.dump(results, output_file, indent=2)
#
#     print(f"Results written to {output_file_path}")
#
#     # 统计支持 DNSSEC 的结果数量
#     dnssec_supported_count = sum(1 for result in results if result["dnssec_supported"])
#
#     print("支持 DNSSEC 的结果数量:", dnssec_supported_count)

def read_dnssec_results(file_path):
    with open(file_path, 'r') as file:
        results = json.load(file)
    return results


if __name__ == "__main__":
    dnssec_results = read_dnssec_results("./analysis/dnssec_results.json")
    dnssec_support_dict = {}  # Dictionary to store DNSSEC support for each server

    for result in dnssec_results:
        dns_server = result["dns_server"]
        domain = result["domain"]
        dnssec_supported = result["dnssec_supported"]

        if dns_server not in dnssec_support_dict:
            dnssec_support_dict[dns_server] = dnssec_supported
        elif not dnssec_support_dict[dns_server]:
            # If DNSSEC support is already True for this server, no need to recompute
            if dnssec_supported:
                dnssec_support_dict[dns_server] = True

    # 统计支持 DNSSEC 的结果数量
    dnssec_supported_count = sum(1 for supported in dnssec_support_dict.values() if supported)

    print("支持 DNSSEC 的结果数量:", dnssec_supported_count)
