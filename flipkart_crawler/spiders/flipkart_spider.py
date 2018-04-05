import scrapy
from ..items import FlipkartTshirtsMenItem
import json, csv, os
import hashlib


class FlipkartSpider(scrapy.Spider):
    name = "product_category_list_crawler"
    start_urls = ['https://www.flipkart.com/men/tshirts/pr?otracker=nmenu_sub_Men_0_T-Shirts&page=50&sid=2oq%2Cs9b%2Cj9y&viewType=grid']
    item_id = 1
    page_number = 0

    def parse(self, response):

        # get contents in script tag which has media in it
        self.page_number = response.url[response.url.find('page=')+len('page='):response.url.rfind('&sid')]
        data = response.xpath("//script[contains(., 'media')]/text()").extract_first()
        if data is not None:
            data = data.encode('utf-8')
            data = data.replace('"apiError":{}};\n', '"apiError":{}}')
            data = data.replace('window.__INITIAL_STATE__ = ', '')

            # convert the string to Json object
            raw_json = json.loads(data)
            raw_json = self.convert_keys_to_string(raw_json)

            # write the crawled data to a csv file
            with open('result.csv', 'a') as csvfile:
                fieldnames = ['id', 'page_number', 'flipkart_product_id', 'title', 'key_specs', 'analytics_data', 'rating',
                              'file_name', 'url']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                if os.stat('result.csv').st_size == 0:
                    writer.writeheader()
                for product in raw_json['productSummary']:
                    try:
                        images_list = raw_json['productSummary'][product]['value']['media']['images']
                        flipkart_item_id = raw_json['productSummary'][product]['value']['itemId']
                        title = raw_json['productSummary'][product]['value']['titles']['title']
                        key_specs = raw_json['productSummary'][product]['value']['keySpecs']
                        analytics_data = raw_json['productSummary'][product]['value']['analyticsData']
                        rating = raw_json['productSummary'][product]['value']['rating']
                        for image in images_list:
                            image = self.convert_keys_to_string(image)
                            # replace the width, height and quality fields in the url
                            image_url = image['url'].encode('utf-8').replace('{@width}', '200')
                            image_url = image_url.encode('utf-8').replace('{@height}', '200')
                            image_url = image_url.encode('utf-8').replace('{@quality}', '100')
                            hash_object = hashlib.sha1(image_url)
                            hex_dig = hash_object.hexdigest()
                            writer.writerow({'id': self.item_id, 'page_number': self.page_number, 'flipkart_product_id': flipkart_item_id, 'title': title,
                                             'key_specs': key_specs, 'analytics_data': analytics_data, 'rating': rating,
                                             'file_name': str(hex_dig)+'.jpeg', 'url': image_url})
                            # download the images from the url
                            yield FlipkartTshirtsMenItem(image_urls=[image_url])
                            self.item_id = self.item_id+1
                    except Exception as e:
                        print e

            # check if next page is available
            next_page = response.css('div._2kUstJ a::attr(href)').extract()[-1]
            if next_page is not None:
                yield response.follow('https://www.flipkart.com'+next_page, callback=self.parse)

        else:
            print '========STOPPED COLLECTING DATA========'
            print 'ERROR IN COLLECTING DATA FOR ' + response.request.url

    def convert_keys_to_string(self, dictionary):
        """Recursively converts dictionary keys to strings."""
        if not isinstance(dictionary, dict):
            return dictionary
        return dict((str(k), self.convert_keys_to_string(v))
            for k, v in dictionary.items())