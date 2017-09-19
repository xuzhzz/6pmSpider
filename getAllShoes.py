from spider import *
from multiprocessing import Pool


MAX_PAGE = 100  # 最大获取页数
GET_IMAGE = True  # 是否下载图片
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
}


def main():
    for i in range(0, MAX_PAGE):
        url = 'https://www.6pm.com/shoes-page{}/CK_XAeICAQE.zso?p={}'.format(str(i + 1), str(i))
        html = get_page(url, headers)
        html = etree.HTML(html)
        product_urls = html.xpath('//div[@id="searchResults"]/a/@href')
        for purl in product_urls:
            purl = 'https://www.6pm.com/' + purl
            sku = re.search(r'product/(\d*)', purl).group(1)
            if os.path.exists(sku):
                print('已经爬取过的SKU', sku)
                continue
            if GET_IMAGE:
                get_image(sku)
            html2 = get_page(purl)
            parse_page(html2, purl, sku)

if __name__ == '__main__':
    main()