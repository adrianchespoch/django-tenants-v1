from django.db.models import JSONField
from django_filters import rest_framework as filters

from backend.shared.filters.filters import BaseFilter
from users.models.extended_group_model import ExtendedGroup


class ExtendedGroupFilter(BaseFilter):
    class Meta:
        filter_overrides = {
            JSONField: {
                'filter_class': filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
        }
        model = ExtendedGroup
        fields = '__all__'
