#logic of our code goes here
#any pages you wanna create goes here
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .forms import *
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

#add movies to the databse

def add_movies(request):
    if request.method == "POST":
        form = MovieForm(request.POST or None)

        #check if the form is valid
        if form.is_valid():
            data= form.save(commit=False)
            data.save()
            return redirect("main:home")

    else:
        form =MovieForm()
    return render( request, 'main/addMovies.html' , {"form" : form, "controller" : "Add movie"})

#edit movies details
def edit_movies(request,id):
    movie= Movie.objects.get(id=id) #select * from Moview where id=id
    if request.method == "POST":
        form = MovieForm(request.POST or None, instance=movie)

        if form.is_valid():
            data= form.save(commit=False)
            data.save()
            return redirect("main:detail" , id)
            # important point to note here after main: "<the name of the page that you gave in your urls.py>"

    else:
        form = MovieForm(instance=movie)
    return render(request , 'main/addMovies.html', {"form" : form, "controller" : "Edit Movie"})
