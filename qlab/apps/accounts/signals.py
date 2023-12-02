from datetime import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver

from qlab.apps.core.utils.send_email import send_html_mail

from .models import User, UserDetail


@receiver(post_save, sender=User)
def user_notification(instance, created, *args, **kwargs):
    if not created:
        return
    today_time = datetime.today().strftime('%d %b, %Y %H:%M')
    UserDetail.objects.create(user=instance)

    if instance.email:
        send_html_mail(
            subject='OTBLab Giriş Bilgileri',
            recipient_list=(instance.email,),
            html_content="""
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
            width: 80px;
            height: 80px;
        }}

        .profile {{
            display: flex;
            align-items: center;
            padding: 5px;
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
            font-weight: 700;
            font-size: 20px;
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
            <p class="code-text">Kimliğinizi doğrulamak ve OTBLab hesabınıza erişim sağlamak için aşağıdaki kullanıcı adı
                parolayı kullanabilirsiniz.</p>
            <h2 class="code">Kullanıcı Adı: {}</h2>
            <h2 class="code">Parola: {}</h2>
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
                instance.full_name,
                instance.username,
                instance.password,
                today_time,
            ),
        )
