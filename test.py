# subject = {'subject': ((('countryName', 'CN'),), (('stateOrProvinceName', '上海'),), (('localityName', '上海'),), (('organizationName', '上海市大数据中心'),), (('commonName', '*.sh.gov.cn'),)), 'issuer': ((('countryName', 'CN'),), (('organizationName', 'UniTrust'),), (('commonName', 'SHECA OV Server CA G5'),)), 'version': 3, 'serialNumber': '5B45618D2A79207162F24F645DAE8217', 'notBefore': 'Jan 31 06:12:26 2023 GMT', 'notAfter': 'Feb 29 15:59:59 2024 GMT', 'subjectAltName': (('DNS', '*.sh.gov.cn'), ('DNS', 'sh.gov.cn')), 'OCSP': ('http://ocsp.global.sheca.com/ovscag5',), 'caIssuers': ('http://certs.global.sheca.com/ovscag5.cer',), 'crlDistributionPoints': ('http://crl.global.sheca.com/ovscag5.crl',)}
#
# for attr_list in subject['subject']:
#     attr, value = attr_list[0]
#     print(f'{attr}: {value}')
import os
from urllib.parse import urlparse

total = 0

for filename in os.listdir('domain_txt'):
    if not filename.endswith('.txt'):
        continue

    province = filename.split('.')[0]
    count = 0

    with open(f'domain_txt/{filename}', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        # f.seek(0)
        # f.truncate()

        for line in lines:
            original_line = line.strip()
            parsed = urlparse(original_line)

            # Add "http://" if the scheme is empty
            # if not parsed.scheme:
            #     modified_line = 'http://' + original_line
            # else:
            #     modified_line = original_line
            #
            # f.write(modified_line + '\n')

            domain = parsed.netloc + parsed.path
            if domain:
                count += 1
            else:
                print(original_line)

    print(f'{province}: {count}')
    total += count

print(f'Total: {total}')
