# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class DefaultValuesPipeline(object):
    def process_item(self, item, spider):
        for field in item.fields:
            item.setdefault(field, None)
            if field == 'third_party_prices':
                item.setdefault(field, [])