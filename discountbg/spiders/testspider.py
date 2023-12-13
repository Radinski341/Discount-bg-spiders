import scrapy


class TestspiderSpider(scrapy.Spider):
    name = "testspider"
    allowed_domains = ["http"]
    start_urls = ["https://www.emag.bg/dvulicev-matrak-mattro-flexo-memory-new-144-h-190-em07/pd/DTNZ1XMBM/"]

    def parse(self, response):
        category_values = ''
        for i in range(0, 2):
            category_values += "|" + response.xpath("normalize-space((//ol[@class='breadcrumb']/li)["+str(i + 1)+"])").get()
            

        yield{
            'category-values' : category_values
        }
