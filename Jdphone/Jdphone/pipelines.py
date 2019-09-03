# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import openpyxl


class JdphonePipeline(object):
    def open_spider(self, spider):  # 在爬虫开启的时候仅执行一次
        if spider.name == 'jdphone':
            self.name_list = []
            self.f = openpyxl.Workbook()
            self.sheet1 = self.f.create_sheet("手机信息")
            self.sheet1.append({"A": "品牌", "B": "型号", "C": "价格", "D": "上市时间", "E": "好评率", "F": "图片", "G": "详情链接"})

    def close_spider(self, spider):  # 在爬虫关闭的时候仅执行一次
        if spider.name == 'jdphone':
            self.f.save("手机6.xlsx")

    def process_item(self, item, spider):
        print("管道开始执行了000000000000000000000000000000000000000000")
        # 过滤出2019年才发布的手机
        if item['year_time'] and item['year_time'][:4:] == "2019" and item['month_time'] != '以官网信息为准':
            # 再过滤出有名字的手机
            if item['name'] and item['name'] not in ['以官网信息为准', '·', '产品名称', '-', '--', '其他', '以官网数据为准', '官网信息为准',
                                                     '以官网为准']:
                # 再过滤出已经查询出来的手机
                if item['name'].upper().replace(" ", "") not in self.name_list:
                    # 再进行双向过滤出已经存在的手机
                    uppname = item['name'].upper().replace(" ", "")
                    if all(uppname not in element.upper().replace(" ", "") and element.upper().replace(" ",
                                                                                                       "") not in uppname
                           for element in self.name_list):
                        self.sheet1.append(
                            {"A": item['brand'], "B": item['name'], "C": item['price'],
                             "D": item['year_time'] + item['month_time'],
                             "E": item['goodrate'], "F": item['image'], "G": item['link']})
                        self.name_list.append(item['name'].upper().replace(" ", ""))
        print("管道执行结束=============================================")
