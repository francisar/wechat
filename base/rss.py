#!/usr/bin/env python
# coding=utf-8

import feedparser

class RSS(object):

    def __init__(self,url):
        self.__rss = feedparser.parse(url)

    def get_title(self):
        return self.__rss.feed.title

    def get_entries(self):
        return self.__rss.entries

    def get_top_entry(self):
        return self.__rss.entries[0]

    def get_entry_list(self):
        title_list = {}
        for entry in self.__rss.entries:
            title_list[entry.title] = entry.links[0]["href"]
        return title_list

