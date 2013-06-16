from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from scrapy.conf import settings
from scrapy import log
from linkedin.items import LinkedinItem
from urlparse import urljoin

class CompanyCrawler(BaseSpider):
    name = "linkedin"
    base_domain = 'http://www.linkedin.com'
    start_urls = [urljoin(base_domain, '/directory/companies/%s.html') %
                  s for s in settings['COMPANY_LETTERS']]

    def parse(self, response):

        hxs = HtmlXPathSelector(response)

        items = []
        TOP_LEVEL_DIR = '//*[@id="body"]/div/ul[2]/li/a/@href'

        relative_paths = hxs.select(TOP_LEVEL_DIR).extract()

        for rel_path in relative_paths:
            full_path = urljoin(self.base_domain, rel_path)
            if 'depth' in response.meta and response.meta['depth'] == 1:
                request = Request(full_path, callback=self.parse_company)
            else:
                request = Request(full_path, callback=self.parse)
            items.append(request)
        return items

    def parse_company(self, response):
        hxs = HtmlXPathSelector(response)

        TITLE_XPATH = '//*[@id="section-header"]/h1/text()'
        COUNTRY_XPATH = '//*[@class="adr"]/span[@class="country-name"]/text()'
        YEAR_XPATH = '//*[@id="extra"]/div[2]/div[2]/div/dl/dd[5]/text()'
        SITE_XPATH = '//div[@class="basic-info"]/div[@class="content inner-mod"]/dl/dd[3]/a/text()'

        company_name = hxs.select(TITLE_XPATH).extract()
        country = hxs.select(COUNTRY_XPATH).extract()
        year = hxs.select(YEAR_XPATH).extract()
        website = hxs.select(SITE_XPATH).extract()

        item = LinkedinItem(_id=response.url, country=country,
                            name=company_name, foundation_year=year)
        item['website_link'] = website
        return item
