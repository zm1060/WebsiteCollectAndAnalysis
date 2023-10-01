
import requests


def analyze_subdomains(subdomains):
    for subdomain in subdomains:
        url = f"http://{subdomain}.yourdomain.com"
        response = requests.get(url, allow_redirects=False)

        if response.status_code == 200:
            if response.url.startswith("https://"):
                print(f"{subdomain} 使用了直接的HTTPS连接")
            else:
                print(f"{subdomain} 未使用HTTPS")
        elif response.status_code == 301 or response.status_code == 302:
            redirect_location = response.headers.get("Location")
            if redirect_location and redirect_location.startswith("https://"):
                print(f"{subdomain} 重定向到HTTPS网站")
            else:
                print(f"{subdomain} 未使用HTTPS且未重定向到HTTPS网站")
        else:
            print(f"{subdomain} 访问失败")


# 示例使用的次级域名列表
subdomains = ["subdomain1", "subdomain2", "subdomain3"]

# 调用函数进行分析
analyze_subdomains(subdomains)