import scrapy
from scrapy.exporters import JsonItemExporter



class EmagSpider(scrapy.Spider):
    name = "emag"
    allowed_domains = ["www.emag.bg"]
    start_urls = [
        "https://www.emag.bg/koledni-elhi/sort-discountdesc/c",
        "https://www.emag.bg/matraci/sort-discountdesc/c",
        "https://www.emag.bg/spalno-belio/sort-discountdesc/c",
        "https://www.emag.bg/tigani/sort-discountdesc/c",
        "https://www.emag.bg/perilni-preparati/sort-discountdesc/c",
        "https://www.emag.bg/veloergometri/sort-discountdesc/c",
        "https://www.emag.bg/vydici/sort-discountdesc/c",
        "https://www.emag.bg/palatki-za-kymping/sort-discountdesc/c",
        "https://www.emag.bg/aparati-za-grizha-poddryzhka-na-tialoto/sort-discountdesc/c",
        "https://www.emag.bg/prahosmukachki/sort-discountdesc/c",
        "https://www.emag.bg/mobilni-telefoni/sort-discountdesc/c"
    
    ]

    def parse(self, response):
        follow_urls = response.xpath("//div[@class='sidebar-tree-body']/a/@href")
        skip_first = True
        base_url = "https://www.emag.bg"

        for url in follow_urls:
            url = url.get()
            
            if not skip_first:
                split_url = url.split('c?')
                url = base_url + split_url[0] + 'sort-discountdesc/c'
                yield response.follow(url, callback = self.follow_next_category)
            skip_first = False



    def follow_next_category(self, response):
        products = response.xpath("//div[@class='card-v2-badge badge-discount']/ancestor::div[@class='card-v2']//div[@class='card-v2-info']/a/@href")
        base_url = "https://www.emag.bg"
        next_page = response.xpath("//a[@class='js-change-page js-next-page']/@href").get()
    

        for product in products:
            yield response.follow(product.get(), callback = self.scrape_product)

        if next_page:
            url = base_url + next_page
            yield response.follow(url, callback = self.follow_next_category)



    def scrape_product(self, response):
        images = response.xpath("//div[@class='multimedia-gallery hidden-xs multimedia-small-gallery ph-carousel-init ph-has-arrows']/div[@class='thumbnail-wrapper']/a/@href")
        imageUrls = ''

        for image in images:
            imageUrls += "|" + image.get()

        optionTypes = response.xpath("//div[@class='product-highlight ']/ul")
        optionTypeValues = ''
        optionValues = ''
        
        for i in range(0, len(optionTypes)):
            optionTypeValues += '|' + response.xpath("normalize-space((//div[@class='product-highlight ']/ul//ancestor::div[@class='product-highlight ']/p/text()[1])["+str(i + 1)+"])").get()
            options = response.xpath("(//div[@class='product-highlight ']/ul)["+str(i + 1)+"]/li/a/div[@class='label-wrapper ']/text()")
            options += response.xpath("(//div[@class='product-highlight ']/ul)["+str(i + 1)+"]/li/a/span/text()")
            optionValues += "(*)"
            for option in options:
                optionValues += "|" + option.get()

        category_values = ''
        for i in range(0, 2):
            category_values += "|" + response.xpath("normalize-space((//ol[@class='breadcrumb']/li)["+str(i + 1)+"])").get()
            

        yield{
            'website': 'emag',
            'website-url': "https://www.emag.bg/",
            'website-id': 'emag-'+ response.xpath("normalize-space(//span[@class='product-code-display hidden-xs']/text())").get(), 
            'product-url': response.request.url, 
            'title': response.xpath("normalize-space(//h1[@class='page-title']/text())").get(), 
            'old-price': response.xpath("(//section[@class='page-section page-section-light']//span[@class='rrp-lp30d-content']/s/text())[1]").get(), 
            'new-price': response.xpath("(//section[@class='page-section page-section-light']//p[@class='product-new-price has-deal']/text())[1]").get(), 
            'discount-percent': response.xpath("//div[@class='card-v2-badge badge-discount']/text()").get(), 
            'images': imageUrls, 
            'option-type': optionTypeValues,
            'options': optionValues, 
            'categories': category_values,
            'description-html': response.xpath("normalize-space(//table[@class='table table-striped specifications-table'])").get() 
        }