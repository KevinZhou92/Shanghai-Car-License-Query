import os
import sys
import getopt
import xlrd
import xlwt
from query import get_bid_result, get_vali_code

xls_file = None
for file in os.listdir('./'):
    if file.find('.xls') != -1:
        xls_file = file
        break

try:
    data_sheet = xlrd.open_workbook('./test.xls').sheets()[0]
except Exception as e:
    print(f"-> Error: {e}")

bid_ids, id_nums = list(map(lambda num: str(int(num)), data_sheet.col_values(0, 1))), list(map(str, data_sheet.col_values(2, 1)))
bid_ids, id_nums = bid_ids[:1], id_nums[:1]
query_results = []
for index in range(0, len(bid_ids)):
    retries = 0
    if bid_ids[index] and id_nums[index]:
        bid_id, last4_of_id = bid_ids[index], id_nums[index][-4:]
        id_num = id_nums[index]
        passwd = ''
        bid_amount = ''
        customer_name, bid_count, expire_date, success_bid, bid_time, query_status = get_bid_result(bid_id, last4_of_id)
        while query_status != 0 and retries < 3:
            customer_name, bid_count, expire_date, success_bid, bid_time, query_status = get_bid_result(bid_id, last4_of_id)

        if customer_name:
            query_results.append(list(map(str, [bid_id, passwd, id_num, last4_of_id, customer_name, 
            bid_count, expire_date, success_bid, bid_time, bid_amount])))


results_file = './results.xls'
try:   
    workbook = xlwt.Workbook()  
    data_sheet = workbook.add_sheet('查询结果')    
    data_sheet.write(0, 0, '投标号')
    data_sheet.write(0, 1, '密码')
    data_sheet.write(0, 2, '身份证')
    data_sheet.write(0, 3, '身份证后四位')
    data_sheet.write(0, 4, '客户姓名')
    data_sheet.write(0, 5, '已投次数')
    data_sheet.write(0, 6, '有效截止日期')
    data_sheet.write(0, 7, '是否中标')
    data_sheet.write(0, 8, '出价时间')
    data_sheet.write(0, 9, '出价金额')
    workbook.save(results_file)

    for count, query_result in enumerate(query_results, 1):
        for index, value in enumerate(query_result):
            data_sheet.write(count, index,  value)

    workbook.save(results_file)  
except Exception as e:  
    print(e)  






