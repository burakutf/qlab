import os
from django.conf import settings
import threading
import jinja2
import pdfkit
from environ import Env

env = Env()


class BarcodeGenerator(threading.Thread):
    def __init__(
        self,
        items,
        template_path=None,
        html_template='barcode.html',
    ):

        self.items = items

        if template_path is None:
            template_path = os.path.dirname(os.path.abspath(__file__))
        self.template_loader = jinja2.FileSystemLoader(template_path)
        self.template_env = jinja2.Environment(loader=self.template_loader)
        self.html_template = html_template

    def render_template(self):
        template = self.template_env.get_template(self.html_template)
        context = {
            'items': self.items,
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
