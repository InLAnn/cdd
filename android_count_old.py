#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import requests
import re
import sys
import xlwings as xw

def match_month(target):
    month_nu = re.findall('-(\d\d)-', target, re.S)
    if month_nu[0][0] is '0':
        month_nu[0] = month_nu[0][1]
    month = month_nu[0] + '月'
    return month

def print_td(h3, date, data, month):
    newL = h3[:]
    source = '未公开源码'
    for i in range(0, len(newL)):
        tr = re.findall('<tr>.*?</tr>', h3[i], re.S)  # tr是每个CVE块组成的列表
        component = re.findall('id="(.*?)"', h3[i], re.S)
        newLL = tr[:]  # newLL是每个CVE块
        newLL.remove(newLL[0])  # 去除newLL中的第一个tr块（标题部分）
        for j in newLL:
            td = re.findall('<td>(.*?)</td>', j, re.S)  # td是一个CVE块中的每个td块作为元素组成的列表（即一个CVE集合）
            if 'href' in td[1]: #检查是否存在源码
                td.append('')
            else:
                td.append(source)

            td.insert(0, component[0])
            td[0] = td[0].capitalize()
            td[0] = td[0].replace('-', ' ')

            if 'Rce' in td[0]:
                td[0] = td[0].replace('Rce', 'Remote code execution vulnerability')
            elif 'Id' in td[0]:
                td[0] = td[0].replace('Id', 'Information disclosure vulnerability')
            elif 'Eop'in td[0]:
                td[0] = td[0].replace('Eop', 'Elevation of privilege vulnerability')
            elif 'Dos' in td[0]:
                td[0] = td[0].replace('Dos', 'Denial of service vulnerability')

            if date == 0:
                td.insert(2, 'Framework')
            elif 'ernel' in td[0]:
                td.insert(2, 'Kernel')
            else:
                td.insert(2, 'Driver')

            td.insert(3, (month[0] + '月'))
            td.remove(td[4])
            td.remove(td[5])
            td.remove(td[5])
            td.insert(-1, ' ')
            td.insert(-1, ' ')
            td.insert(-1, ' ')
            data.append(td)
    return data

def write_excel(data):
    app = xw.App(visible=True, add_book=False)
    wb = app.books.add()
    wb.sheets[0].range('A1').value = data
    wb.save('data.xlsx')
    wb.close()
    app.quit()

def main():
    target = "https://source.android.com/security/bulletin/2016-08-01?hl=en"
    req = requests.get(target)
    output = req.text
    h2 = output.split('security patch level—Vulnerability')
    h2.remove(h2[0])
    data = []
    h3 = h2[0].split('<h3')
    h3.remove(h3[0])
    for date in range(len(h2)):
        h3 = re.findall('<h3.*?</table>', h2[date], re.S)  # h3是每个组件大块
        while '' in h3:  # 清除h3中的空元素
            h3.remove('')
        month = match_month(target)
        print_td(h3, date, data, month)
    write_excel(data)

main()

# if __name__ == '__main__':
#     help = '''[+]Usage:python3 android_count_old.py <url_path>
# [+]Example:python3 android_count_old.py http://source.android.com/security/bulletin/201x-xx-xx?hl=en'''
#     print(help)
#     if len(sys.argv) == 2:
#         target = sys.argv[1]
#         main()
#     else:
#         print('Usage Error')
