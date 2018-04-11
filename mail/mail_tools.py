# -*- coding: utf-8 -*-

import smtplib
import email.MIMEMultipart
import email.MIMEText
import email.MIMEBase
import os.path

def mail_to(smtp_server,sender,receviers,subject,text,file_name):
    server = smtplib.SMTP(smtp_server)
    main_msg = email.MIMEMultipart.MIMEMultipart()
    text_msg = email.MIMEText.MIMEText(text)
    main_msg.attach(text_msg)
    contype = 'application/octet-stream'
    maintype, subtype = contype.split('/', 1)

    data = open(file_name, 'rb')
    file_msg = email.MIMEBase.MIMEBase(maintype, subtype)
    file_msg.set_payload(data.read( ))
    data.close( )
    email.Encoders.encode_base64(file_msg)

    basename = os.path.basename(file_name)
    file_msg.add_header('Content-Disposition',
        'attachment', filename = basename)
    main_msg.attach(file_msg)

    main_msg['From'] = sender
    main_msg['To'] = ','.join(receviers)
    main_msg['Subject'] = subject
    main_msg['Date'] = email.Utils.formatdate( )

    fullText = main_msg.as_string( )

    server.sendmail(sender, receviers, fullText)
    server.quit()

def send_mail(users, local_file):
    mail_to('smtp.yidian.com', 'dataplatform@yidian-inc.com', ['%s@yidian-inc.com' % i for i in users.split(',')], '[用户画像]'+local_file, '[用户画像查询结果]', local_file)


