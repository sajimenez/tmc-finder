import sys

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator


class OperationManager(models.Manager):
    def find_code(self, term, amount):
        qs = self.get_queryset().filter(
            term_min__lte=term,
            term_max__gt=term,
            amount_min__lt=amount,
            amount_max__gte=amount
        )
        if qs.exists():
            return qs.first().code


class Operation(models.Model):
    class Meta:
        verbose_name = _('operation')
        verbose_name_plural = _('operations')

    code = models.CharField(_('code'), max_length=10)
    title = models.CharField(_('title'), max_length=255, null=True, blank=True)
    subtitle = models.CharField(_('subtitle'), max_length=255, null=True, blank=True)
    term_min = models.PositiveIntegerField(_('minimun term in days (inclusive)'), default=0)
    term_max = models.PositiveIntegerField(_('maximun term in days'), default=2147483647)
    amount_min = models.FloatField(_('minimun amount in UF'), validators=[MinValueValidator(0.0)], default=0.0)
    amount_max = models.FloatField(
        _('maximun amount in UF (inclusive)'),
        validators=[MinValueValidator(0.0)],
        default=sys.float_info.max,
    )

    objects = OperationManager()

    def __str__(self):
        return self.code
