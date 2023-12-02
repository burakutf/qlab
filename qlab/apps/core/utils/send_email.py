from datetime import datetime
import threading
import logging

from django.conf import settings
from django.core.mail import EmailMessage


logger = logging.getLogger('SEND SMS')


class EmailThread(threading.Thread):
    def __init__(self, subject, html_content, recipient_list, file_path=None):
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = html_content
        self.file_path = file_path
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMessage(
            self.subject,
            self.html_content,
            settings.EMAIL_HOST_USER,
            self.recipient_list,
        )
        msg.content_subtype = 'html'
        if self.file_path is not None:
            msg.attach_file(self.file_path)
        msg.send()


def send_html_mail(subject, html_content, recipient_list, file_path=None):
    if not settings.SEND_EMAIL:
        return
    EmailThread(subject, html_content, recipient_list, file_path).start()


def general_html_content(name, title, text):

    today_time = datetime.today().strftime('%d %b, %Y %H:%M')

    return """
<!DOCTYPE html>
<html lang="tr">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OTBLab Email Confirmation</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #d9d9d9;
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        .container {{
            max-width: 512px;
            margin: 30px auto;
            background-color: #F1EFEF;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            border-radius: 10px;
            overflow: hidden;
        }}

        .header {{
            background-color: #357C8E;
            text-align: center;
            padding: 12px;
        }}

        .header a {{
            display: inline-block;
            text-decoration: none;
        }}

        .header img {{
            width: 45px;
            height: 65px;
        }}

        .profile {{
            display: flex;
            align-items: center;
            border-bottom-style: solid;
            border-color: #EDF0F3;
        }}

        .profile img {{
            width: 36px;
            height: 36px;
            border-radius: 50%;
        }}

        .profile h2 {{
            margin-left: 15px;
            font-weight: 400;
            font-size: 16px;
            color: #4C4C4C;
        }}

        .code-container {{
            padding: 20px 24px;
        }}

        .code-text {{
            margin-bottom: 10px;
            font-weight: 400;
            font-size: 16px;
            color: #4C4C4C;
        }}

        .code {{
            margin-bottom: 10px;
            font-weight: 600;
            font-size: 17px;
            color: #262626;
        }}

        .info-container {{
            padding: 16px 24px;
            background-color: #F1EFEF;
        }}

        .info-title {{
            margin-bottom: 12px;
            font-weight: 700;
            font-size: 14px;
            color: #262626;
        }}

        .info-label {{
            font-weight: 700;
            font-size: 12px;
            color: #737373;
        }}

        .info-value {{
            margin-bottom: 12px;
            font-weight: 400;
            font-size: 12px;
            color: #737373;
        }}

        .footer {{
            background-color: #EDF0F3;
            padding-top: 15px;
            padding-bottom: 15px;
            color: #6A6C6D;
            text-align: center;
            text-decoration: underline;
        }}

        .footer a {{
            color: #6A6C6D;
            text-decoration: none;
        }}

        .usertitle {{
            color: rgb(6, 6, 6);
            font-size: 20px;
        }}
    </style>
</head>

<body>
    <div class="container">
        <div class="header">
            <a href="https://qyazilim.com.tr/">
                <img src="https://i.hizliresim.com/sch0cd4.png" alt="OTBLab Logo">
            </a>
        </div>
        <div class="code-container">
            <div class="profile">
                <p class="usertitle">Merhaba {},</p>
            </div>
            <p class="code-text">{}.</p>
            <h2 class="code">{}</h2>
            <p class="code-text"><a href="https://otb-lab.com/" target="_blank">Detaylı Bilgi İçin Giriş Yapınız.</a></p>
            <p class="code-text">Bize verdiğiniz destek için teşekkür ederiz. Q Yazılım Ekibi</p>
        </div>
        <div class="info-container">
            <h2 class="info-title">Bu ne zaman gerçekleşti?</h2>
            <p class="info-label">Tarih:</p>
            <p class="info-value">{} (GMT)</p>
        </div>
        <div class="footer">
            <p><a href="https://qyazilim.com.tr/" target="_blank">Buna neden yer verdiğimizi öğrenin.</a></p>
        </div>
    </div>
</body>

</html>""".format(
        name,
        title,
        text,
        today_time,
    )
