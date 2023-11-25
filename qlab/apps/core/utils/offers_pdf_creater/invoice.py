import os
import locale
from django.conf import settings
import jinja2
import pdfkit
from datetime import datetime
from environ import Env

env = Env()


class InvoiceGenerator:
    def __init__(
        self,
        client_name,
        items,
        vat_rate,
        preface,
        terms,
        org_owner,
        org_name,
        address,
        phone,
        email,
        left_logo,
        right_logo,
        signature,
        bank_name,
        bank_no,
        bank_branch,
        bank_iban,
        company_name,
        company_address,
        company_person,
        company_number,
        company_email,
        subject,
        template_path=None,
        html_template='invoice.html',
    ):
        self.company_name = company_name
        self.company_address = company_address
        self.company_person = company_person
        self.company_number = company_number
        self.company_email = company_email
        self.subject = subject
        self.org_owner = org_owner
        self.org_name = org_name
        self.address = address
        self.signature = signature
        self.phone = phone
        self.email = email
        self.left_logo = left_logo
        self.right_logo = right_logo
        self.bank_name = bank_name
        self.bank_no = bank_no
        self.bank_branch = bank_branch
        self.bank_iban = bank_iban
        self.preface = preface
        self.client_name = client_name
        self.items = items
        self.terms = terms.replace('\n','<br>')

        self.vat_rate = vat_rate
        self.total = float(
            sum(item['quantity'] * item['unit_price'] for item in items)
        )

        kdv = (self.total * vat_rate) / 100
        self.kdv_total = self.total + kdv
        locale.setlocale(locale.LC_TIME, env.str('LANGUAGE_PATH'))
        self.today_date = datetime.today().strftime('%d %b, %Y')
        self.month = datetime.today().strftime('%B')
        if template_path is None:
            template_path = os.path.dirname(os.path.abspath(__file__))
        self.template_loader = jinja2.FileSystemLoader(template_path)
        self.template_env = jinja2.Environment(loader=self.template_loader)
        self.html_template = html_template

    def render_template(self):
        template = self.template_env.get_template(self.html_template)
        context = {
            'subject': self.subject,
            'company_person': self.company_person,
            'company_name': self.company_name,
            'company_address': self.company_address,
            'company_number': self.company_number,
            'company_email': self.company_email,
            'org_owner': self.org_owner,
            'org_name': self.org_name,
            'address': self.address,
            'phone': self.phone,
            'email': self.email,
            'left_logo': 'https://api.otb-lab.com' + self.left_logo.url,
            'right_logo': 'https://api.otb-lab.com' + self.right_logo.url,
            'signature': 'https://api.otb-lab.com' + self.signature.url,
            'bank_name': self.bank_name,
            'bank_no': self.bank_no,
            'bank_branch': self.bank_branch,
            'bank_iban': self.bank_iban,
            'client_name': self.client_name,
            'preface': self.preface,
            'terms': self.terms,
            'today_date': self.today_date,
            'kdv_total': f'₺{self.kdv_total:.2f}',
            'total': f'₺{self.total:.2f}',
            'month': self.month,
            'items': self.items,
            'vat_rate': self.vat_rate,
        }
        return template.render(context)

    def generate_pdf(self, name):
        output_text = self.render_template()

        config = pdfkit.configuration(wkhtmltopdf=env.str('WKHTMLTOPDF_PATH'))
        if settings.DOMAIN == 'localhost':
            output_path = '/Users/burak/Desktop/projeler/qlab/qlab/media/test.pdf'   # TODO ürün aşamasında bu kontrolü kaldır
        else:
            media_root = settings.MEDIA_ROOT.replace('/media/', '')
            output_path = media_root + settings.MEDIA_URL + name
        pdfkit.from_string(output_text, output_path, configuration=config)
