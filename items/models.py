from django.db import models
from members.views import User

# Create your models here.

class Item(models.Model):
	name = models.CharField(max_length=200)
	description = models.TextField()
	price = models.FloatField()
	def __str__(self):
		return self.name

class Order(models.Model):
	status = models.IntegerField()
	user = models.ForeignKey(User)
	items = models.ManyToManyField(Item)
	def __str__(self):
		return str(self.id)