import json
import subprocess
import re


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


if __name__ == "__main__":
    file_path = "./analysis/namerserver_ip.json"
    json_data = read_json_file(file_path)
    dns_servers = extract_ips(json_data)

    # Replace 'credit.wenzhou.gov.cn' with the actual domain you want to test
    domain_to_test = 'credit.wenzhou.gov.cn'

    results = []

    for dns_server in dns_servers:
        result = test_dnssec_support(domain_to_test, dns_server)
        results.append(result)

    # Write results to JSON file
    output_file_path = "./analysis/dnssec_results.json"
    with open(output_file_path, 'w') as output_file:
        json.dump(results, output_file, indent=2)

    print(f"Results written to {output_file_path}")
