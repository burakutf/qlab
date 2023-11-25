import os
import locale
from django.conf import settings
import jinja2
import pdfkit
from datetime import datetime
from environ import Env

env = Env()


class WorkOrderGenerator:
    def __init__(
        self,
        items,
        devices,
        proposal_id,
        org_owner,
        left_logo,
        signature,
        company_name,
        company_address,
        company_person,
        company_number,
        company_advisor,
        start_date,
        end_date,
        goal,
        vehicles,
        personal,
        template_path=None,
        html_template='work_order.html',
    ):
        self.personal = personal
        self.vehicles = vehicles
        self.company_name = company_name
        self.company_address = company_address
        self.company_person = company_person
        self.company_number = company_number
        self.company_advisor = company_advisor
        self.start_date = start_date
        self.end_date = end_date
        self.devices = devices
        self.goal = goal
        self.org_owner = org_owner
        self.signature = signature
        self.left_logo = left_logo
        self.items = items
        self.proposal_id = proposal_id
        locale.setlocale(locale.LC_TIME, env.str('LANGUAGE_PATH'))
        self.today_date = datetime.today().strftime('%d %b, %Y')
        if template_path is None:
            template_path = os.path.dirname(os.path.abspath(__file__))
        self.template_loader = jinja2.FileSystemLoader(template_path)
        self.template_env = jinja2.Environment(loader=self.template_loader)
        self.html_template = html_template

    def render_template(self):
        template = self.template_env.get_template(self.html_template)
        context = {
            'goal': self.goal,
            'company_person': self.company_person,
            'company_name': self.company_name,
            'company_address': self.company_address,
            'company_number': self.company_number,
            'company_advisor': self.company_advisor,
            'org_owner': self.org_owner,
            'left_logo': settings.DOMAIN + self.left_logo.url,
            'signature': settings.DOMAIN + self.signature.url,
            'today_date': self.today_date,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'items': self.items,
            'devices': self.devices,
            'proposal_id': self.proposal_id,
            'vehicles': self.vehicles,
            'personal': self.personal,
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
