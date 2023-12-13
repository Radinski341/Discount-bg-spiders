import scrapy


class MagazinabgSpider(scrapy.Spider):
    name = "magazinabg"
    allowed_domains = ["magazinabg.com"]
    start_urls = ["https://magazinabg.com/%D0%B2%D1%81%D0%B8%D1%87%D0%BA%D0%B8-%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D0%B8"]

    def parse(self, response):
        products = response.xpath("//span[contains(@class, 'sale_badge')]//ancestor::div[@class='image']//a[1]//@href")

        nextPage = response.xpath("//ul[@class='pagination']/li//text()[.='>']/ancestor::a/@href").get()
        for product in products:
            yield response.follow(product.get(), callback = self.scrape_product)

        if nextPage:
            yield response.follow(nextPage, callback = self.parse)

    
    def scrape_product(self, response):
        images = response.xpath("//meta[@property='og:image']/@content")
        imageUrls = ''

        for image in images:
            imageUrls += "|" + image.get()

        
        options = response.xpath("//div[@class='options']//select/option/text()")
        optionValues = ''

        for option in options:
            if 'Моля' not in option.get():
                optionValues += '|' + option.get()

        outOfStock = response.xpath("//div[@class='main-image']//span[@class='badge out_of_stock_badge']").get()

        if not outOfStock:
            yield{
                'website': 'magazinabg',
                'website-url': "https://magazinabg.com/",
                'website-id': 'magazinabg-'+ response.xpath("//p[@class='info']/text()").get(),
                'product-url': response.request.url,
                'title': response.xpath("//h1[@id='page-title']/text()").get(),
                'old-price': response.xpath("//span[@class='price-old']/text()").get(),
                'new-price': response.xpath("//span[@class='live-price-new']/text()").get(),
                'discount-percent': response.xpath("//span[@class='badge sale_badge']//i/text()").get(),
                'images': imageUrls,
                'option-type': response.xpath("//div[@class='options']//label[@class='control-label']/text()").get(),
                'options': optionValues,
                'description-html': response.xpath("normalize-space(//div[@class='tab-pane active'])").get()
            }