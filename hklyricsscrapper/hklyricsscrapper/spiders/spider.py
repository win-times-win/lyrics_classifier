import scrapy
from scrapy import Selector
from scrapy.http import Request
from ..items import HklyricsscrapperItem


class LyricsSpider(scrapy.Spider):
    name = "Lyrics"
    allowed_domains = ["mojim.com"]
    start_urls = [
        "https://mojim.com/twzlha_02.htm",
        "https://mojim.com/twzlha_03.htm",
        "https://mojim.com/twzlha_04.htm",
        "https://mojim.com/twzlha_05.htm",
        "https://mojim.com/twzlha_06.htm",
        "https://mojim.com/twzlha_07.htm",
        "https://mojim.com/twzlhb_02.htm",
        "https://mojim.com/twzlhb_03.htm",
        "https://mojim.com/twzlhb_04.htm",
        "https://mojim.com/twzlhb_05.htm",
        "https://mojim.com/twzlhb_06.htm",
        "https://mojim.com/twzlhb_07.htm",
        "http://mojim.com/twzlhc_28.htm",
        "http://mojim.com/twzlhc_29.htm",
        "http://mojim.com/twzlhc_30.htm",
        "http://mojim.com/twzlhc_31.htm",
        "http://mojim.com/twzlhc_32.htm",
        "http://mojim.com/twzlhc_33.htm",
    ]

    def parse(self, response):
        out = HklyricsscrapperItem()
        i = 0
        for artist_list in response.css("ul.s_listA a").getall():
            i += 1
            if i > 1:
                break
            artist_list = Selector(text=artist_list)
            artist_list_url = artist_list.css("a::attr(href)").get()
            artist_name = artist_list.css("a::text").get()
            yield response.follow(
                artist_list_url,
                callback=self.parse_artist,
                meta={"out": out, "artist_name": artist_name},
            )

    def parse_artist(self, response):
        out = response.meta["out"]
        artist_name = response.meta["artist_name"]
        print("im here at artist")
        for hc in ["hc3", "hc4"]:
            for song_list in response.css(f"span.{hc} a").getall():
                song_list = Selector(text=song_list)
                song_list_url = song_list.css("a::attr(href)").get()
                song_name = song_list.css("a::text").get()
                yield response.follow(
                    song_list_url,
                    callback=self.parse_song,
                    meta={
                        "out": out,
                        "artist_name": artist_name,
                        "song_name": song_name,
                    },
                )

    def parse_song(self, response):
        out = response.meta["out"]
        artist_name = response.meta["artist_name"]
        song_name = response.meta["song_name"]
        print("im here at song")
        out["artist_name"] = artist_name
        out["song_name"] = song_name
        out["lyrics"] = response.css("dd#fsZx3::text").getall()
        yield out
