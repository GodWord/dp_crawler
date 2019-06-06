import base64


def img_decode(base64_str):
    img_data = base64.b64decode(base64_str)
    return img_data
