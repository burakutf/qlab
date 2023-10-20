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
        template_path=None,
        html_template='invoice.html',
        css_file='invoice.css',
    ):
        self.client_name = client_name
        self.items = items
        self.total = sum(
            item['quantity'] * item['unit_price'] for item in items
        )
        kdv = (self.total * vat_rate) / 100
        self.kdv_total = self.total + kdv
        locale.setlocale(locale.LC_TIME, 'tr_TR')
        self.today_date = datetime.today().strftime('%d %b, %Y')
        self.month = datetime.today().strftime('%B')
        if template_path is None:
            template_path = os.path.dirname(
                os.path.abspath(__file__)
            )  # Get the directory of the current script
        self.template_loader = jinja2.FileSystemLoader(template_path)
        self.template_env = jinja2.Environment(loader=self.template_loader)
        self.html_template = html_template
        self.css_file = os.path.join(
            template_path, css_file
        )  # Get the full path to the CSS file

    def render_template(self):
        template = self.template_env.get_template(self.html_template)
        context = {
            'client_name': self.client_name,
            'today_date': self.today_date,
            'kdv_total': self.kdv_total,
            'total': f'TL{self.total:.2f}',
            'month': self.month,
            'items': self.items,
        }
        return template.render(context)

    def generate_pdf(self, output_pdf):
        output_text = self.render_template()
        config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
        pdfkit.from_string(
            output_text, output_pdf, configuration=config, css=self.css_file
        )


# Usage:
items = [
    {
        'name': 'TV',
        'quantity': 31,
        'unit_price': 499.25,
        'description': '42 inch LCD TV',
    },
    {
        'name': 'Couch',
        'quantity': 31,
        'unit_price': 399.50,
        'description': 'Leather couch',
    },
    {
        'name': 'Washing Machine',
        'quantity': 31,
        'unit_price': 1500,
        'description': 'Front load washing machine',
    },
    {
        'name': 'Tesis Taban Fiyatı',
        'quantity': 1,
        'unit_price': 1500,
        'description': 'Lorem Ipsum, kısaca Lipsum, masaüstü yayıncılık ve basın yayın sektöründe kullanılan taklit yazı bloğu olarak tanımlanır. Lipsum, oluşturulacak şablon ve taslaklarda içerik yerine geçerek yazı bloğunu doldurmak için kullanılır.',
    },
    {
        'name': 'Masraf',
        'quantity': 1,
        'unit_price': 1500,
        'description': 'Yol Masrafı',
    },
    {
        'name': 'İskonto',
        'quantity': 1,
        'unit_price': -40500,
        'description': 'Ölçüm Fiyatı üzerinden iskonto',
    },
]
invoice_generator = InvoiceGenerator('Burak Uzun', items, 20)
invoice_generator.generate_pdf('invoice.pdf')
