import os
import locale
import jinja2
import pdfkit
from datetime import datetime


class InvoiceGenerator:
    def __init__(
        self,
        client_name,
        items,
        vat_rate,
        preface,
        terms,
        template_path=None,
        html_template='invoice.html',
        css_file='invoice.css',
    ):
        self.preface = preface
        self.terms = terms
        self.client_name = client_name
        self.items = items
        self.vat_rate = vat_rate
        self.total = float(
            sum(item['quantity'] * item['unit_price'] for item in items)
        )

        kdv = (self.total * vat_rate) / 100
        self.kdv_total = self.total + kdv
        locale.setlocale(locale.LC_TIME, 'tr_TR')
        self.today_date = datetime.today().strftime('%d %b, %Y')
        self.month = datetime.today().strftime('%B')
        if template_path is None:
            template_path = os.path.dirname(os.path.abspath(__file__))
        self.template_loader = jinja2.FileSystemLoader(template_path)
        self.template_env = jinja2.Environment(loader=self.template_loader)
        self.html_template = html_template
        self.css_file = os.path.join(template_path, css_file)

    def render_template(self):
        template = self.template_env.get_template(self.html_template)
        context = {
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

    def generate_pdf(self, output_pdf, name):
        if not os.path.exists(output_pdf):
            os.makedirs(output_pdf)
        output_pdf = output_pdf + '/' + name
        output_text = self.render_template()
        config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
        pdfkit.from_string(
            output_text, output_pdf, configuration=config, css=self.css_file
        )
        return output_pdf
