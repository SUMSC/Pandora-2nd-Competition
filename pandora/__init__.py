from flask import Flask, request, jsonify


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        """
        20'
        只有 Hello World 的首页
        :return:
        """
        return "Hello, world!"

    @app.errorhandler(404)
    def page_not_found(error):
        """
        10'
        以此项目中的404.html作为此Web Server工作时的404错误页
        """
        from flask import render_template
        return render_template('404.html'), 404

    # TODO: 完成接受 HTTP_URL 的 picture_reshape
    # TODO: 完成接受相对路径的 picture_reshape
    @app.route('/pic', methods=['GET'])
    def picture_reshape():
        """
        40' (20'ssh + 10' file + 10' http)

        **请使用 PIL 进行本函数的编写**
        获取请求的 query_string 中携带的 b64_url 值
        从 b64_url 下载一张图片的 base64 编码，reshape 转为 100*100，并开启抗锯齿（ANTIALIAS）
        对 reshape 后的图片分别使用 base64 与 md5 进行编码，以 JSON 格式返回，参数与返回格式如下

        :param: b64_url: 
            本题的 b64_url 以 arguments 的形式给出，可能会出现两种输入
            1. 一个 HTTP URL
            2. 一个指向 TXT 文本文件的相对路径，该 TXT 文本文件包含一个 base64 字符串

        :return: JSON
        {
            "md5": <图片reshape后的md5编码: str>,
            "base64_picture": <图片reshape后的base64编码: str>
        }
        """
        import PIL
        from PIL import Image
        import os
        import requests
        import base64
        from io import BytesIO
        import hashlib

        target_h = 100
        target_w = 100

        url = request.args.get('b64_url')
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

        return jsonify({"md5": hashlib.md5(image.tobytes()).hexdigest(), "base64_picture": base64_str.decode('utf8')})

    @app.route('/996')
    def company_996():
        """
        30'
        从 github.com/996icu/996.ICU 项目中获取所有的已确认是996的公司名单，并

        :return: 以 JSON List 的格式返回，格式如下
        [{
            "city": <city_name 城市名称>,
            "company": <company_name 公司名称>,
            "exposure_time": <exposure_time 曝光时间>,
            "description": <description 描述>
        }, ...]
        """
        from bs4 import BeautifulSoup
        import requests

        html = requests.get("https://github.com/996icu/996.ICU/blob/master/blacklist/README.md",
                            proxies={"https": "127.0.0.1:1080"}).text
        soup = BeautifulSoup(html, 'lxml')
        # print(soup.find(id='readme').article.find_all('table')[1].tbody.find_all('tr')[0].find_all('td')[0].text)
        # res=[[k.text for k in j.find_all('td')] for j in [i for i in soup.find(id='readme').article.find_all('table')[1].tbody.find_all('tr')]]
        res = [dict(zip(["city", "company", "exposure_time", "description"], [j.text for j in i.find_all('td')][:4]))
               for i in
               soup.find(id='readme').article.find_all('table')[1].tbody.find_all('tr')]
        return jsonify(res)

    return app
