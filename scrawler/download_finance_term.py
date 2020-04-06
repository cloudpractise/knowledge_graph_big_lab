#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import requests
from lxml import html
from lxml import etree
import csv

#需要爬数据的网址
url="http://www.ghsl.cn/dictionary/ec/dictionary_ec_a.html"

#获得全部Url的列表
url_list =  []
for i in range(97,123):
    url_list.append(url.replace("_a", '_'+chr(i) ))

#创建全部术语的列表
finance_term_list = []
for x in url_list:
    page = requests.get(x)
    if page.status_code == 200:
        print("successfully open url", x)
        tree = html.fromstring(page.text)
        result = tree.xpath('//table[@class="content"]/tr/td/text()')
        # 从Chrome Inspect整个表格为：table class="content",因此，抽取table classs.
        # /html/body/center/table/tbody/tr[2]/td/table/tbody/tr/td[3]/table/tbody/tr[2]/td[2]/p[2]/table/tbody/tr[1]/td[1]/center/b
        # class之下是tbody/tr，但tbody是隐式标记，不被lxml的html识别，因此，直接跟着/tr
        for i in range(len(result)):
            try:
                output_term = result[i]
                output_term = output_term.encode("latin1", 'ignore').decode("gbk",'ignore').replace('\t', '').replace('\n', '')
                print("the value added to finance_term_list is", i, output_term)
                finance_term_list.append(output_term)
                i = i + 1
            except IOError:
                 print("unsuccessfully open url", x)
            continue
print("Before: the value of finance_term_list is ", finance_term_list)
before_removing_none =  len(finance_term_list)

##### 数据清理
## 删除冗余空格
finance_term_list_clean = []
for i in range(len(finance_term_list)):
    if i < (len(finance_term_list) -2):
        if finance_term_list[i] == '   ' and finance_term_list[i+1] == '   ':
            print('skip of appending data', finance_term_list[i] )
        else:
            finance_term_list_clean.append(finance_term_list[i])
    else:
        finance_term_list_clean.append(finance_term_list[i])

## 合并误拆分数据
finance_term_list_clean[104] = finance_term_list_clean[104] + finance_term_list_clean[105]
del finance_term_list_clean[105]
finance_term_list_clean[116] = finance_term_list_clean[116] + '。' + finance_term_list_clean[117]
del finance_term_list_clean[117]
finance_term_list_clean[194] = finance_term_list_clean[194] + finance_term_list_clean[195]
del finance_term_list_clean[195]

# 创建术语表CSV文件，但还是需要手工调整
csv_head = ["English Terms","中文术语","中文定义"]
with open('finance_term_file.csv','w', newline='', encoding='utf-8-sig') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(csv_head)
    for i in range(len(finance_term_list_clean) // 3):
        f_csv.writerow([finance_term_list_clean[3*i],finance_term_list_clean[3*i+1],finance_term_list_clean[3*i+2]])
        print("the data written to csv",finance_term_list_clean[3*i],finance_term_list_clean[3*i+1],finance_term_list_clean[3*i+2])
