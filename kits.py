import scrapy
import pprint
import re
from kititems import kitItem

class lbSpider(scrapy.Spider):
    # spider name
    name = 'lb'

    # settings for output file
    # automatically quotes strings with commas so need to mess with delimiters
    custom_settings = {
            'FEED_FORMAT': 'csv',
            'FEED_URI': 'kits.csv'
            }

    allowed_domains = ['littlebits.cc']
    start_urls = ['http://littlebits.cc/shop/kits']

    # parses the kits home page
    def parse(self, response):
        for entry in response.xpath("//div[@class='ShopCard-content']"):

            # construct the detail page url
            bitpage_rel = entry.xpath('a/@href').extract_first()
            kitlink = response.urljoin(bitpage_rel)

            # extract basic info for the kits
            kitname = entry.xpath('a/h3/text()').extract_first()
            kitretailprice = entry.xpath("h4/span/text()").extract_first()
            kitdescription = entry.xpath("p/text()").extract_first()

            # callback for fetching additional details
            request = scrapy.Request(kitlink, callback=self.parse_item_page)

            # the simplest way to share data with the callback function
            # each shared variable needs to be accessed through 'meta' in both the caller and the callee
            request.meta['kitretailprice'] = kitretailprice
            request.meta['kitname'] = kitname
            request.meta['kitdescription'] = kitdescription

            # using 'yield' instead of 'return' - generators weigh less
            yield request

    # callback to parse details for each kit from the detail page
    def parse_item_page(self, response):
        for p in response.xpath("//div[@class='KitPartSlide-content u-textCenter']"):
            # items to be persisted in csv being initialized in callback instead as each kit has lots of bits
            item = kitItem()

            # the simplest way to share data with the callback function
            # each shared variable needs to be accessed through 'meta' in both the caller and the callee
            item['kitname'] = response.meta['kitname']
            item['kitlink'] = response.url
            item['kitretailprice'] = response.meta['kitretailprice']
            item['kitdescription'] = response.meta['kitdescription']

            # bitname contains bit count when kits have more than one of the same bit
            bitname = p.xpath('p/text()').extract_first()

            # find the bitcount number within the bitname
            bitcount = re.search('\((\d+)\)', bitname)
            if bitcount:
                #print "FOUND " + bitcount.group(1)
                item['bitcount'] = bitcount.group(1) # extract the bitcount
                item['bitname'] = re.sub('\((\d+)\)',"", bitname) # remove the parentheses and bitcount from bitname
            else:
                item['bitcount'] = 1 # if there is no bitcount availablem assume 1
                item['bitname'] = bitname

            # debug    
            #if bitname.endswith(')'):
            #    if bitname[-2].isnumeric():
            #        print bitname.rfind('(')
            #        print bitname.rfind(')')
            yield item
