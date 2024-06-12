import scrapy


class TestspiderSpider(scrapy.Spider):
    name = "testspider"
    allowed_domains = ["www.emag.bg"]
    start_urls = ["https://www.emag.bg/komplekt-giri-liveup-2-br-2h2kg-16-5sm-oranzhev-10212058/pd/D9DNSYMBM/"]


    def parse(self, response):
        images = response.xpath("//div[@class='multimedia-gallery hidden-xs multimedia-small-gallery ph-carousel-init ph-has-arrows']/div[@class='thumbnail-wrapper']/a/@href")
        imageUrls = ''

        for image in images:
            imageUrls += "|" + image.get()

        if imageUrls == "":
            imageUrls+= '|' + response.xpath("//a[@class='thumbnail product-gallery-image gtm_rp125918']/@href").get()
        
        parentProductId = 'emag-'+ response.xpath("normalize-space(//span[@class='product-code-display hidden-xs']/text())").get()
        
        
       
        optionType = response.xpath("normalize-space((//div[@class='product-highlight ']/ul//ancestor::div[@class='product-highlight ']/p/text()[1])[1])").get()
        options = response.xpath("(//div[@class='product-highlight ']/ul)[1]/li/a/div[@class='label-wrapper ']")
        options += response.xpath("(//div[@class='product-highlight ']/ul)[1]/li/a/span")
        for option in options:
            followUrl = option.xpath('ancestor::a/@href').get()
            self.parent_website_id = parentProductId
            
            yield response.follow(followUrl, callback = self.get_product_option, meta = {'parent-website-id': parentProductId, 'parent-option': option.xpath('text()').get(), 'option-type' : optionType})
        
            

        category_values = ''
        for i in range(0, 2):
            category_values += "|" + response.xpath("normalize-space((//ol[@class='breadcrumb']/li)["+str(i + 1)+"])").get()
            

        yield{
            'is-product-choice': False,
            'website': 'emag',
            'website-url': "https://www.emag.bg/",
            'website-id': parentProductId, 
            'product-url': response.request.url, 
            'title': response.xpath("normalize-space(//h1[@class='page-title']/text())").get(), 
            'old-price': response.xpath("(//section[@class='page-section page-section-light']//span[@class='rrp-lp30d-content']/s/text())[1]").get(), 
            'new-price': response.xpath("(//section[@class='page-section page-section-light']//p[@class='product-new-price has-deal']/text())[1]").get(), 
            'discount-percent': response.xpath("//div[@class='card-v2-badge badge-discount']/text()").get(), 
            'images': imageUrls, 
            'categories': category_values,
            'description-html': response.xpath("normalize-space(//table[@class='table table-striped specifications-table'])").get() 
        }


        
    def get_product_option(self, response):
        oldPrice = response.xpath("(//section[@class='page-section page-section-light']//span[@class='rrp-lp30d-content']/s/text())[1]").get()
        if(not oldPrice):
            oldPrice = response.xpath("normalize-space((//section[@class='page-section page-section-light']//span[@class='rrp-lp30d-content']/text())[1])").get()

        currentProductId = 'emag-'+ response.xpath("normalize-space(//span[@class='product-code-display hidden-xs']/text())").get()

        images = response.xpath("//div[@class='multimedia-gallery hidden-xs multimedia-small-gallery ph-carousel-init ph-has-arrows']/div[@class='thumbnail-wrapper']/a/@href")
        imageUrls = ''

        for image in images:
            imageUrls += "|" + image.get()

        if imageUrls == "":
            imageUrls+= '|' + response.xpath("//a[@class='thumbnail product-gallery-image gtm_rp125918']/@href").get()
        
        if(oldPrice):
            yield{
                'is-product-choice': True,
                'parent-website-id': response.meta.get('parent-website-id'),
                'website-id':currentProductId,
                'product-url': response.request.url, 
                'option-type' : response.meta.get('option-type'),
                'option': response.meta.get('parent-option'), 
                'title': response.xpath("normalize-space(//h1[@class='page-title']/text())").get(), 
                'old-price': oldPrice, 
                'new-price': response.xpath("(//section[@class='page-section page-section-light']//p[@class='product-new-price has-deal']/text())[1]").get(),
                'images': imageUrls, 
                'discount-percent': response.xpath("//div[@class='card-v2-badge badge-discount']/text()").get()  
            }