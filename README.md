# WebsiteCollectAndAnalysis



## Configure

```shell
sudo apt-get install whois
```

```shell
pip install -r requirements.txt
```

## Run
First Run: collect_gwy.py and collect_provience.py, it may take hours to run it(it's a bug, i have no idea about it).
```shell
python3 collect_gwy.py
```
Open a new terminal and run
Notice: You should make sure your current work dir is in the project.

something like /***/WebsiteCollectAndAnalysis
```shell
python3 collect_provience.py
```
And then you can run unzip_gwy.py and unzip_sheng.py, since you run the above file which will download a lot of zip file.

```shell
python3 unzip_gwy.py
```

```shell
python3 unzip_sheng.py
```


After that, we will further process these file. I have download and unzip all of them.
```shell
python3 merger_csv.py
```
It will merger all file under the directory of /total_csv and output the result to /mergerd_csv

## ToDo
二、研究内容
1. 关系图
仅绘制首页关系图
依据出度和入度，绘制全国各省市关系图。分析哪些类型的节点较为重要。

2. 分析网站链接的无效率
分析首页中网站的链接（内链和外链）无效情况，包括域名解析和网页内容等等。
以数量+比例进行对比。
外链的数量和分布情况。
3. 流量分析
通过第三方网络服务来统计重点目标网站的访问流量，基于流量对重点站点进行排序，用于分析安全威胁的风险范围。
   - 流量大小排名
   - 是否存在国家或城市区分
4. Http/Https分析
重点参考文献 [1]
   - 站点首页使用https和http的情况，并且从不同角度（部门、省市级别、行政功能）进行统计；
   - 分析次级域名是否应用 https，包括三种类型：未使用、直接使用和重定向到https网站；
   - TLS分为多个版本，可测试https使用的是哪个版本；
   - 获取证书的多级数据；
   - 参考论文[1]中构建的检测工具，对网站使用的证书从多个角度，对其进行评级；
   - 统计各个部门的网站应用HTTPS的情况；
   - 统计最常使用CA，是否免费，收费如何等等，是否存在使用不信任（漏洞）的证书；
   - 统计全站或者非全站使用Https的情况；
   - 网页部分加密，网页中外部的链接非https加密
   "Blocked mixed content" 意思是网站中同时包含了安全和不安全的内容，使得浏览器无法加载所有内容，从而导致网站无法正常访问。这通常是由于网站使用了不安全的 HTTP 协议来加载某些内容，而浏览器使用的是安全的 HTTPS 协议。为了确保网站的安全性，浏览器会阻止加载不安全的内容，从而导致网站无法正常显示。要解决此问题，您需要将网站中所有的 HTTP 链接更改为 HTTPS 链接，以确保所有内容都是安全的。
5. 可访问性和合理性
该问题是否深入研究待考虑
在使用浏览器访问网站时，浏览器会自动加上www，但是部分站点不加www，无法正常访问，这是什么原因呢？
6. 第三方服务分析
围绕：Content Security Polic 和 Subresource integrity 进行分析。（待学习，参考论文[4]），Web网页安全也是非常广泛，是否进一步研究，需要经过调研后再说。
  - 分析网页中内嵌的图床、JavaScript、广告等第三方服务的普遍性和安全性
     - 是否存在广告
     - 是否嵌入恶意信息
     - JavaScript版本，是否存在安全漏洞
       - $.fn.jquery命令来查看软件版本，参考
  - 分析网站的外链的特点，外链大部分是关联到哪些网站的，绘图展示所有网站的关联关系。
    - 通过关联关系可发现重点域名
    - 非政府网站用绿色
    - 政府网站用红色
  - 研究政府网站是否遵守CSP和SRI机制
7. DNS记录分析
- IPv4和IPv6
  - IP地址数量和运营商，冗余角度分析
  - IPv6的部署规模
  - IP地址的地理位置，省市级别的网站的IP是否是在特定区域，使访问更快
  - 托管商是本地服务商，还是云服务商
- CNAME
  - 是否使用CDN服务
  - CDN服务商
- NS (参考文献[2])
平均水平、全国各省市横向对比，分析NS的情况
  - 权威服务商特点，是否集中，可绘图展示
  - 权威服务器数量，冗余角度分析
  - 权威服务器是否隶属多个服务商
  - 权威服务器是第三方，还是自建
- PTR记录？为什么有，普及率呢？
8. 分析次级网页
对次级网页的特点也继续分析，包括安全性、JavaScript、图床等第三方服务进行分析。
9. 内容分析
- 备案信息
  - ICP备案信息
  - 公安备案信息
- 电子化程度，是否有小程序或者公众号等内容
- 无障碍化、关怀版等适合老年人的功能
- 其他
10. 外部域名注册信息
对于非.gov.cn的域名，获取它们的WHOIS注册信息，分析以下内容：
- 注册公司
- 注册人姓名
- 注册商
- 注册地点
- 联系方式
11. 技术沟通
若发现安全问题，向对方沟通，保证对方网站的安全。
12. 资源严重依赖
从多个维度分析，政府网站的资源是否严重依赖或者集中，导致通过攻击个别实体，即可攻破所有网站，对其影响范围进行评估，参考论文[5]。通过构建图关系模型，进行风险评估。
论文[5]构建了基于图的评估模型，非常值得参考，无论是计算资源依赖，还是计算风险，都可以参考。

- 网页内容
  - 如何获取网页加载产生的所有链接，包括JavaScript、CSS、图片、JSON等
    - 静态获取网页链接，分析是否存在外部链接等
    - 动态获取网页加载时所需要的资源
- DNS记录（dnspython包）
  - IP
    - IPv4和IPv6
    - IPv4地理位置
  - CNAME
    - CDN服务，及其厂商
  - NS
    - 权威服务器商
- 站点证书
- 流量排名
- 备案信息（针对事业单位），发现极个别网站无备案信息

