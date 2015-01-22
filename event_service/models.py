from django.db import models
from django.utils.translation import ugettext_lazy as _


class Organization(models.Model):
    """
    Represents an org in the system
    """
    name = models.CharField(max_length=255,
                            verbose_name=_(u'name'),
                            db_index=True)


class Event(models.Model):
    """
    Represents an event
    """
    org = models.ForeignKey(Organization,
                            related_name='owner',
                            verbose_name=_(u'organization'))
    hostname = models.CharField(max_length=255,
                                verbose_name=_(u'hostname'),
                                db_index=True)
    string = models.CharField(max_length=255,
                              verbose_name=_(u'string'))

    created_on = models.DateTimeField(verbose_name=_(u'created on'),
                                      db_index=True)