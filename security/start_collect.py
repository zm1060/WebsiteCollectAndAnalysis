# import ssl
# import socket
# import datetime
# import json
# from urllib.parse import urlparse
#
#
# class DateTimeEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, datetime.datetime):
#             return obj.isoformat()
#         return super().default(obj)
#
#
# def extract_fields(data):
#     extracted_fields = {}
#     for entry in data:
#         for field, value in entry:
#             extracted_fields[field] = value
#     return extracted_fields
#
#
# def extract_subject_info(subject):
#     return extract_fields(subject)
#
#
# def get_certificate_info(domain, port=443):
#     try:
#         # 建立与服务器的连接
#         context = ssl.create_default_context()
#         # context.check_hostname = False
#         # context.verify_mode = ssl.CERT_OPTIONAL
#         with socket.create_connection((domain, port)) as sock:
#             with context.wrap_socket(sock, server_hostname=domain) as ssock:
#                 cert = ssock.getpeercert()
#
#         # 获取证书信息
#         issuer = cert['issuer']
#         subject = cert['subject']
#         not_before = cert['notBefore']
#         not_after = cert['notAfter']
#         sans = cert['subjectAltName']
#
#         # Accessing issuer information
#         issuer_info = extract_fields(issuer)
#
#         # Accessing subject information dynamically
#         subject_info = extract_subject_info(subject)
#
#         # Accessing validity period
#         not_before_date = not_before
#         not_after_date = not_after
#
#         # 检查证书状态
#         current_date = datetime.datetime.now()
#         not_before_date = datetime.datetime.strptime(not_before, '%b %d %H:%M:%S %Y %Z')
#         not_after_date = datetime.datetime.strptime(not_after, '%b %d %H:%M:%S %Y %Z')
#
#         certificate_status = {
#             'domain': domain,
#             'issuer': issuer_info,
#             'subject': subject_info,
#             'sans': [entry[1] for entry in sans],
#             'notBefore': not_before_date,
#             'notAfter': not_after_date,
#             'isSelfSigned': issuer == subject,
#             'isExpired': current_date > not_after_date,
#             'isMismatched': False,
#         }
#
#         print(domain.lower())
#         print(subject_info.get('commonName', '').lower())
#         return certificate_status
#
#     except Exception as e:
#         return {
#             'domain': domain,
#             'error': str(e),
#         }
#
#
# def main():
#     total_urls = []
#     with open('../total.txt', 'r', encoding='utf-8') as file:
#         total_urls = [domain.strip() for domain in file.readlines() if domain.strip()]
#     total_domains = [urlparse(url).netloc for url in total_urls]
#
#     domain_list = total_domains
#     # domain_list = ['www.ndrc.gov.cn', 'baidu.com', 'weibo.com', 'jd.com', 'www.cfstc.org', ]
#     results = []
#
#     for domain in domain_list:
#         certificate_info = get_certificate_info(domain)
#         print(certificate_info)
#         results.append(certificate_info)
#
#     # Save the results in a customized format to a JSON file
#     custom_results = []
#     for result in results:
#         custom_result = {
#             'domain': result['domain'],
#             'issuer': result['issuer'],
#             'subject': result['subject'],
#             'sans': result['sans'],
#             'notBefore': result['notBefore'],
#             'notAfter': result['notAfter'],
#             'isSelfSigned': result['isSelfSigned'],
#             'isExpired': result['isExpired'],
#             'isMismatched': result['isMismatched'],
#         }
#         custom_results.append(custom_result)
#
#     with open('certificate_results_custom.json', 'w', encoding='utf-8') as json_file:
#         json.dump(custom_results, json_file, cls=DateTimeEncoder, ensure_ascii=False, indent=2)
#
#
# if __name__ == "__main__":
#     main()
#
# # certificate verify failed: unable to get local issuer certificate
# # sslv3 alert handshake failure
# # does not support HTTPS.
# # certificate verify failed: Hostname mismatch, certificate is not valid for 'xxxx'
########################################################################################################################
#
# import asyncio
# import ssl
# import socket
# import datetime
# import json
# from urllib.parse import urlparse
#
#
# class DateTimeEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, datetime.datetime):
#             return obj.isoformat()
#         return super().default(obj)
#
#
# def extract_fields(data):
#     extracted_fields = {}
#     for entry in data:
#         for field, value in entry:
#             extracted_fields[field] = value
#     return extracted_fields
#
#
# def extract_subject_info(subject):
#     return extract_fields(subject)
#
#
# def get_certificate_info(domain, port=443):
#     try:
#         context = ssl.create_default_context()
#         with socket.create_connection((domain, port)) as sock:
#             with context.wrap_socket(sock, server_hostname=domain) as ssock:
#                 cert = ssock.getpeercert()
#
#         issuer = cert['issuer']
#         subject = cert['subject']
#         not_before = cert['notBefore']
#         not_after = cert['notAfter']
#         sans = cert['subjectAltName']
#
#         issuer_info = extract_fields(issuer)
#         subject_info = extract_subject_info(subject)
#
#         not_before_date = datetime.datetime.strptime(not_before, '%b %d %H:%M:%S %Y %Z')
#         not_after_date = datetime.datetime.strptime(not_after, '%b %d %H:%M:%S %Y %Z')
#
#         current_date = datetime.datetime.now()
#
#         certificate_status = {
#             'domain': domain,
#             'issuer': issuer_info,
#             'subject': subject_info,
#             'sans': [entry[1] for entry in sans],
#             'notBefore': not_before_date,
#             'notAfter': not_after_date,
#             'isSelfSigned': issuer == subject,
#             'isExpired': current_date > not_after_date,
#             'isMismatched': False,
#         }
#         print(certificate_status)
#         return certificate_status
#
#     except Exception as e:
#         return {
#             'domain': domain,
#             'error': str(e),
#         }
#
#
# async def get_certificate_info_async(domain, port=443):
#     loop = asyncio.get_event_loop()
#     return await loop.run_in_executor(None, get_certificate_info, domain, port)
#
#
# async def main_async():
#     total_urls = []
#     with open('../total.txt', 'r', encoding='utf-8') as file:
#         total_urls = [domain.strip() for domain in file.readlines() if domain.strip()]
#     total_domains = [urlparse(url).netloc for url in total_urls]
#
#     domain_list = total_domains
#     tasks = [get_certificate_info_async(domain) for domain in domain_list]
#     results = await asyncio.gather(*tasks)
#
#     custom_results = []
#     for result in results:
#         custom_result = {
#             'domain': result['domain'],
#             'issuer': result['issuer'],
#             'subject': result['subject'],
#             'sans': result['sans'],
#             'notBefore': result['notBefore'],
#             'notAfter': result['notAfter'],
#             'isSelfSigned': result['isSelfSigned'],
#             'isExpired': result['isExpired'],
#             'isMismatched': result['isMismatched'],
#         }
#         custom_results.append(custom_result)
#
#     with open('certificate_results_custom.json', 'w', encoding='utf-8') as json_file:
#         json.dump(custom_results, json_file, cls=DateTimeEncoder, ensure_ascii=False, indent=2)
#
#
# if __name__ == "__main__":
#     asyncio.run(main_async())
#
#
#
# import asyncio
# import ssl
# import socket
# import datetime
# import json
# from urllib.parse import urlparse
# from tqdm import tqdm
#
# class DateTimeEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, datetime.datetime):
#             return obj.isoformat()
#         return super().default(obj)
#
# def extract_fields(data):
#     extracted_fields = {}
#     for entry in data:
#         for field, value in entry:
#             extracted_fields[field] = value
#     return extracted_fields
#
# def extract_subject_info(subject):
#     return extract_fields(subject)
#
# def get_certificate_info(domain, port=443):
#     try:
#         context = ssl.create_default_context()
#         with socket.create_connection((domain, port)) as sock:
#             with context.wrap_socket(sock, server_hostname=domain) as ssock:
#                 cert = ssock.getpeercert()
#
#         issuer = cert['issuer']
#         subject = cert['subject']
#         not_before = cert['notBefore']
#         not_after = cert['notAfter']
#         sans = cert['subjectAltName']
#
#         issuer_info = extract_fields(issuer)
#         subject_info = extract_subject_info(subject)
#
#         not_before_date = datetime.datetime.strptime(not_before, '%b %d %H:%M:%S %Y %Z')
#         not_after_date = datetime.datetime.strptime(not_after, '%b %d %H:%M:%S %Y %Z')
#
#         current_date = datetime.datetime.now()
#
#         certificate_status = {
#             'domain': domain,
#             'issuer': issuer_info,
#             'subject': subject_info,
#             'sans': [entry[1] for entry in sans],
#             'notBefore': not_before_date,
#             'notAfter': not_after_date,
#             'isSelfSigned': issuer == subject,
#             'isExpired': current_date > not_after_date,
#             'isMismatched': False,
#         }
#         return certificate_status
#
#     except Exception as e:
#         return {
#             'domain': domain,
#             'error': str(e),
#         }
#
# async def get_certificate_info_async(domain, port=443):
#     loop = asyncio.get_event_loop()
#     return await loop.run_in_executor(None, get_certificate_info, domain, port)
#
# async def main_async():
#     total_urls = []
#     with open('../total.txt', 'r', encoding='utf-8') as file:
#         total_urls = [domain.strip() for domain in file.readlines() if domain.strip()]
#     total_domains = [urlparse(url).netloc for url in total_urls]
#
#     domain_list = total_domains
#     tasks = [get_certificate_info_async(domain) for domain in domain_list]
#
#     # Integrate tqdm to track progress
#     with tqdm(total=len(tasks), desc="Processing domains", unit="domain") as pbar:
#         async def track_progress(task):
#             nonlocal pbar
#             result = await task
#             pbar.update(1)
#             return result
#
#         results = await asyncio.gather(*(track_progress(task) for task in tasks))
#
#     custom_results = []
#     for result in results:
#         custom_result = {
#             'domain': result['domain'],
#             'issuer': result['issuer'],
#             'subject': result['subject'],
#             'sans': result['sans'],
#             'notBefore': result['notBefore'],
#             'notAfter': result['notAfter'],
#             'isSelfSigned': result['isSelfSigned'],
#             'isExpired': result['isExpired'],
#             'isMismatched': result['isMismatched'],
#         }
#         custom_results.append(custom_result)
#
#     with open('certificate_results_custom.json', 'w', encoding='utf-8') as json_file:
#         json.dump(custom_results, json_file, cls=DateTimeEncoder, ensure_ascii=False, indent=2)
#
# if __name__ == "__main__":
#     asyncio.run(main_async())
#
#
# import asyncio
# import ssl
# import socket
# import datetime
# import json
# from urllib.parse import urlparse
# from tqdm import tqdm
#
# class DateTimeEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, datetime.datetime):
#             return obj.isoformat()
#         return super().default(obj)
#
# def extract_fields(data):
#     extracted_fields = {}
#     for entry in data:
#         for field, value in entry:
#             extracted_fields[field] = value
#     return extracted_fields
#
# def extract_subject_info(subject):
#     return extract_fields(subject)
#
# def get_certificate_info(domain, port=443):
#     try:
#         context = ssl.create_default_context()
#         with socket.create_connection((domain, port)) as sock:
#             with context.wrap_socket(sock, server_hostname=domain) as ssock:
#                 cert = ssock.getpeercert()
#
#         issuer = cert['issuer']
#         subject = cert['subject']
#         not_before = cert['notBefore']
#         not_after = cert['notAfter']
#         sans = cert['subjectAltName']
#
#         issuer_info = extract_fields(issuer)
#         subject_info = extract_subject_info(subject)
#
#         not_before_date = datetime.datetime.strptime(not_before, '%b %d %H:%M:%S %Y %Z')
#         not_after_date = datetime.datetime.strptime(not_after, '%b %d %H:%M:%S %Y %Z')
#
#         current_date = datetime.datetime.now()
#
#         certificate_status = {
#             'domain': domain,
#             'issuer': issuer_info,
#             'subject': subject_info,
#             'sans': [entry[1] for entry in sans],
#             'notBefore': not_before_date,
#             'notAfter': not_after_date,
#             'isSelfSigned': issuer == subject,
#             'isExpired': current_date > not_after_date,
#             'isMismatched': False,
#         }
#         return certificate_status
#
#     except Exception as e:
#         return {
#             'domain': domain,
#             'error': str(e),
#         }
#
# async def get_certificate_info_async(domain, port=443):
#     loop = asyncio.get_event_loop()
#     return await loop.run_in_executor(None, get_certificate_info, domain, port)
#
# async def main_async():
#     total_urls = []
#     with open('../total.txt', 'r', encoding='utf-8') as file:
#         total_urls = [domain.strip() for domain in file.readlines() if domain.strip()]
#     total_domains = [urlparse(url).netloc for url in total_urls]
#
#     domain_list = total_domains
#     tasks = [get_certificate_info_async(domain) for domain in domain_list]
#
#     # Integrate tqdm to track progress
#     with tqdm(total=len(tasks), desc="Processing domains", unit="domain") as pbar:
#         async def track_progress(task):
#             nonlocal pbar
#             result = await task
#             pbar.update(1)
#             write_result_to_json(result)  # Write result to JSON file after processing each domain
#             return result
#
#         results = await asyncio.gather(*(track_progress(task) for task in tasks))
#
# def write_result_to_json(result):
#     custom_result = {
#         'domain': result.get('domain', ''),
#         'issuer': result.get('issuer', {}),
#         'subject': result.get('subject', {}),
#         'sans': result.get('sans', []),
#         'notBefore': result.get('notBefore', ''),
#         'notAfter': result.get('notAfter', ''),
#         'isSelfSigned': result.get('isSelfSigned', False),
#         'isExpired': result.get('isExpired', False),
#         'isMismatched': result.get('isMismatched', False),
#     }
#     print(custom_result)
#     with open('certificate_results_custom_to.json', 'a', encoding='utf-8') as json_file:
#         json.dump(custom_result, json_file, cls=DateTimeEncoder, ensure_ascii=False, indent=2)
#         json_file.write(',\n')  # Add a newline after each JSON object
#
#
# if __name__ == "__main__":
#     asyncio.run(main_async())

import os
import asyncio
import ssl
import socket
import datetime
import json
from urllib.parse import urlparse
from tqdm import tqdm


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return super().default(obj)


def extract_fields(data):
    extracted_fields = {}
    for entry in data:
        for field, value in entry:
            extracted_fields[field] = value
    return extracted_fields


def extract_subject_info(subject):
    return extract_fields(subject)


def get_certificate_info(domain, port=443):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, port)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()

        issuer = cert['issuer']
        subject = cert['subject']
        not_before = cert['notBefore']
        not_after = cert['notAfter']
        sans = cert['subjectAltName']

        issuer_info = extract_fields(issuer)
        subject_info = extract_subject_info(subject)

        not_before_date = datetime.datetime.strptime(not_before, '%b %d %H:%M:%S %Y %Z')
        not_after_date = datetime.datetime.strptime(not_after, '%b %d %H:%M:%S %Y %Z')

        current_date = datetime.datetime.now()

        certificate_status = {
            'domain': domain,
            'issuer': issuer_info,
            'subject': subject_info,
            'sans': [entry[1] for entry in sans],
            'notBefore': not_before_date,
            'notAfter': not_after_date,
            'isSelfSigned': issuer == subject,
            'isExpired': current_date > not_after_date,
            'isMismatched': False,
        }
        return certificate_status

    except Exception as e:
        return {
            'domain': domain,
            'error': str(e),
        }



async def get_certificate_info_async(domain, port=443):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, get_certificate_info, domain, port)


def get_existing_domains(filename):
    existing_domains = set()
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as existing_file:
            existing_data = json.load(existing_file)
            existing_domains = {entry['domain'] for entry in existing_data}
    return existing_domains


async def main_async():
    existing_results_file = 'certificate_results_custom.json'
    new_results_file = 'certificate_results_custom_missing.json'

    # Step 1: Get existing domains
    existing_domains = get_existing_domains(existing_results_file)

    # Step 2: Get total_urls and filter out existing domains
    total_urls = []
    with open('../total.txt', 'r', encoding='utf-8') as file:
        total_urls = [domain.strip() for domain in file.readlines() if domain.strip()]
    total_domains = [urlparse(url).netloc for url in total_urls]
    new_domains = list(set(total_domains) - existing_domains)


    print(new_domains)
    # Step 3: Create tasks only for new domains
    tasks = [get_certificate_info_async(domain) for domain in new_domains]

    # Integrate tqdm to track progress
    with tqdm(total=len(tasks), desc="Processing domains", unit="domain") as pbar:
        async def track_progress(task):
            nonlocal pbar
            result = await task
            pbar.update(1)
            write_result_to_json(result, new_results_file)  # Write result to the new file
            return result

        # Step 4: Run tasks for new domains
        results = await asyncio.gather(*(track_progress(task) for task in tasks))


def write_result_to_json(result, filename):
    custom_result = {
        'domain': result.get('domain', ''),
        'issuer': result.get('issuer', {}),
        'subject': result.get('subject', {}),
        'sans': result.get('sans', []),
        'notBefore': result.get('notBefore', ''),
        'notAfter': result.get('notAfter', ''),
        'isSelfSigned': result.get('isSelfSigned', False),
        'isExpired': result.get('isExpired', False),
        'isMismatched': result.get('isMismatched', False),
    }
    print(custom_result)
    with open(filename, 'a', encoding='utf-8') as json_file:
        json.dump(custom_result, json_file, cls=DateTimeEncoder, ensure_ascii=False, indent=2)
        json_file.write(',\n')  # Add a newline after each JSON object


if __name__ == "__main__":
    # asyncio.run(main_async())
    cert = get_certificate_info('www.baidu.com')
    print(cert)
