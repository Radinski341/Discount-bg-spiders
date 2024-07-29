import scrapy


class MakasaSpider(scrapy.Spider):
    name = "makasa"
    allowed_domains = ["makasa.org"]
    start_urls = [
        "https://makasa.org/category/za-doma?per_page=90",
        "https://makasa.org/category/eterichni-masla?per_page=90",
        "https://makasa.org/category/bazovi-masla?per_page=90",
        "https://makasa.org/category/difuzeri?per_page=90",
        "https://makasa.org/category/lice?per_page=90",
        "https://makasa.org/category/tyalo?per_page=90",
        "https://makasa.org/category/kosa?per_page=90",
        "https://makasa.org/category/grim?per_page=90",
        "https://makasa.org/category/slancezashtitni-produkti?per_page=90",
        "https://makasa.org/category/za-mama-i-bebe?per_page=90",
        "https://makasa.org/category/kozmetika-za-maje?per_page=90 6933"
    ]

    def parse(self, response):
        base_url = 'https://makasa.org'
        products = response.xpath("//div[@class='_products-list']//div[contains(@class, '_product-ribbon-holder')]//span[text()='SALE']/ancestor::div[contains(@class, '_product-inner')]//a[contains(@class, '_product-quick-view')]/@href")
        next_page = response.xpath("//li[@class='next']/a/@href").get()
        

        for product in products:
            yield response.follow(product.get(), callback = self.scrape_product)
        
        if next_page:
            url = base_url + next_page
            yield response.follow(url, callback = self.parse)
    
    def scrape_product(self, response):
        image = response.xpath("//img[@class='image primary lazyload-image lazyload-square']/@data-src").get()
        if image:
            image = '|' + image

        description = response.xpath("//div[@class='woocommerce-product-details__short-description']").get()
        
        if not description:
            description = response.xpath("//div[@class='_textbox']").get()

        category = '|Козметика'
        subcategory = response.xpath("normalize-space(//div[@class='_breadcrumb']//ul/li[2]/a/text())").get()
        
        if subcategory:
            category = category + '|' + subcategory

        yield{
            'is-product-choice': False,
            'website': 'makasa',
            'website-url': "https://makasa.org",
            'website-id': response.xpath("normalize-space(//h1[@class='_h2 js-product-title']/text())").get(), 
            'product-url': response.request.url, 
            'title': response.xpath("normalize-space(//h1[@class='_h2 js-product-title']/text())").get(), 
            'old-price': response.xpath("(//div[@class='_product-details-price-old price-old-js ']//i[@class='_product-details-price-value rtl-ltr']/text())[1]").get(), 
            'new-price': response.xpath("(//span[@class='_product-details-price-new price-new-js rtl-ltr']/text())[1]").get(), 
            'discount-percent': response.xpath("(//span[@class='_product-ribbon _product-discount _product-discount-percent js-discount-save-percent']//span/text())[1]").get(), 
            'images': image, 
            'categories': category,
            'delivery-price': '6',
            'description-html': description   
        }
