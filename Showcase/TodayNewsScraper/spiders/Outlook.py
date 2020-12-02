import sys
import scrapy
import re
from datetime import datetime, timedelta

stopScraping = False
storyCount = 0
storyLimit = 15
daysToScrape = 1

urlPrefix = "https://www.outlookindia.com"

class OutlookSpider(scrapy.Spider):
    name = "Outlook"
    allowed_domains = ["outlookindia.com"]
    start_urls = ["https://www.outlookindia.com/website/1/"]

    def parse(self, response):
        #currPageNum = int( response.css("ul.page-numbers>li>a.currentpage::text").extract_first() )
        global storyCount
        global stopScraping

        Links = response.css(  "div.web_sub_search div.excl_left div.listing ul li div.main_heading_new a::attr( href )"  ).extract()
        Links = Links + response.css(  "div.web_sub_search div.excl_left div.listing ul li div.content_serach div.cont_head a::attr( href )"  ).extract()

        for Link in Links:
            if( stopScraping == False ):
                Link = urlPrefix + Link
                yield scrapy.Request(Link, callback = self.parseNews)
                storyCount += 1
                if( storyCount == storyLimit ):
                    stopScraping = True
                
            else:
                break

        if( stopScraping == False ):
            nextPageLink = urlPrefix + response.css( "div.pagination ul li a::attr(href)" ).extract_first()
            #TODO Add check for nextPageLink in order to catch last page
            yield scrapy.Request(nextPageLink, callback = self.parse)
            
    def parseNews(self, response):
        global stopScraping
        storyLink = response.url      

        headLine = response.css( "div.wrapper_story_left h1[ itemprop = 'headline' ]::text" ).extract_first() or ""
        
        Source = "Outlook India"
        sourceLink = "https://www.outlookindia.com/"

        imageLink = response.css( "div.wrapper_story_left div.magzine_stry_image img::attr(src)" ).extract_first() or ""

        contentList = response.css(  "div.wrapper_story_left div.story_description div[ itemprop = 'articleBody' ] p *::text"  ).extract()
        Content = " ".join( contentList )

        Output = {
            "headLine": headLine,
            "storyLink": storyLink,
            "Source": Source,
            "sourceLink": sourceLink,
            "imageLink": imageLink,
            "Content": Content
        }
		
        rightNow = datetime.now()
        articleTiming = response.css( "div.author_name_date *::text" ).extract()
        for Element in articleTiming:
            DateTimeMatch = re.search( "\d\d \w+ \d\d\d\d", Element )
            if( DateTimeMatch is not None ):
                articleTiming = DateTimeMatch[0]
                break

        articleTiming = datetime.strptime( articleTiming, "%d %B %Y" )
        if(
            articleTiming < (  rightNow - timedelta( days = daysToScrape )  )
        ):
            stopScraping = True
            
        yield Output