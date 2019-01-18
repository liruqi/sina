# -*- coding: utf-8 -*-

from __future__ import absolute_import
import bs4, logging, os
from spider.spider import Spider
from weibo.weibo_message import WeiboMessage

HOME_URL = "http://www.hust.edu.cn"

class HUSTParser(Spider):

    def __init__(self):
        super(HUSTParser, self).__init__(HOME_URL)
        self.logger = logging.getLogger()

    def get_weibo_message(self):
        html = self.download_text()
        soup = bs4.BeautifulSoup(html, "html.parser")
        items = soup.find_all(attrs={"class": "xnews_title"})
        yitems = soup.find_all(attrs={"class": "ynews_title"})
        items = items + yitems
        gnewsDom = soup.find(attrs={"class": "mod-news-4"})
        yitems = gnewsDom.find_all(attrs={"class": "snews_title"})
        print ("snews_title:", yitems)
        self.logger.info(str(items))
        items = items + yitems
        msg = ''
        for topItem in (items):
            title = topItem.a.string.strip()
            url = topItem.a.get('href')
            if (self.posted(url)):
                continue
            msg = "%s%s%s" % (title, os.linesep, url)
            wm = WeiboMessage(msg)
            self.write(url, wm)
            print ("HUSTParser:", url, msg)
            return wm
        return None
