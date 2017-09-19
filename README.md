# 6pm spider

## 环境及依赖

``Python3``

``requests``

``lxml``


## 实现

以[shoes at 6pm.com](https://www.6pm.com/shoes-page1/CK_XAeICAQE.zso?p=0)为起始页采集网站上所有的鞋子。

抓取鞋子的商品品牌，标题，产品信息，每个SKU的属性，价格，图片。

## 使用方法

先指定最大采集页数。
在[getALLShoes.py](./getAllShoes.py)中的MAX_PAGES。
如果不想下载图片，可以修改GET_IMAGE = False。

运行：``python3 getAllShoes.py``

图片和鞋子详情(detail.txt)保存到当前目录下以SKU命名的文件夹。


## 待改进

1.没有抓到库存的包。

2.可以增加多进程加快爬取速度。

3.测试爬取了大概半小时还没被封。
