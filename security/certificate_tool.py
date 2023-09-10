import ssl
import socket


def fetch_certificates(hostname):
    # Check if the website supports HTTPS
    try:
        # Send SYN on TCP port 443
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(10)  # Set a timeout in case the connection takes too long
            s.connect((hostname, 443))
    except ConnectionRefusedError:
        print(f"The website {hostname} does not support HTTPS.")
        return

    # Initiate an HTTPS connection and fetch SSL certificates
    try:
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                # Get the certificate
                cert = ssock.getpeercert()
                print(cert)
                # Print the certificate details
                print(f"Certificate for {hostname}:")
                print(f"Issuer: {cert['issuer']}")
                print(f"Subject: {cert['subject']}")
                print(f"Valid From: {cert['notBefore']}")
                print(f"Valid Until: {cert['notAfter']}")
                # Additional certificate information can be accessed in the 'cert' dictionary

    except ssl.SSLError as e:
        print(f"An error occurred while fetching the certificate: {e}")




# Example usage
fetch_certificates("www.baidu.com")


# Possible Output
var = {'subject': ((('countryName', 'CN'),), (('stateOrProvinceName', 'beijing'),), (('localityName', 'beijing'),),
                   (('organizationName', 'Beijing Baidu Netcom Science Technology Co., Ltd'),),
                   (('commonName', 'baidu.com'),)), 'issuer': (
(('countryName', 'BE'),), (('organizationName', 'GlobalSign nv-sa'),),
(('commonName', 'GlobalSign RSA OV SSL CA 2018'),)), 'version': 3, 'serialNumber': '55E6ACAED1F8A430F9A938C5',
       'notBefore': 'Jul  6 01:51:06 2023 GMT', 'notAfter': 'Aug  6 01:51:05 2024 GMT', 'subjectAltName': (
    ('DNS', 'baidu.com'), ('DNS', 'baifubao.com'), ('DNS', 'www.baidu.cn'), ('DNS', 'www.baidu.com.cn'),
    ('DNS', 'mct.y.nuomi.com'), ('DNS', 'apollo.auto'), ('DNS', 'dwz.cn'), ('DNS', '*.baidu.com'),
    ('DNS', '*.baifubao.com'), ('DNS', '*.baidustatic.com'), ('DNS', '*.bdstatic.com'), ('DNS', '*.bdimg.com'),
    ('DNS', '*.hao123.com'), ('DNS', '*.nuomi.com'), ('DNS', '*.chuanke.com'), ('DNS', '*.trustgo.com'),
    ('DNS', '*.bce.baidu.com'), ('DNS', '*.eyun.baidu.com'), ('DNS', '*.map.baidu.com'), ('DNS', '*.mbd.baidu.com'),
    ('DNS', '*.fanyi.baidu.com'), ('DNS', '*.baidubce.com'), ('DNS', '*.mipcdn.com'), ('DNS', '*.news.baidu.com'),
    ('DNS', '*.baidupcs.com'), ('DNS', '*.aipage.com'), ('DNS', '*.aipage.cn'), ('DNS', '*.bcehost.com'),
    ('DNS', '*.safe.baidu.com'), ('DNS', '*.im.baidu.com'), ('DNS', '*.baiducontent.com'), ('DNS', '*.dlnel.com'),
    ('DNS', '*.dlnel.org'), ('DNS', '*.dueros.baidu.com'), ('DNS', '*.su.baidu.com'), ('DNS', '*.91.com'),
    ('DNS', '*.hao123.baidu.com'), ('DNS', '*.apollo.auto'), ('DNS', '*.xueshu.baidu.com'),
    ('DNS', '*.bj.baidubce.com'), ('DNS', '*.gz.baidubce.com'), ('DNS', '*.smartapps.cn'), ('DNS', '*.bdtjrcv.com'),
    ('DNS', '*.hao222.com'), ('DNS', '*.haokan.com'), ('DNS', '*.pae.baidu.com'), ('DNS', '*.vd.bdstatic.com'),
    ('DNS', '*.cloud.baidu.com'), ('DNS', 'click.hm.baidu.com'), ('DNS', 'log.hm.baidu.com'),
    ('DNS', 'cm.pos.baidu.com'), ('DNS', 'wn.pos.baidu.com'), ('DNS', 'update.pan.baidu.com')),
       'OCSP': ('http://ocsp.globalsign.com/gsrsaovsslca2018',),
       'caIssuers': ('http://secure.globalsign.com/cacert/gsrsaovsslca2018.crt',),
       'crlDistributionPoints': ('http://crl.globalsign.com/gsrsaovsslca2018.crl',)}
