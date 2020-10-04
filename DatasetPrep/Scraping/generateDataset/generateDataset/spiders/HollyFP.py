import sys
import scrapy

storyCount = 0
storyLimit = int( sys.argv[1] )
pageLimit = int( sys.argv[2] )

class HollyfpSpider(scrapy.Spider):
    name = 'HollyFP'
    allowed_domains = ["firstpost.com"]
    start_urls = ["https://www.firstpost.com/entertainment/hollywood/page/1"]

    def parse(self, response):
        Links = response.css("div.big-thumb>div.title_wrap>h3.main-title>a::attr(href)").extract()
        for Link in Links:
            if(
                ( storyCount < storyLimit )
                or
                ( storyLimit == -1 )
            ):
                yield scrapy.Request(Link, callback = self.parseNews)
                storyCount += 1
            else:
                break

        currPageNum = int( response.css("ul.pagination>li.active>a::text").extract_first() )
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
        #TODO Check the CSS Path to Image Tag
        imageLink = response.css('img[class*="wp-image-"]::attr(src)').extract_first()
        if(imageLink is None):
            imageLink = ""
        contentList = response.css( "div.article-full-content>p::text" ).extract()
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