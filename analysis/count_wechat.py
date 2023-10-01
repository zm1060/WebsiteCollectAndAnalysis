import requests
from PIL import Image
from io import BytesIO
from pyzbar.pyzbar import decode


def check_qr_code(url):
    try:
        # Send GET request to retrieve the web page content
        response = requests.get(url, verify=False)
        # Check if the response was successful
        response.raise_for_status()

        # Read the binary content of the web page
        image_data = response.content
        # Load the binary content into a Pillow image object
        image = Image.open(BytesIO(image_data))
        # Convert the image to grayscale for better QR code recognition
        image_gray = image.convert("L")
        # Decode the QR codes in the image
        qr_codes = decode(image_gray)

        if qr_codes:
            print("QR codes found on the web page!")
            for qr_code in qr_codes:
                print("QR code data:", qr_code.data.decode("utf-8"))
        else:
            print("No QR codes found on the web page.")
    except requests.exceptions.RequestException as e:
        print("An error occurred while retrieving the web page:", e)
    except (OSError, IOError, Image.UnidentifiedImageError) as e:
        print("An error occurred while processing the image:", e)


# Example usage
check_qr_code("https://www.yancheng.gov.cn")