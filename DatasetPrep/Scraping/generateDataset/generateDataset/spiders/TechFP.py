import sys
import scrapy
import re

storyCount = 0
storyLimit = 1
pageLimit = 1

class TechfpSpider(scrapy.Spider):
    name = 'TechFP'
    allowed_domains = ["firstpost.com"]
    start_urls = ["https://www.firstpost.com/tech/news-analysis/page/2"]

    def parse(self, response):
        currPageNum = int( response.css( "a.active::text" ).extract_first() )
        Links = response.css('div.text-wrapper>a[href*="firstpost.com"]::attr(href)').extract()
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
            nextPageLink = response.css( 'a[rel="next"]::attr(href)' ).extract_first()
            #TODO Add check for nextPageLink in order to catch last page
            yield scrapy.Request(nextPageLink, callback = self.parse)

    def parseNews(self, response):
        storyLink = response.url      
        headLine = response.css( "h1.post-title::text" ).extract_first()
        Source = "FirstPost"
        sourceLink = "https://www.firstpost.com/"

        imageLink = response.css( 'img[class*="wp-image-"]::attr(src)' ).extract_first()
        if(imageLink is None):
            imageLink = ""
        else:
            imageLink = re.search( "images.+", imageLink )[0]

        paraText = set(  response.css( "div.text-content-wrap>p::text" ).extract()  )
        paraSpanText = set(  response.css( "div.text-content-wrap>p span::text" ).extract()  )
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