import datetime
from django.contrib.gis.db import models
from us_counties.models import County
from unemployment.managers import *


class CountyByMonth(models.Model):
    """
    The unemployment data in county in a particular month.
    """
    # The time and place
    county = models.ForeignKey(County)
    year = models.IntegerField()
    month = models.IntegerField()

    # The goodies
    labor_force = models.IntegerField()
    employment = models.IntegerField()
    unemployment = models.IntegerField()
    unemployment_rate = models.FloatField()

    # The boring stuff
    is_seasonally_adjusted = models.BooleanField('seasonally adjusted')
    is_preliminary = models.BooleanField('preliminary')
    benchmark = models.CharField(max_length=150)
    
    # Managers
    objects = models.GeoManager()
    adjusted = SeasonallyAdjustedManager()
    unadjusted = UnadjustedManager()
    
    class Meta:
        ordering = ('county', 'year', 'month',)
        verbose_name = 'County by Month'
        verbose_name_plural = 'Counties by Month'
        
    def __unicode__(self):
        return u'%s %s-%s' % (self.county, self.year, self.month)
        
    def get_month_display(self):
        """
        Return the month in AP style.
        """
        from django.utils.dateformat import format
        return format(datetime.date(2010, self.month, 01), 'N')
        
    def get_month_obj(self):
        """
        Return the month as a datetime object.
        """
        return datetime.datetime(self.year, self.month, 1)
        
    def get_next_month(self):
        """
        Return the month after this one.
        """
        from dateutil.relativedelta import relativedelta
        return self.get_month_obj() + relativedelta(months=+1)
    
    def get_previous_month(self):
        """
        Return the month before this one.
        """
        from dateutil.relativedelta import relativedelta
        return self.get_month_obj() + relativedelta(months=-1)
