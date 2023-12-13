# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class DiscountbgPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        field_names = adapter.field_names()
        for field_name in field_names:
            if 'price' in field_name:
                value = adapter.get(field_name)
                value = value.replace('лв', '')
                adapter[field_name] = float(value)
            if 'discount-percent' in field_name:
                value = adapter.get(field_name)
                value = value.replace('%', '')
                value = value.replace('-', '')
                adapter[field_name] = float(value)
        return item
        