import locale
from environ import Env

from datetime import datetime

from django.core.cache import cache
from django.db.models import Count, Sum, F, Q
from django.db.models.functions import TruncMonth

from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from qlab.apps.accounts.models import User
from qlab.apps.accounts.permissions import PermissionChoice
from qlab.apps.company.models import (
    Company,
    LabDevice,
    Proposal,
    ProposalChoices,
    Vehicle,
)

env = Env()

locale.setlocale(locale.LC_TIME, env.str('LANGUAGE_PATH'))


def get_monthly_data(queryset, date_field, value_field=None):
    data = queryset.annotate(month=TruncMonth(date_field))
    if value_field:
        data = data.annotate(total_count=Sum(value_field)).values(
            'month', 'total_count'
        )
        result = {}
        for item in data:
            if item['month'] in result:
                result[item['month']] += item['total_count']
            else:
                result[item['month']] = item['total_count']

        result = [{'name': k.strftime('%B'), 'value': v} for k, v in result.items()]
        return result
    else:
        data = (
            data.values('month')
            .annotate(total_count=Count('id'))
            .values('month', 'total_count')
        )
    return [
        {
            'name': item['month'].strftime('%B'),
            'value': item.get('value', item.get('total_count')),
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
        has_perm = (
            PermissionChoice.STATISTICS_VIEW in self.request.action_permissions
        )

        if not has_perm:
            raise PermissionDenied(('İstatistik görüntüleme yetkiniz yok!'))

        key = 'user-statistics'
        data = cache.get(key)

        if data is not None:
            return Response(data)

        personal_count = User.objects.filter(is_active=True).count()
        vehicles_count = Vehicle.objects.count()
        company_count = Company.objects.count()
        device_count = LabDevice.objects.count()
        proposal = Proposal.objects.all()
        monthly_proposals = get_monthly_data(proposal, 'created_at')
        monthly_approve_proposals = get_monthly_data(
            proposal.filter(status=ProposalChoices.APPROVAL),
            'created_at',
        )
        monthly_earnings = get_monthly_data(
            proposal.filter(
                Q(parameters__count__isnull=False),
                Q(parameters__parameter__price__isnull=False),
            ),
            'created_at',
            F('parameters__count') * F('parameters__price'),
        )

        current_year = datetime.now().year
        months = [
            datetime(year=current_year, month=i, day=1) for i in range(1, 13)
        ]

        monthly_proposal_list = get_monthly_list(months, monthly_proposals)
        monthly_approval_proposal_list = get_monthly_list(
            months, monthly_approve_proposals
        )
        proposals_earnings = get_monthly_list(months, monthly_earnings)
        data = {
            'personal_count': personal_count,
            'vehicles_count': vehicles_count,
            'company_count': company_count,
            'device_count': device_count,
            'monthly_proposal': monthly_proposal_list,
            'monthly_approval_proposal': monthly_approval_proposal_list,
            'monthly_earnings': proposals_earnings,
        }
        cache.set(key, data, env.int('CACHE_TIMEOUT', default=30))
        return Response(data)
