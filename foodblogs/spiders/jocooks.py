import scrapy


class JocooksSpider(scrapy.Spider):
    name = 'jocooks'
    start_urls = ['https://www.jocooks.com/category/recipes/']
    custom_settings = {
        'HTTPCACHE_ENABLED': True
    }

    def parse(self, response):
        for recipe_url in response.css('a.entry-title-link::attr(href)').getall():
            yield scrapy.Request(recipe_url, callback=self.parse_recipe)

        yield scrapy.Request(url=response.css('li.pagination-next a::attr(href)').get())

    def parse_recipe(self, response):
        yield {
            'url': response.url,
            'title': response.xpath('//meta[@property="og:title"]/@content').get(),
            'incredients': list(set(response.css('.wprm-recipe-ingredient-name *::text').getall()))
        }
