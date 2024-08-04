import django_filters
from django.db.models import ForeignKey, DateField, DateTimeField, UUIDField, JSONField


class BaseFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        model_fields = self.Meta.model._meta.fields
        for field in model_fields:
            field_name = field.name
            if isinstance(field, ForeignKey):
                self.filters[field_name] = django_filters.CharFilter(
                    field_name=field_name, lookup_expr="exact"
                )
                # # M2: get all if do not match
                # self.filters[field_name] = django_filters.ModelChoiceFilter(
                #     field_name=field_name, queryset=field.related_model.objects.all(), lookup_expr="exact"
                # )
            elif isinstance(field, JSONField):
                continue
            elif isinstance(field, UUIDField):
                self.filters[field_name] = django_filters.CharFilter(
                    field_name=field_name, lookup_expr="iexact"
                )
            elif field.primary_key:
                self.filters[field_name] = django_filters.NumberFilter(
                    field_name=field_name
                )
            # ## Text fields ===============
            else:
                self.filters[field_name] = django_filters.CharFilter(
                    field_name=field_name, lookup_expr="icontains"
                )
                if isinstance(field, DateField) or isinstance(field, DateTimeField):
                    self.filters[field_name] = django_filters.DateFilter(
                        field_name=field_name, lookup_expr="icontains"
                    )
                    self.filters[field_name + '_range'] = django_filters.DateFromToRangeFilter(
                        field_name=field_name
                    )
