from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator


class Operation(models.Model):
    class Meta:
        verbose_name = _('operation')
        verbose_name_plural = _('operations')

    code = models.CharField(_('code'), max_length=10)
    title = models.CharField(_('title'), max_length=255, null=True, blank=True)
    subtitle = models.CharField(_('subtitle'), max_length=255, null=True, blank=True)
    term_min = models.PositiveIntegerField(_('term min (inclusive)'), null=True, blank=True)
    term_max = models.PositiveIntegerField(_('term max'), null=True, blank=True)
    amount_min = models.FloatField(_('amount min'), validators=[MinValueValidator(0)], null=True, blank=True)
    amount_max = models.FloatField(
        _('amount max (inclusive)'),
        validators=[MinValueValidator(0)],
        null=True,
        blank=True
    )

    def __str__(self):
        return self.code
