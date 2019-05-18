def answer(url: str, app) -> dict:
    from PIL import Image
    import os
    import requests
    import base64
    from io import BytesIO
    import hashlib

    target_h = 100
    target_w = 100

    # url = request.args.get('b64_url')
    if os.path.exists(os.path.join(app.root_path, url)):
        with open(os.path.join(app.root_path, url), 'r') as fp:
            simg = fp.readline().strip()
    else:
        simg = requests.get(url).text
    img_data = base64.b64decode(simg)
    # 有时可能用到的urlencode
    # img_data = img_data.replace("%2B", "+").replace("%3D", "=").replace("%2F", "/")
    image = Image.open(BytesIO(img_data))
    image = image.resize((target_h, target_w), Image.ANTIALIAS)
    output_buffer = BytesIO()
    image.save(output_buffer, format='PNG')
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data)

    return {"md5": hashlib.md5(image.tobytes()).hexdigest(), "base64_picture": base64_str.decode('utf8')}


def test_reshape_file_md5(client, app):
    url = "img.txt"
    res = client.get('/pic?b64_url={}'.format(url))
    assert res.json.get('md5') == answer(url=url, app=app).get('md5')


def test_reshape_file_b64(client, app):
    url = "img.txt"
    res = client.get('/pic?b64_url={}'.format(url))
    assert res.json.get('base64_picture') == answer(url=url, app=app).get('base64_picture')


def test_reshape_http_md5(client, app):
    url = "https://oss.liontao.xin/img.txt"
    res = client.get('/pic?b64_url={}'.format(url))
    assert res.json.get('md5') == answer(url=url, app=app).get('md5')

def test_reshape_http_b64(client, app):
    url = "https://oss.liontao.xin/img.txt"
    res = client.get('/pic?b64_url={}'.format(url))
    assert res.json.get('base64_picture') == answer(url=url, app=app).get('base64_picture')
