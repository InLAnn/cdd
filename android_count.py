# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import requests
import sys
import xlwings as xw

def match_month(target):
    month = re.findall('-(\d\d)-', target, re.S)
    if month[0][0] is '0':
        month[0] = month[0][1]
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
            td.insert(0, component[0])
            td[0] = td[0].capitalize()
            td[0] = td[0].replace('-', ' ')
            if date == 0:
                td.insert(2, 'Framework')
            elif 'Kernel' in td[0]:
                td.insert(2, 'Kernel')
            else:
                td.insert(2, 'Driver')

            vuln_component = ''
            check_vuln_type(td)

            # if td[4] == 'EoP': # check vuln type
            #     vuln_component = 'Elevation of privilege vulnerability in ' + td[0]
            # elif td[4] == 'ID':
            #     vuln_component = 'Information disclosure vulnerability in ' + td[0]
            # elif td[4] == 'RCE':
            #     vuln_component = 'Remote code execution vulnerability in ' + td[0]
            # elif td[4] == 'DoS':
            #     vuln_component = 'Denial of service vulnerability in ' + td[0]
            # else: # td[4] = N/A
            #     vuln_component = 'Vulnerability in ' + td[0]

            td.remove(td[0]) # 针对单个CVE块列表进行修改
            td.remove(td[3])
            td.remove(td[-1])
            td.insert(0, vuln_component)
            td.insert(3, (month[0] + '月'))
            td.append(' ')
            td.append(' ')
            td.append(' ')

            if '#asterisk' in td[4]:  # 确定是否公开源码
                td.append(source)
            else:
                td.append('')
            td.remove(td[4])
            data.append(td)
    return data

def check_vuln_type(td):
    if td[4] == 'EoP':  # check vuln type
        vuln_component = 'Elevation of privilege vulnerability in ' + td[0]
    elif td[4] == 'ID':
        vuln_component = 'Information disclosure vulnerability in ' + td[0]
    elif td[4] == 'RCE':
        vuln_component = 'Remote code execution vulnerability in ' + td[0]
    elif td[4] == 'DoS':
        vuln_component = 'Denial of service vulnerability in ' + td[0]
    else:  # td[4] = N/A
        vuln_component = 'Vulnerability in ' + td[0]
    return vuln_component

def write_excel(data):
    app = xw.App(visible=True, add_book=False)
    wb = app.books.add()
    wb.sheets[0].range('A1').value = data
    wb.save('data.xlsx')
    wb.close()
    app.quit()

def main():
    # target = 'https://source.android.com/security/bulletin/2017-06-01?hl=en'
    req = requests.get(target)
    output = req.text
    # h2 = output.split('security patch level—Vulnerability details</h2>') # h2 确定CVE发布日期是1号还是5号，以此判断是framework层还是driver层，暂不考虑google update部分
    h2 = output.split('security patch level vulnerability details</h2>') #  2018.03开始h2中的内容修改为level vulnerability
    h2.remove(h2[0])
    data = []
    for date in range(len(h2)):
        h3 = re.findall('<h3.*?</table>', h2[date], re.S)  # h3是每个组件大块
        while '' in h3:  # 清除h3中的空元素
            h3.remove('')
        month = match_month(target)
        print_td(h3, date, data, month)

    # data.insert(0,['简要描述', 'ID', '漏洞类型', '日期', '等级', '难度预估', '完成情况', '漏洞披露状态', '备注']) # 视情况添加这一行
    write_excel(data)

if __name__ == '__main__':
    help = '''[+]Usage:python3 android_count.py <url_path>
[+]Example:python3 android_count.py http://source.android.com/security/bulletin/201x-xx-xx?hl=en'''
    print(help)
    if len(sys.argv) == 2:
        target = sys.argv[1]
        main()
    else:
        print('Usage Error')
