#             商品品牌，标题，产品信息
#             每个SKU的属性，价格，库存，图片
import requests
from requests.exceptions import ConnectionError
from lxml import etree
import re
import json
import os
from hashlib import md5


def get_page(url, headers=None):
    try:
        response = requests.get(url, headers=headers)
        # print(response.status_code)
        # print(response.text)
        if response.status_code == requests.codes.ok:
            return response.text
    except ConnectionError as e:
        print(e.args)


def get_img_json(params):
    url = 'https://api.zcloudcat.com/v1/images'

    try:
        response = requests.get(url, params=params)
        if response.status_code == requests.codes.ok:
            return response.text
    except ConnectionError as e:
        print(e.args)


def save_image(path, filename, content, pformat):
    if not os.path.exists(path):
        os.mkdir(path)
    filename = filename + '_' + md5(content).hexdigest()
    file = '{0}/{1}/{2}{3}'.format(os.getcwd(), path, filename, pformat)
    print(file)
    if not os.path.exists(file):
        with open(file, 'wb') as f:
            f.write(content)
            f.close()


def download_image(url):
    try:
        response = requests.get(url)
        if response.status_code == requests.codes.ok:
            return response.content
        else:
            print('error!')
    except ConnectionError as e:
        print(e.args)


def get_image(sku):
    params = {
        'productId': sku,
        'siteId': '2',
        'recipe': '["MULTIVIEW", "SWATCH"]',
        'type': '["SWATCH", "PAIR", "TOP", "BOTTOM", "LEFT", "BACK", "RIGHT", "FRONT"]',
        'excludes': '["format", "productId", "recipeName", "styleId", "imageId"]',
    }

    img_json = get_img_json(params)
    images = json.loads(img_json)
    img = []
    # print(images)
    for image_k in images:
        if image_k == 'images':
            for imgs in images[image_k].items():
                for img in imgs:
                    # print(type(img))
                    print('3', img)
                    if isinstance(img, list):
                        for img_ in img:
                            name = sku + '_' + img_['type']
                            img_url = 'https://www.6pm.com' + img_['filename']
                            # print(img_url)
                            pformat = img_url[img_url.rfind('.'):]
                            # print(pformat)
                            save_image(sku, name, download_image(img_url), pformat)


def parse_page(html, url, sku):
    print('start parse page...', url)

    html = etree.HTML(html)

    # 品牌以及品牌链接
    brand = html.xpath("string(//div[@class='SRGgm']/div/a[4])")
    brand_url = 'https://www.6pm.com' + html.xpath("//div[@class='SRGgm']/div/a[4]/@href")[0]
    print(brand, brand_url)

    # 标题
    title = html.xpath("string(//div[@class='vUkNo'])")
    print(title)

    # 产品信息
    product_info = html.xpath("string(//div[@class='_1Srfn']/ul)").strip()
    print(product_info)

    # 价格
    price = html.xpath("//span[@class='_3r_Ou ']/text()")
    if price:
        price = price[0]
    else:
        price = html.xpath("//span[@class='_3r_Ou']/text()")[0]
    print(price)

    # 颜色 尺寸 宽度
    color = html.xpath(
        "//div[@class='_30wtU']/div[@class='_17Dby']/form/div[@class='VrH5P']/div[@class='Dcl_8']/select[@id='pdp-color-select']/option/text()")
    if color:
        color = color if not color[0].startswith('Select') else color[1:]
    else:
        color = html.xpath(
            "//div[@class='_30wtU']/div[@class='_17Dby']/form/div[@class='VrH5P']/div[@class='_24jH2']/text()")
    print(color)

    size = html.xpath(
        "//div[@class='_30wtU']/div[@class='_17Dby']/form/div[@class='_1KSLq']/div[@class='VrH5P'][1]/div[@class='Dcl_8']/select[@id='pdp-size-select']/option/text()")
    if size:
        size = size if not size[0].startswith('Select') else size[1:]
    else:
        size = html.xpath(
            "//div[@class='_30wtU']/div[@class='_17Dby']/form/div[@class='_1KSLq']/div[@class='VrH5P'][1]/div[@class='_24jH2']/text()")
    print(size)

    width = html.xpath(
        "//div[@class='_30wtU']/div[@class='_17Dby']/form/div[@class='_1KSLq']/div[@class='VrH5P'][2]/div[@class='Dcl_8']/select[@id='pdp-width-select']/option/text()")
    if width:
        width = width if not width[0].startswith('Select') else width[1:]
    else:
        width = html.xpath(
            "//div[@class='_30wtU']/div[@class='_17Dby']/form/div[@class='_1KSLq']/div[@class='VrH5P'][2]/div[@class='_24jH2']/text()")
    print(width)

    item = {
        'url': url,
        'brand': brand,
        'brand_url': brand_url,
        'title': title,
        'product_info': product_info,
        'color': color,
        'size': size,
        'width': width,
    }
    if not os.path.exists(sku):
        os.mkdir(sku)
    file = '{0}/{1}/detail.txt'.format(os.getcwd(), sku)
    with open(file, 'w') as f:
        f.write(json.dumps(item))
        f.close()


if __name__ == '__main__':
    # url = 'https://www.6pm.com/p/lifestride-spark-red/product/8872328/color/585'
    # url = 'https://www.6pm.com/p/nine-west-elenta-light-natural-leather/product/8819494/color/52907?zlfid=192&ref=pd_detail_1_sims_p'
    # url = 'https://www.6pm.com/p/lifestride-spark-taupe/product/8872328/color/11?zlfid=192&ref=pd_detail_1_sims_p'
    # url = 'https://www.6pm.com/p/bandolino-yara-natural-synthetic/product/8599315/color/59416?zlfid=192&ref=pd_detail_1_sims_p'
    url = 'https://www.6pm.com/p/stride-rite-batman-lighted-athletic-2-0-toddler-little-kid-navy/product/8718735/color/515'
    sku = re.search(r'product/(\d*)', url).group(1)
    # print(sku)
    # get_image(sku)

    html = get_page(url)
    parse_page(html, url, sku)
