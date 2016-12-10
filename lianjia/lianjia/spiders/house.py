import scrapy
import re

class HouseSpider(scrapy.Spider):
    name = 'house'

    print('''
    ================================
    ================================
    ====== CHENG LÜ ===== SEU ======
    ================================
    ================================
    ''')
    def start_requests(self):    
        urls = [
            'http://nj.lianjia.com/ershoufang/gulou/',
            'http://nj.lianjia.com/ershoufang/jianye/',
            'http://nj.lianjia.com/ershoufang/xuanwu/',
            'http://nj.lianjia.com/ershoufang/yuhuatai/',
            'http://nj.lianjia.com/ershoufang/qixia/',
            'http://nj.lianjia.com/ershoufang/jiangning/',
            'http://nj.lianjia.com/ershoufang/pukou/',
        ]
        for url in urls:
            print('''
            ================
            ================
            ==== REGION ====
            ================
            ================''', url)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        # analyse this page
        # url_base = response.urljoin('')
        # yield scrapy.Request(url_base, callback=self.parseHouse)

        print('''
        ================
        ================
        ===== PAGE =====
        ================
        ================''', response)
        # fetch all data
        for res in response.xpath('//li[@class="clear"]'):
            yield {
                'community': res.xpath('.//div[@class="houseInfo"]/a[@data-el="region"]/text()').extract_first(),
                'property':
                res.xpath('.//div[@class="houseInfo"]/text()[last()]').extract_first(),
                'position': res.xpath('.//div[@class="positionInfo"]/text()[normalize-space()]').extract_first(),
                'total': res.xpath('.//div[@class="totalPrice"]/span/text()').extract_first(),
                'unit':
                res.xpath('.//div[@class="unitPrice"]/span/text()').extract_first()
            }


        # get page
        page = response.xpath("//div[@class=\"page-box fr\"]/div[@comp-module=\"page\"]/@page-data").extract_first()
        page_head = response.xpath("//div[@class=\"page-box fr\"]/div[@comp-module=\"page\"]/@page-url").extract_first()

        if page:
            # find the max/current page
            pagePattern = re.compile("\d+")
            mPage = pagePattern.findall(page)
            maxPage = mPage[0]
            curPage = mPage[1]
            print('''
            ++++++++++++++++
            ++++++++++++++++
              PAGE %s GET!
            ++++++++++++++++
            ++++++++++++++++
             TOTAL %s PAGES
            ++++++++++++++++
            ++++++++++++++++
            ''' %(curPage, maxPage))

            # join the next page
            url_root = r'http://nj.lianjia.com'
            pageHeadPattern = re.compile(r"/ershoufang/\w+/\w+")
            url_body = pageHeadPattern.match(page_head)
            if int(curPage)!=int(maxPage):
                next_page = url_root + url_body[0] + str(int(curPage)+1)
                print('go to', next_page)
                yield scrapy.Request(next_page, callback=self.parse)
            else:
                print(page,curPage,maxPage,'COMPLETED!')
        else:
            print('''
            GGGGGGGGGGGGGGGG
            GGGGGGGGGGGGGGGG
            GGGGGGGGGGGGGGGG
            GGGGGGGGGGGGGGGG
            GGGGGGGGGGGGGGGG
            ''', response)
