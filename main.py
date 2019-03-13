#!/usr/bin/python
# -*- coding:utf-8 -*-
import re
import rrd


if __name__ == '__main__':
    spider = rrd.Spider()
    # with open('test.html', 'wb+') as f:
    #     f.write(spider.get_html().content)
    ids = [i for i in range(2872653, 2872654)]
    spider.run(ids)
