from django.db import models
from django.db.models import Subquery
from django.utils.translation import gettext_lazy as _
import datetime


class Base(models.Model):
    order = models.IntegerField(_('Sorting'), default=0,
                                        help_text=_('We usualy order a model in a client and an admin part.'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'), null=True, blank=False,
                                   help_text=_('Show when an entry was created.'))
    updated = models.DateTimeField(verbose_name=_('Updated'), auto_now=True, null=True, blank=False,
                                   help_text=_('Show when an entry was updated'))
    is_active = models.BooleanField(_('Public'), default=True,
                                    help_text=_('This entry is visible or unvisible for a client part or admin part.'))
    is_deleted = models.BooleanField(_('Delete status'), default=False)

    class Meta(object):
        abstract = True

    def save(self, *args, **kwargs):
        self.updated = datetime.datetime.now()
        if not self.created:
            self.created = datetime.datetime.now()
        super(Base, self).save(*args, **kwargs)


class SQCount(Subquery):
    template = '(SELECT count(*) FROM (%(subquery)s) _count)'  # noqa: WPS323
    output_field = models.IntegerField()