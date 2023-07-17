from django.db import models

# Create your models here.
# Create your models here.
class Stock(models.Model):
	links=models.CharField(max_length=100,default=None)
	news=models.CharField(max_length=100,default=None)
	sentiment=models.CharField(max_length=100,default=None)

	class Meta:
		app_label = 'SMAUTAFA'
