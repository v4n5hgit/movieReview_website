from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Movie(models.Model): # we are creating a table named Movie
    #fields for the Movie table
    name = models.CharField(max_length=350)
    director= models.CharField(max_length=350)
    cast= models.CharField(max_length=1000)
    description= models.TextField(max_length=5000)
    release_date= models.DateField()
    averageRating = models.FloatField(default=0)
    image = models.URLField(default=None, null=True)


    def __str__(self): #function called string returns whatever you want in the string version in django-admin
        return self.name

    def __unicode__(self):
        return self.name

        #now after creating a table we need to register it to admin.py
        #and after making any changes to database we need to run migrations
class reviews(models.Model):
    movieid = models.IntegerField()
    user= models.CharField(max_length=100)
    review = models.TextField(max_length=3000)
    rating = models.FloatField(default=0)
