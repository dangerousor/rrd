#!/usr/bin/python
# -*- coding:utf-8 -*-
import rrd


if __name__ == '__main__':
    spider = rrd.Spider()
    # with open('test.html', 'wb+') as f:
    #     f.write(spider.get_html().content)
    spider.run()
