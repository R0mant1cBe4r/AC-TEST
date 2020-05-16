# coding=utf-8

# __Author__: Be4r

import nmap
import json
import datetime
import xlsxwriter
import time
import sys
#reload(sys)
#sys.setdefaultencoding('utf8')


#创建一个excel
#workbook = xlsxwriter.Workbook(u'公网业务口开放情况.xlsx')
#创建一个sheet
#worksheet = workbook.add_worksheet('端口开放')

#写入字段名
def write_to_param(row_num):
    headings = ['DOMAIN','IP','PORT','STATE','SERVICE','VERSION']
    worksheet.write_row('A'+str(row_num), headings)

#写入port细节
def write_port_detail(row_num, port_select):
    worksheet.write_row('A'+str(row_num),port_select)

#创建nmap扫描
def scan(ip):
    nm = nmap.PortScanner()
    nmap_dict = nm.scan(hosts=ip, arguments='-sV -p 1-65535')
    #nmap_dict = nm.scan(arguments='-p 1-65535 -v -iL '+path)
    #scan_result = nm[ip]
    #print nm.command_line()
    #print scan_result
    return nmap_dict

#获取port细节
def get_port_detail(port, ip_port_dict):
    port_detail_list = []
    port_detail_list.append(str(port)+"/tcp")
    port_detail_list.append(ip_port_dict[port]['state'])
    port_detail_list.append(ip_port_dict[port]['name'])
    if ip_port_dict[port]['product'] == "" and ip_port_dict[port]['version'] =="" and ip_port_dict[port]['extrainfo'] == "":
        port_detail_list.append(" ")
    elif ip_port_dict[port]['product'] == "" and ip_port_dict[port]['version'] =="" and ip_port_dict[port]['extrainfo'].strip():
        port_detail_list.append("("+ip_port_dict[port]['extrainfo']+")")
    elif ip_port_dict[port]['product'].strip() and ip_port_dict[port]['version'] =="" and ip_port_dict[port]['extrainfo'] == "":
        port_detail_list.append(ip_port_dict[port]['product'])
    elif ip_port_dict[port]['product'].strip() and ip_port_dict[port]['version'].strip() and ip_port_dict[port]['extrainfo'] == "":
        port_detail_list.append(ip_port_dict[port]['product']+" "+ip_port_dict[port]['version'])
    elif ip_port_dict[port]['product'] == "" and ip_port_dict[port]['version'].strip() and ip_port_dict[port]['extrainfo'].strip():
        port_detail_list.append(ip_port_dict[port]['version']+" ("+ip_port_dict[port]['extrainfo']+")")
    else:
        port_detail_list.append(ip_port_dict[port]['product']+" "+ip_port_dict[port]['version']+" ("+ip_port_dict[port]['extrainfo']+")")

    return port_detail_list

#从txt中获取domain清单
def getDomain(path):
    domain = []
    f = open(path,'r')
    line = f.readline()
    while line:
        l = str(line).strip()
        domain.append(l)
        line = f.readline()
    f.close()
    return domain

#进度条展示
def get_progress_bar(id,num):
    percent = 1.0 * id / num * 100
    print ('complete   percent:%.2f' % percent + '%',)   
    sys.stdout.write("\r")
    time.sleep(0.1)
    
if __name__== "__main__":
    
    starttime = datetime.datetime.now()

    #print ('Start port service scan...')
    #ip_port_dict = scan("nmap.txt")['scan']
    #print ('End of port service scan, start collating data...')

    domain = getDomain('nmap.txt')
    txt = open('port.txt','w')

    #ip数目
    ip_num = len(domain)
    #标记ip存活数
    ip_up_num = 0
    #标记ip未存活数
    ip_down_num = []
    #标记写入excel行数
    row_num = 1

    row = 1

    #write_to_param(row_num)
    #row_num += 1

    txt.write('[\'DOMAIN\',\'IP\',\'PORT\',\'STATE\',\'SERVICE\',\'VERSION\']\n')
    txt.flush()

    for dom in domain:
        print (str(row)+': Start "' + dom + '" port service scan...')
        txt.write(str(row)+': Start "' + dom + '" port service scan...')
        txt.flush()
        ip_port_dict = scan(dom)['scan']

        for ip in ip_port_dict:
            try:
                #port升序
                ip_port_sort = sorted(ip_port_dict[ip]['tcp'])

                #ip_row = [ip,'','','','']
                #txt.write(str(ip)+'\n')
                #txt.flush()
                #worksheet.write_row('A'+str(row_num),ip_row)
                #row_num += 1
                #write_to_param(row_num)
                #row_num += 1
                #print nmap_dict

                #遍历获取all ports数据
                for port in ip_port_sort:
                    port_detail_list = get_port_detail(port,ip_port_dict[ip]['tcp'])
                    port_detail_list.insert(0,ip)
                    port_detail_list.insert(0,ip_port_dict[ip]['hostnames'][0]['name'])
                    #write_port_detail(row_num, port_detail_list)
                    print (port_detail_list)
                    txt.write(str(port_detail_list)+'\n')
                    txt.flush()
                    row_num += 1
        
                #ip_row[:] = []
                ip_up_num += 1

            except:
                ip_down_num.append(str(ip))
                #continue
        row += 1

    endtime = datetime.datetime.now()
    #workbook.close()
    txt.close()
    print (' * It takes time: ' + str((endtime-starttime).seconds) + 's')
    print (' * Sum of hosts: ' + str(ip_num) + '; Live hosts: ' + str(ip_up_num))
    print (' * Non-live hosts: ' + str(ip_down_num))