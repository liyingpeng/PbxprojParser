#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 第三方 SMTP 服务
mail_host = "email.baidu.com"  # 设置服务器
mail_user = "liyingpeng"  # 用户名
mail_pass = "Ee1992323123eE"  # 口令

sender = 'liyingpeng@baidu.com'
# receivers = ['cid-app@baidu.com', 'zhuojunhui@baidu.com', 'liumiao@baidu.com', 'lixiaopeng04@baidu.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
# receivers = ['liyingpeng@baidu.com', 'lixiaopeng04@baidu.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
receivers = ['liyingpeng@baidu.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱


def send(msg):
    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    # html = """
    # <p color='red'>Python 邮件发送测试...</p>
    # <p><a href="http://www.runoob.com">这是一个链接</a></p>
    # """
    message = MIMEText(msg, 'html', 'utf-8')

    message['From'] = Header("liyingpeng@baidu.com", 'utf-8')
    message['To'] = Header(','.join(receivers), 'utf-8')
    subject = 'cid-app团队代码复用率统计'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.ehlo
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print "邮件发送成功"
        smtpObj.close()
    except smtplib.SMTPException:
        print "Error: 无法发送邮件"
    pass
