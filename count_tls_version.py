import json
import os
import ssl
import socket
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor

ssl._create_default_https_context = ssl._create_unverified_context


def parse_certificate_info(cert_info):
    parsed_info = {}

    # Extract subject details
    subject = cert_info.get('subject', [])
    for attr_list in subject:
        for attr, value in attr_list:
            if attr == 'countryName':
                parsed_info['Subject_Country'] = value
            elif attr == 'stateOrProvinceName':
                parsed_info['Subject_State'] = value
            elif attr == 'localityName':
                parsed_info['Subject_Locality'] = value
            elif attr == 'organizationName':
                parsed_info['Subject_Organization'] = value
            elif attr == 'commonName':
                parsed_info['Subject_CommonName'] = value

    # Extract issuer details
    issuer = cert_info.get('issuer', [])
    for attr_list in issuer:
        for attr, value in attr_list:
            if attr == 'countryName':
                parsed_info['Issuer_Country'] = value
            elif attr == 'organizationName':
                parsed_info['Issuer_Organization'] = value
            elif attr == 'commonName':
                parsed_info['Issuer_CommonName'] = value

    # Extract subjectAltName
    subject_alt_name = cert_info.get('subjectAltName', [])
    parsed_info['SubjectAltName'] = subject_alt_name[0][1] if subject_alt_name else None

    # Extract notBefore and notAfter
    parsed_info['NotBefore'] = cert_info.get('notBefore', '')
    parsed_info['NotAfter'] = cert_info.get('notAfter', '')

    return parsed_info


def extract_attr_value(attr_list, attr_name):
    for attr, value in attr_list:
        if attr == attr_name:
            return value
    return None


def test_tls_version(host, port=443):
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_OPTIONAL  # Enforce server certificate verification

    print(f"Testing TLS version for {host}")
    try:
        with socket.create_connection((host, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                tls_version = ssock.version()
                print(f"{host} is using TLS version {tls_version}")
                # Extract certificate information
                cert_info = ssock.getpeercert()
                print("Certificate Information:")
                print(cert_info)
                cipher = ssock.cipher()
                # Add debug prints
                print("Cipher: ", cipher)

                return tls_version, cert_info, cipher, host

    except socket.gaierror as e:
        print(f"Error connecting to {host}: {e}")
    except ssl.SSLError as e:
        print(f"Error establishing TLS connection to {host}: {e}")
    except socket.error as e:
        print(f"Error resolving {host}: {e}")
    except Exception as e:
        print(f"Error connecting to {host}: {e}")
    return None, None, None, host


def extract_domain_from_line(line):
    url_info = urlparse(line.strip())
    return url_info.netloc


def process_file(file_path, province, output_directory):
    province_tls_info = {}

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return province_tls_info

    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(test_tls_version, extract_domain_from_line(line)): line for line in lines}
        for future in futures:
            try:
                result = future.result()
                print(f"Processing line: {result}")

                tls_version, cert_info, cipher, host = result

                if tls_version is not None:
                    if province not in province_tls_info:
                        province_tls_info[province] = []

                    # Check if cert_info is available
                    if cert_info:
                        # Extract relevant certificate information
                        parsed_info = {}

                        # Extract subject details
                        subject = cert_info.get('subject', [])
                        for attr_list in subject:
                            attr, value = attr_list[0]
                            if attr == 'countryName':
                                parsed_info['Subject_Country'] = value
                            elif attr == 'stateOrProvinceName':
                                parsed_info['Subject_State'] = value
                            elif attr == 'localityName':
                                parsed_info['Subject_Locality'] = value
                            elif attr == 'organizationName':
                                parsed_info['Subject_Organization'] = value
                            elif attr == 'commonName':
                                parsed_info['Subject_CommonName'] = value

                        # Extract issuer details
                        issuer = cert_info.get('issuer', [])
                        for attr_list in issuer:
                            attr, value = attr_list[0]
                            if attr == 'countryName':
                                parsed_info['Issuer_Country'] = value
                            elif attr == 'organizationName':
                                parsed_info['Issuer_Organization'] = value
                            elif attr == 'commonName':
                                parsed_info['Issuer_CommonName'] = value

                        # Extract subjectAltName
                        subject_alt_name = cert_info.get('subjectAltName', [])
                        parsed_info['SubjectAltName'] = subject_alt_name[0][1] if subject_alt_name else None

                        # Extract notBefore and notAfter
                        parsed_info['NotBefore'] = cert_info.get('notBefore', '')
                        parsed_info['NotAfter'] = cert_info.get('notAfter', '')

                        tls_info = {"TLS_Version": tls_version, "Certificate_Info": parsed_info, "Cipher": cipher, "Host": host}
                        province_tls_info[province].append(tls_info)
                        print(f"TLS Info added for {province}: {tls_info}")
                    else:
                        if cipher:
                            tls_info = {"TLS_Version": tls_version, "Certificate_Info": {}, "Cipher": cipher, "Host": host}
                            province_tls_info[province].append(tls_info)
                        else:
                            tls_info = {"TLS_Version": tls_version, "Certificate_Info": {}, "Cipher": None, "Host": host}
                            print(f"TLS Info added for {province}: {tls_info}")

                else:
                    print(f"TLS version is None for line: {future.result()}")
            except Exception as e:
                print(f"Error processing line: {e}")

    # Print the final province_tls_info before writing to JSON
    print(f"Final TLS Info for {province}: {province_tls_info.get(province, [])}")

    return province_tls_info


def process_directory(directory, output_directory):
    overall_tls_info = {"Overall": []}
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        province = file_name.split(".txt")[0]
        if file_name.endswith(".txt"):
            # Check if result json file already exists
            json_filename = f"{province}_result.json"
            json_filepath = os.path.join(output_directory, json_filename)

            if os.path.exists(json_filepath):
                print(f"Skipping {json_filename} as it already exists.")
                continue

            province_tls_info = process_file(file_path, province, output_directory)

            print(f"Province-wise TLS Version and Certificate Information for {file_name}:")

            # Write results to JSON file in the specified output directory
            with open(json_filepath, 'w', encoding='utf-8') as json_file:
                json.dump(province_tls_info, json_file, ensure_ascii=False, indent=2)

            overall_tls_info["Overall"].extend(province_tls_info)
    print("\nOverall TLS Version and Certificate Information:")
    print(overall_tls_info)

    # Write overall results to JSON file in the specified output directory
    overall_json_filepath = os.path.join(output_directory, "overall_result.json")
    with open(overall_json_filepath, 'w', encoding='utf-8') as overall_json_file:
        json.dump(overall_tls_info, overall_json_file, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    target_directory = "domain_txt"  # Replace with your target directory path
    output_directory = "result"
    os.makedirs(output_directory, exist_ok=True)
    process_directory(target_directory, output_directory)
