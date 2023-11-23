import json
import os
import socket
import ssl
import OpenSSL
import requests


def get_certificate(hostname, port=443):
    try:
        with socket.create_connection((hostname, port),timeout=5) as sock:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_OPTIONAL

            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                # 获取 DER 格式的证书
                der_cert = ssock.getpeercert(binary_form=True)
                pem_cert = ssl.DER_cert_to_PEM_cert(der_cert)
                # 加载证书
                cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, pem_cert)
                return cert, ssock.getpeercert()
    except Exception as e:
        print(f"Error fetching certificate for {hostname}: {e}")
        return None, None

def get_cert_chain(hostname, port=443):
    cert_chain = []

    # 建立 SSL/TLS 连接
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_OPTIONAL
    # 设置回调函数来保存证书链
    context.set_default_verify_paths()
    cert_chain = context.get_ca_certs()

    with socket.create_connection((hostname, port), timeout=5) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            pass  # 连接建立，证书链已保存

    return cert_chain


def get_certificate_info(cert, raw_cert):
    # 解析证书信息
    subject = cert.get_subject()
    issuer = cert.get_issuer()
    valid_from = cert.get_notBefore().decode('utf-8')
    valid_until = cert.get_notAfter().decode('utf-8')

    cert_chain = []
    for url in raw_cert.get('caIssuers', []):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_ASN1, response.content)
                cert_chain.append(x509)
        except requests.RequestException as e:
            print(f"Error fetching certificate from {url}: {e}")

    # 获取证书链的详细信息
    cert_chain_info = []
    for item in cert_chain:
        cissuer = item.get_issuer()
        csubject = item.get_subject()
        cvalid_from = item.get_notBefore().decode('utf-8')
        cvalid_until = item.get_notAfter().decode('utf-8')
        cert_chain_info.append({
            'issuer': cissuer.O,
            'subject': csubject.O or subject.CN,
            'version': item.get_version() + 1,
            'valid_from': cvalid_from,
            'valid_until': cvalid_until,
            'is_expired': item.has_expired()
        })

    return {
        'hostname': subject.CN,
        'issuer': issuer.O,
        'subject': subject.O or subject.CN,  # 使用 organizationName 或者 fallback 到 CN
        'version': cert.get_version() + 1,
        'valid_from': valid_from,
        'valid_until': valid_until,
        'cert_chain': cert_chain_info,
    }


def fetch_certificates(hostname, unit_name):
    # 创建存储证书信息的目录
    os.makedirs(f'./ca/{unit_name}', exist_ok=True)

    filename = os.path.join(f'./ca/{unit_name}', f"{hostname}.json")
    if os.path.exists(filename):
        # 如果文件已存在，不再重复获取
        return

    try:
        # 获取证书信息
        cert_info = None
        cert, raw_cert = get_certificate(hostname)
        if cert and raw_cert:
            cert_info = get_certificate_info(cert, raw_cert)
            print(cert_info)
        # 将证书信息写入 JSON 文件
        output_filename = f"./ca/{unit_name}/{hostname}.json"
        if cert_info:
            with open(output_filename, 'w', encoding='utf-8') as json_file:
                json.dump(cert_info, json_file, ensure_ascii=False, indent=4)
            print(f"Certificate information for {hostname} has been saved to {output_filename}.")

    except Exception as e:
        # 处理可能发生的错误
        error_filename = f'./ca/{unit_name}/errors.txt'
        with open(error_filename, 'a') as error_file:
            error_file.write(f"{hostname}: {str(e)}\n")
        print(f"An error occurred for {hostname}: {e}. Error written to {error_filename}.")


# 使用示例
# hostname = 'km.gov.cn'  # 替换为您想要检查的域名
# cert, raw_cert = get_certificate(hostname)
# if cert and raw_cert:
#     info = get_certificate_info(cert, raw_cert)
#     print(info)

# cert_chain = get_cert_chain(hostname)
# for cert in cert_chain:
#     print(cert)


# import os
# import socket
# import ssl
# import json
#
# def fetch_certificates(hostname, unit_name):
#     # Check if the website supports HTTPS
#     os.makedirs(f'./ca/{unit_name}', exist_ok=True)
#
#     filename = os.path.join(f'./ca/{unit_name}', f"{hostname}.json")
#     if os.path.exists(filename):
#         # If the file already exists, return
#         return
#
#     try:
#         # Send SYN on TCP port 443
#         with socket.create_connection((hostname, 443)) as s:
#             s.settimeout(5)  # Set a timeout in case the connection takes too long
#             context = ssl.create_default_context()
#             # Initiate an HTTPS connection and fetch SSL certificates
#             try:
#
#                 with context.wrap_socket(s, server_hostname=hostname) as ssock:
#                     # Get the certificate
#                     cert = ssock.getpeercert()
#                     # Get the certificate chain
#                     cert_chain = context.get_ca_certs()
#
#                     # Create a dictionary with certificate details
#                     certificate_info = {
#                         'hostname': hostname,
#                         'issuer': cert['issuer'],
#                         'subject': cert['subject'],
#                         'valid_from': cert['notBefore'],
#                         'valid_until': cert['notAfter'],
#                         'cert_chain': cert_chain,
#                     }
#                     # Get the negotiated TLS version
#                     tls_version = ssock.version()
#                     certificate_info['tls_version'] = tls_version
#
#                     # Write the certificate information to a JSON file
#                     output_filename = f"./ca/{unit_name}/{hostname}.json"
#                     with open(output_filename, 'w', encoding='utf-8') as json_file:
#                         json.dump(certificate_info, json_file, ensure_ascii=False, indent=4)
#                     print(f"Certificate information for {hostname} has been saved to {output_filename}.")
#                     print(f"The TLS version used by {hostname} is: {tls_version}")
#
#             except ssl.SSLError as e:
#                 # Write the hostname into a file within the unit_name directory
#                 error_filename = f'./ca/{unit_name}/rerror.txt'
#                 with open(error_filename, 'a') as error_file:
#                     error_file.write(hostname + "\n")
#                 print(f"An error occurred while fetching the certificate: {e}. Error written to {error_filename}.")
#
#     except (socket.timeout, socket.gaierror) as e:
#         # Write the hostname into a file within the unit_name directory
#         error_filename = f'./ca/{unit_name}/rerror.txt'
#         with open(error_filename, 'a') as error_file:
#             error_file.write(hostname + "\n")
#         print(f"The website {hostname} does not support HTTPS or cannot be reached. Error written to {error_filename}.")
#
#     except socket.error as e:
#         # Handle the socket error
#         print(f"Socket error occurred while connecting to {hostname}: {e}")
##########################################################################################
#
# def fetch_certificates(hostname, unit_name):
#     # Check if the website supports HTTPS
#     os.makedirs(f'./ca/{unit_name}', exist_ok=True)
#
#     if os.path.exists(f'./ca/{unit_name}/{hostname}.json'):
#         # If the file already exists, return
#         return
#
#     try:
#         # Send SYN on TCP port 443
#         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#             s.settimeout(10)  # Set a timeout in case the connection takes too long
#             s.connect((hostname, 443))
#     except Exception as e:
#         # Write the hostname into a file within the unit_name directory
#         error_filename = f'./ca/{unit_name}/error.txt'
#         with open(error_filename, 'a') as error_file:
#             error_file.write(hostname + "\n")
#         print(f"The website {hostname} does not support HTTPS. Error written to {error_filename}.")
#         return
#
#     # Initiate an HTTPS connection and fetch SSL certificates
#     try:
#         context = ssl.create_default_context()
#         with socket.create_connection((hostname, 443)) as sock:
#             with context.wrap_socket(sock, server_hostname=hostname) as ssock:
#                 # Get the certificate
#                 cert = ssock.getpeercert()
#                 # Create a dictionary with certificate details
#                 certificate_info = {
#                     'hostname': hostname,
#                     'issuer': cert['issuer'],
#                     'subject': cert['subject'],
#                     'valid_from': cert['notBefore'],
#                     'valid_until': cert['notAfter']
#                 }
#
#                 # Write the certificate information to a JSON file
#                 output_filename = f"./ca/{unit_name}/{hostname}.json"
#                 with open(output_filename, 'w', encoding='utf-8') as json_file:
#                     json.dump(certificate_info, json_file, ensure_ascii=False, indent=4)
#                 print(f"Certificate information for {hostname} has been saved to {output_filename}.")
#
#     except ssl.SSLError as e:
#         # Write the hostname into a file within the unit_name directory
#         with open(f'./ca/{unit_name}/error.txt', 'a') as error_file:
#             error_file.write(hostname + "\n")
#         print(f"An error occurred while fetching the certificate: {e}. Error written to ./ca/{unit_name}/error.txt.")
#

# Example usage
# fetch_certificates("www.bpf.cas.cn", "中科院")
