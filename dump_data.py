#! /usr/bin/python3
#1连接数据库并查询 2使用查询结果构造excel表格 3将excel表格发送到邮箱 4空结果不生成表格发送
#查询语句 SELECT full_name, phone, email, gender, owner_id, created_at FROM contacts WHERE owner_type='Member' AND deleted_at IS NULL and created_at >= '#{today}'；
#所需字段 "公司名称", "联系人名称", "联系人注册电话", "联系人注册邮件", "创建时间"

import os
import psycopg2
import time
from envelopes import Envelope
import xlsxwriter

#全局变量num用于判断是否有新用户
num = 0


def generate_file():
    global num
    #获取当天日期
    today = time.strftime("%Y-%m-%d",time.localtime())
    #连接数据库并查询
    conn = psycopg2.connect(database="xxxxxxx", user="xxxxxx", password="xxxxx", host="xxxxx", port="5432")
    cur = conn.cursor()
    #today
    cur.execute("select enterprises.name,contacts.full_name,contacts.phone,contacts.email,contacts.created_at from contacts,members,enterprises where cast(contacts.owner_id as int)=members.id and members.enterprise_id=enterprises.id and contacts.owner_type='Member' and contacts.deleted_at is null and contacts.created_at >= %s",(today,))
    #a specific date
    #cur.execute("select enterprises.name,contacts.full_name,contacts.phone,contacts.email,contacts.created_at from contacts,members,enterprises where cast(contacts.owner_id as int)=members.id and members.enterprise_id=enterprises.id and contacts.owner_type='Member' and contacts.deleted_at is null and contacts.created_at >= '2017-02-03'")
    rows = cur.fetchall()
    #cursor.fetchall() 这个例程获取所有查询结果（剩余）行，返回一个列表。空行时则返回空列表。
    #进行列表是否为空判断,不为空则构造xlsx表格
    if rows:
         workbook = xlsxwriter.Workbook('/tmp/icc_data.xlsx')  # 建立文件
         worksheet = workbook.add_worksheet()  # 建立sheet
         column = ["公司名称", "联系人名称", "联系人注册电话", "联系人注册邮件", "创建时间"]
         worksheet.write_row("A1",column)
         for row in rows:
          num += 1
          format_time = row[4].strftime("%Y-%m-%d %H:%M:%S")
          data = [row[0],row[1],row[2],row[3],format_time]
          n = num + 1
          col = "A%d" % n
          worksheet.write_row(col,data)
         workbook.close()
    conn.close()


#发送邮件
def send_mail(mail_list, subject, mail_body):
    envelope = Envelope(
        from_addr=('xxx@gmail.com', 'xxxx'),
        to_addr=(mail_list),
        cc_addr=(['xxx@gmail.com']),
        subject=subject,
        html_body=mail_body
    )
    # 发送附件
    if os.path.isfile("/tmp/xxx.xlsx"):
        envelope.add_attachment('/tmp/xxx.xlsx',mimetype='application/vnd.ms-excel')
    envelope.send('smtp.exmail.gmail.com', login='xxx@gmail.com', password='xxxxx', tls=True)



if __name__ == '__main__':
    generate_file()
    mail_address = [u'yyy@gmail.com']

    subject = '用户数据导出'
    if num == 0:
        html_body = "无新增用户"
    else:
        html_body = "有%d个新增用户" % num
    send_mail(mail_address, subject, html_body)
