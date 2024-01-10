import os
import ssl
import socket
from urllib.parse import urlparse
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

import socket
import ssl


def test_tls_version(host, port=443):
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    print(f"Testing TLS version for {host}")
    try:
        with socket.create_connection((host, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                tls_version = ssock.version()
                print(f"{host} is using TLS version {tls_version}")
                return tls_version
    except socket.gaierror as e:
        print(f"Error connecting to {host}: {e}")
    except ssl.SSLError as e:
        print(f"Error establishing TLS connection to {host}: {e}")
    except socket.error as e:
        print(f"Error resolving {host}: {e}")
    except Exception as e:
        print(f"Error connecting to {host}: {e}")


def extract_domain_from_line(line):
    url_info = urlparse(line.strip())
    return url_info.netloc


def process_file(file_path, province_tls_versions):
    with open(file_path, "r") as file:
        lines = file.readlines()
    for line in lines:
        domain = extract_domain_from_line(line)
        province = domain.split(".")[-1]
        tls_version = test_tls_version(domain)

        if province not in province_tls_versions:
            province_tls_versions[province] = {}

        if tls_version not in province_tls_versions[province]:
            province_tls_versions[province][tls_version] = 1
        else:
            province_tls_versions[province][tls_version] += 1


def process_directory(directory):
    province_tls_versions = {}
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        if os.path.isfile(file_path):
            process_file(file_path, province_tls_versions)

    print("Province-wise TLS Version distribution:")
    for province, tls_versions in province_tls_versions.items():
        print(f"{province}: {tls_versions}")

    print("\nOverall TLS Version distribution:")
    overall_tls_versions = {}
    for tls_versions in province_tls_versions.values():
        for version, count in tls_versions.items():
            overall_tls_versions[version] = overall_tls_versions.get(version, 0) + count

    print(overall_tls_versions)


if __name__ == "__main__":
    target_directory = "domain_txt"  # 替换为你的目标目录路径
    process_directory(target_directory)
