import requests
from PIL import Image
from io import BytesIO
from pyzbar.pyzbar import decode


def check_qr_code(url):
    # 发送GET请求获取网页内容
    response = requests.get(url)
    # 从响应中读取网页的二进制内容
    image_data = response.content
    # 将二进制内容加载到Pillow图像对象中
    image = Image.open(BytesIO(image_data))
    # 将图像转换为灰度图像，以便更好地进行二维码识别
    image_gray = image.convert("L")
    # 解码图像中的二维码
    qr_codes = decode(image_gray)

    if qr_codes:
        print("网页中存在二维码！")
        for qr_code in qr_codes:
            print("二维码数据:", qr_code.data.decode("utf-8"))
    else:
        print("网页中不存在二维码。")


# 示例使用
check_qr_code("https://ypjg.ln.gov.cn/")