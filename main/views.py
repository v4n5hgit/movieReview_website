#logic of our code goes here
#any pages you wanna create goes here
from django.shortcuts import render
from django.http import HttpResponse
from .models import *
#function based views
#home page
def home(request): #what the users will see on our front page every view that has to be viewed i the html has to go thru request parameter
    allMovies= Movie.objects.all() # select * from Movie (equivalent SQL query)
    # we need to create a dictionary for our html template. Html file will contain "movies" which will refer to allMovies
    context = {
        "movies" : allMovies,

    }

    return render(request, 'main/index.html', context)

#detail page
def detail(request,id):
    movie= Movie.objects.get(id=id) #select * from Moview where id=id
    context = {
        "movie" : movie
    }

    return render(request, 'main/details.html', context)
