#from django.db import models
from django.contrib.gis.db import models

# Create your models here.

class DamLevels(models.Model):
    Id = models.IntegerField(primary_key=True)
    Dam = models.CharField(max_length=100)
    ThisWeek = models.DecimalField(max_digits=5, decimal_places=2)
    LastWeek = models.DecimalField(max_digits=5, decimal_places=2)
    LastYear = models.DecimalField(max_digits=5, decimal_places=2)
    CreationDate = models.DateTimeField()
    geom = models.PointField()

    def __str__(self):
        return self.Dam

    class Meta:
        verbose_name_plural = 'DamLevels'

