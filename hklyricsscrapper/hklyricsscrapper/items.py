# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HklyricsscrapperItem(scrapy.Item):
    # define the fields for your item here like:
    artist_name = scrapy.Field()
    song_name = scrapy.Field()
    lyrics = scrapy.Field()
