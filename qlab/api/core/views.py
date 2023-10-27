import locale
from environ import Env

from datetime import datetime

from django.core.cache import cache
from django.db.models import Count, Sum, F, Q
from django.db.models.functions import TruncMonth

from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from qlab.apps.accounts.models import User
from qlab.apps.company.models import Company, Proposal, Vehicle

env = Env()

locale.setlocale(locale.LC_TIME, env.str('LANGUAGE_PATH'))


def get_monthly_data(queryset, date_field, value_field=None):
    data = queryset.annotate(month=TruncMonth(date_field))
    if value_field:
        data = data.annotate(value=Sum(value_field)).values('month', 'value')
    else:
        data = (
            data.values('month')
            .annotate(count=Count('id'))
            .values('month', 'count')
        )
    return [
        {
            'name': item['month'].strftime('%B'),
            'value': item.get('value', item.get('count')),
        }
        for item in data
    ]


def get_monthly_list(months, monthly_data):
    monthly_list = []
    for month in months:
        value = next(
            (
                item['value']
                for item in monthly_data
                if item['name'] == month.strftime('%B')
            ),
            0,
        )
        monthly_list.append(
            {
                'name': month.strftime('%B'),
                'value': value,
            }
        )
    return monthly_list


class StatisticsView(ListAPIView):
    def get(self, request, *args, **kwargs):
        key = 'user-statistics'
        data = cache.get(key)

        if data is not None:
            return Response(data)

        personal_count = User.objects.filter(is_active=True).count()
        vehicles_count = Vehicle.objects.count()
        company_count = Company.objects.count()

        monthly_proposals = get_monthly_data(
            Proposal.objects.all(), 'created_at'
        )
        monthly_earnings = get_monthly_data(
            Proposal.objects.filter(
                Q(parameters__count__isnull=False),
                Q(parameters__parameter__price__isnull=False),
            ),
            'created_at',
            F('parameters__count') * F('parameters__parameter__price'),
        )

        current_year = datetime.now().year
        months = [
            datetime(year=current_year, month=i, day=1) for i in range(1, 13)
        ]

        monthly_proposal_list = get_monthly_list(months, monthly_proposals)
        proposals_earnings = get_monthly_list(months, monthly_earnings)

        data = {
            'personal_count': personal_count,
            'vehicles_count': vehicles_count,
            'company_count': company_count,
            'monthly_proposal': monthly_proposal_list,
            'monthly_earnings': proposals_earnings,
        }
        cache.set(key, data, env.int('CACHE_TIMEOUT', default=30))
        return Response(data)
