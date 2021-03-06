from scrapy import Request
import time
import random
from newspaper import Article
from em_report.spiders.base.baseSpider import baseSpider

class winshangspider(baseSpider):
	name = "shangquan"
	allowed_domains = ["winshang.com"]
	start_urls = ['http://news.winshang.com/list-1307.html']

	def parse(self, response):#爬取每个版块的url
		for j in range(1,1000):#测试错误时把数字调小  1000
			website_url = self.start_urls[0][:-5] + '/page-' + str(j) + '.html'
			# print(website_url)
			yield Request(website_url,self.parse_news, dont_filter=True)

	def parse_news(self,response):#构建不同版块的所有页面的url
		news_urls = response.xpath('//div[@class="fzywtt"]/a/@href').extract()
		# print(news_urls)
		for news_url in news_urls:
			yield Request(news_url,self.parse_content,meta = {'url':news_url}, dont_filter=True)

	def parse_content(self,response):
		#对每个页面进行解析
		ID = 'songtengteng'

		# website_name = response.xpath('//*[@id="form1"]/div[7]/div[1]/a[1]/text()').extract_first()
		# print(website_name)

		# website_block = response.xpath('//*[@id="form1"]/div[7]/div[1]/a[3]/text()').extract_first()
		# print(website_block)

		news_url = response.meta['url']
		# print(news_url)

		news_tag = response.xpath('//div[@class="newskey"]//strong//a/text()').extract()
		news_tags = ','.join(news_tag)
		# print(news_tags)

		news_title = response.xpath('//h1/text()').extract_first()
		# print(news_title)

		a = Article(response.meta['url'], language='zh')  # Chinese
		a.download()
		a.parse()
		news_content = a.text
		# print(news_content)

		# 发布时间
		a = random.randint(1, 61)
		if a >= 0 and a < 10:
			a = '0' + str(a)
		else:
			a = str(a)
		publish_time = response.xpath('//div[@class="nly"]/span/text()').extract_first().lstrip().rstrip()
		# print(publish_time)
		year = publish_time[:4]
		month = publish_time[5:7]
		day = publish_time[8:10]
		hour = publish_time[11:13]
		minute = publish_time[14:16]
		publish_time = year + month + day + ' ' + hour + ':' + minute + ':' + a
		# print(publish_time)

		date = str(time.strftime("%Y%m%d"))
		currentTime = str(time.strftime("%H:%M:%S"))
		crawl_time = date + ' ' + currentTime
		# print(crawl_time)

		news_author = response.xpath('//*[@id="form1"]/div[10]/div[2]/div[1]/span[2]/text()').extract_first()[3:]
		# print(news_author)

		yield self.getItem(id = ID,
		                   news_url = news_url,
		                   website_name = '赢商网',
		                   website_block = '商圈',
		                   news_title = news_title,
		                   publish_time = publish_time,
		                   news_author = news_author,
		                   news_tags = news_tags,
		                   news_content = news_content)
		# item = BcspiderItem()
		# item['ID'] = ID
		# item['website_name'] = website_name
		# item['website_block'] = website_block
		# item['news_url'] = news_url
		# item['news_tags'] = news_tags
		# item['news_title'] = news_title
		# item['news_content'] = news_content
		# item['publish_time'] = publish_time
		# item['crawl_time'] = crawl_time
		# item['news_author'] = news_author
		# item['file_urls'] = ''
		#
		# yield item
