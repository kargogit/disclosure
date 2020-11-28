import sys
import scrapy
import re

storyCount = 0
storyLimit = 1
pageLimit = 1

class HealthfpSpider(scrapy.Spider):
    name = 'HealthFP'
    allowed_domains = ["firstpost.com"]
    start_urls = ["https://www.firstpost.com/category/health/page/1"]

    def parse(self, response):
        currPageNum = int( response.css("ul.pagination>li.active>a::text").extract_first() )
        Links = response.css("div.big-thumb>div.title-wrap>h3.main-title>a::attr(href)").extract()
        for Link in Links:
            global storyCount
            if(
                ( storyCount < storyLimit )
                or
                ( storyLimit == -1 )
            ):
                yield scrapy.Request(Link, callback = self.parseNews)
                storyCount += 1
            else:
                currPageNum = pageLimit
                break

        if(
            ( currPageNum < pageLimit )
            or
            ( pageLimit == -1 )
        ):
            nextPageLink = response.css( "ul.pagination>li.next>a::attr(href)" ).extract_first()
            #TODO Add check for nextPageLink in order to catch last page
            yield scrapy.Request(nextPageLink, callback = self.parse)

    def parseNews(self, response):
        storyLink = response.url      
        headLine = response.css('h1.inner-main-title::text').extract_first()
        Source = "FirstPost"
        sourceLink = "https://www.firstpost.com/"

        imageLink = response.css( "div.article-img>img::attr(data-src)" ).extract_first()
        if(imageLink is None):
            imageLink = ""
        else:
            imageLink = re.search( "images.+", imageLink )[0]


        paraText = set(  response.css( "div.article-full-content>p::text" ).extract()  )
        paraSpanText = set(  response.css( "div.article-full-content>p span::text" ).extract()  )
        contentList = list(  paraText.union( paraSpanText )  )
        Content = " ".join( contentList )

        Output = {
            "headLine": headLine,
            "storyLink": storyLink,
            "Source": Source,
            "sourceLink": sourceLink,
            "imageLink": imageLink,
            "Content": Content
        }
        yield Output