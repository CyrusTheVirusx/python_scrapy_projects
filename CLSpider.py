from __future__ import absolute_import
from CraigslistCrawler.items import CraigslistcrawlerItem
from scrapy.http import Request
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule




class CLSpider(CrawlSpider):
    name = "CLSpider"
    allowed_domains = ["https://philadelphia.craigslist.org"]
    start_urls = ["https://philadelphia.craigslist.org/cto"]

    rules = (
        Rule(
        SgmlLinkExtractor(allow_domains=("https://philadelphia.craigslist.org/cto", )),
        callback='parse_page', follow=True
        ),

    )

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        rows = hxs.select('//div[@class="content"]/p[@class="row"]')

        for row in rows:
            item = CraigslistcrawlerItem()
            link = row.xpath('.//span[@class="pl"]/a')
            item['title'] = link.xpath("text()").extract()
            item['link'] = link.xpath("@href").extract()
            item['price'] = row.xpath('.//span[@class="l2"]/span[@class="price"]/text()').extract()

            url = 'https://philadelphia.craigslist.org'.format(''.join(item['link']))
            yield Request(url=url, meta={'item': item}, callback=self.parse_item_page)

    def parse_item_page(self, response):
        hxs = HtmlXPathSelector(response)

        item = response.meta['item']
        item['description'] = hxs.select('//section[@id="postingbody"]/text()').extract()
        return item