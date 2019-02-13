# -*- coding: utf-8 -*-
import scrapy
import json
import pandas as pd


class DataAnalystSpider(scrapy.Spider):
    name = 'data_analyst'
    allowed_domains = ['www.lagou.com']
    start_urls = ['http://www.lagou.com/']

    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'Connection': 'keep-alive',
            'Host': 'www.lagou.com',
            'origin': 'https://www.lagou.com',
            'referer': 'https://www.lagou.com/jobs/'
                       'list_%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90?labelWords=&fromSearch=true&suginput=',
            'X-Requested-With': 'XMLHttpRequest'
        }
    }

    def start_requests(self):
        request_url = "https://www.lagou.com/jobs/positionAjax.json?" \
                      "city=%E6%B7%B1%E5%9C%B3&needAddtionalResult=false"
        form_data = {
            "first": "false",
            "pn": "",         # 表示页码，需要改变
            "kd": "数据分析"
        }

        cookies = {'JSESSIONID': 'ABAAABAAAGFABEF627883382DF4728CF42B79411832ADDE',
                   ' _ga': 'GA1.2.819692420.1545786412',
                   ' _gid': 'GA1.2.303725459.1545786412',
                   ' user_trace_token': '20181226090656-89c5e5f5-08aa-11e9-b0a4-525400f775ce',
                   ' LGUID': '20181226090656-89c5eb4e-08aa-11e9-b0a4-525400f775ce',
                   ' index_location_city': '%E6%B7%B1%E5%9C%B3',
                   ' Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1545786412,1545786816',
                   ' TG-TRACK-CODE': 'search_code',
                   ' SEARCH_ID': 'c7e0f30bf23b49508328a343b8722c05',
                   ' LGRID': '20181226095740-a07b3179-08b1-11e9-ad84-5254005c3644',
                   ' Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1545789457'}

        for page in range(20):
            form_data['pn'] = str(page + 1)
            yield scrapy.FormRequest(
                url=request_url,
                formdata=form_data,
                cookies=cookies,
                callback=self.parse
            )

    def parse(self, response):
        if response:

            my_json = json.loads(response.text)
            result = (my_json
                      .get('content')
                      .get('positionResult')
                      .get('result'))

            def get_page(a_json):
                return a_json.get('content').get('pageNo')

            df = pd.DataFrame({'content': result})
            df.to_csv(f"result-{get_page(my_json)}.txt",
                      index=False)






