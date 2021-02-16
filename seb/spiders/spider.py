import re

import scrapy

from scrapy.loader import ItemLoader
from ..items import SebItem
from itemloaders.processors import TakeFirst


class SebSpider(scrapy.Spider):
	name = 'seb'
	start_urls = ['https://www.seb.lt/infobankas']

	def parse(self, response):
		post_links = response.xpath('//p[@class="heading"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)


	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@property="content:encoded"]//text()[normalize-space() and not(ancestor::a | ancestor::div[@class="item-list"])]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="content"]/p[@class="info"]/text()').getall()
		date = [p.strip() for p in date]
		date = ' '.join(date).strip()
		if date:
			date = re.findall(r'\d{4}\s\d{2}\s\d{2}', date)[0]

		item = ItemLoader(item=SebItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
