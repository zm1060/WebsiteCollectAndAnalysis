import certifi

print(certifi.where())


Failed to request website: http://sww.cq.gov.cn  (HTTPConnectionPool(host='sww.cq.gov.cn%20', port=80): Max retries exceeded with url: / (Caused by NameResolutionError("<urllib3.connection.HTTPConnection object at 0x7fa4659b63e0>: Failed to resolve 'sww.cq.gov.cn%20' ([Errno -2] Name or service not known)")))
Failed to request website: http://baoting.hainan.gov.cn (Status code: 301)
Failed to request website: http://wxgdj.wuzhou.gov.cn (Status code: 403)
File already exists: ./response/scjdglj.guilin.gov.cn.txtFailed to request website: https://credit.zs.gov.cn (HTTPSConnectionPool(host='credit.zs.gov.cn', port=443): Max retries exceeded with url: / (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1007)'))))

