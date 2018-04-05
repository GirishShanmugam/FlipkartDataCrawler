import scrapy

import flipkart_crawler
from ..items import FlipkartTshirtsMenItem
import json, csv, os
import hashlib


class FlipkartSpider(scrapy.Spider):
    name = "product_category_list_crawler"
    start_urls = [
        'https://www.flipkart.com/men/shirts/pr?otracker=nmenu_sub_Men_0_Shirts&page=2&sid=2oq%2Cs9b%2Cmg4&viewType=grid',
        'https://www.flipkart.com/men/tshirts/pr?otracker=nmenu_sub_Men_0_T-Shirts&page=2&sid=2oq%2Cs9b%2Cj9y&viewType=grid',
        'https://www.flipkart.com/mens-clothing/ethnic-wear/kurtas/pr?otracker=nmenu_sub_Men_0_Kurtas&page=2&sid=2oq%2Cs9b%2C3a0%2Cr6s&viewType=grid',
        'https://www.flipkart.com/mens-clothing/suits-blazers/pr?otracker=nmenu_sub_Men_0_Suits+and+Blazers&page=2&sid=2oq%2Cs9b%2Cq9f&viewType=grid',
        'https://www.flipkart.com/mens-clothing/winter-seasonal-wear/jackets/pr?otracker=nmenu_sub_Men_0_Jackets&page=2&sid=2oq%2Cs9b%2Cqgu%2C8cd&viewType=grid',
        'https://www.flipkart.com/mens-clothing/winter-seasonal-wear/sweatshirts/pr?otracker=nmenu_sub_Men_0_Sweatshirts&page=2&sid=2oq%2Cs9b%2Cqgu%2C8vm&viewType=grid',
        'https://www.flipkart.com/men/jeans/pr?otracker=nmenu_sub_Men_0_Jeans&page=2&sid=2oq%2Cs9b%2C94h&viewType=grid',
        'https://www.flipkart.com/mens-clothing/trousers/pr?otracker=nmenu_sub_Men_0_Trousers&page=2&sid=2oq%2Cs9b%2C9uj&viewType=grid',
        'https://www.flipkart.com/mens-clothing/~shorts-and-capris/pr?otracker=nmenu_sub_Men_0_Shorts+and+3%2F4ths&page=2&sid=2oq%2Cs9b&viewType=grid',
        'https://www.flipkart.com/mens-clothing/cargos-shorts-34ths/cargos/pr?otracker=nmenu_sub_Men_0_Cargos&page=2&sid=2oq%2Cs9b%2Cvde%2Clrd&viewType=grid',
        'https://www.flipkart.com/mens-clothing/sports-wear/track-pants/pr?otracker=nmenu_sub_Men_0_Track+pants&page=2&sid=2oq%2Cs9b%2C6gr%2Crfn&viewType=grid']

    item_id = 1
    page_number = 0

    def parse(self, response):
        # get contents in script tag which has media in it
        self.page_number = response.url[response.url.find('page=')+len('page='):response.url.rfind('&sid')]
        csv_file_name = response.url[:response.url.rfind('/')]
        csv_file_name = csv_file_name[csv_file_name.rfind('/')+len('/'):]
        csv_file_name = 'flipkart_men_' + csv_file_name.replace('/', '_') + '.csv'
        data = response.xpath("//script[contains(., 'media')]/text()").extract_first()
        if data is not None:
            data = data.encode('utf-8')
            data = data.replace('"apiError":{}};\n', '"apiError":{}}')
            data = data.replace('window.__INITIAL_STATE__ = ', '')

            # convert the string to Json object
            raw_json = json.loads(data)
            raw_json = self.convert_keys_to_string(raw_json)

            # write the crawled data to a csv file
            with open(csv_file_name, 'w') as csvfile:
                fieldnames = ['id', 'page_number', 'flipkart_product_id', 'title', 'key_specs', 'analytics_data', 'rating',
                              'file_name', 'url']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                if os.stat(csv_file_name).st_size == 0:
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
                            image_url = image['url'].encode('utf-8').replace('{@width}', '300')
                            image_url = image_url.encode('utf-8').replace('{@height}', '300')
                            image_url = image_url.encode('utf-8').replace('{@quality}', '100')
                            hash_object = hashlib.sha1(image_url)
                            hex_dig = hash_object.hexdigest()
                            writer.writerow({'id': self.item_id, 'page_number': self.page_number, 'flipkart_product_id': flipkart_item_id, 'title': title,
                                             'key_specs': key_specs, 'analytics_data': analytics_data, 'rating': rating,
                                             'file_name': str(hex_dig)+'.jpeg', 'url': image_url})
                            # download the images from the url
                            yield FlipkartTshirtsMenItem(image_urls=[image_url], page_url=response.url)
                            self.item_id = self.item_id+1
                    except Exception as e:
                        print (e)

            # check if next page is available
            next_page = response.css('div._2kUstJ a::attr(href)').extract()[-1]
            if next_page is not None:
                yield response.follow('https://www.flipkart.com'+next_page, callback=self.parse)

        else:
            print ('========STOPPED COLLECTING DATA========')
            print ('ERROR IN COLLECTING DATA FOR ' + response.request.url)

    def convert_keys_to_string(self, dictionary):
        """Recursively converts dictionary keys to strings."""
        if not isinstance(dictionary, dict):
            return dictionary
        return dict((str(k), self.convert_keys_to_string(v))
            for k, v in dictionary.items())