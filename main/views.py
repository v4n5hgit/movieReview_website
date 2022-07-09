#logic of our code goes here
#any pages you wanna create goes here
from unicodedata import name
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .forms import *
import json
from urllib import response
import requests
#function based views
#home page
apiBaseURL = 'https://api.themoviedb.org/3/'
apiKey = '3d9b4ef8cf0ea93474001f18dabe2e00'

imagebase = 'https://image.tmdb.org/t/p/w300'

#home page
def home(request): #what the users will see on our front page every view that has to be viewed i the html has to go thru request parameter
    # allMovies= Movie.objects.all() # select * from Movie (equivalent SQL query)
    # # we need to create a dictionary for our html template. Html file will contain "movies" which will refer to allMovies
    # context = {
    #     "movies" : allMovies,
    # }
    response = requests.get(apiBaseURL + 'movie/now_playing?api_key=' + apiKey).json()
    popular_movies = response["results"]
    movie_id = []
    for i in popular_movies:
        movie_id.append(i["id"])
    response3 = {}
    for i in movie_id:
        response3[i] = requests.get(apiBaseURL + 'movie/' + str(i) + '?api_key=' + apiKey).json()
    return render(request, 'main/index.html', {'response3' : response3})

#detail page
def detail(request,id):
    # movie= Movie.objects.get(id=id) #select * from Moview where id=id
    # context = {
    #     "movie" : movie
    # }
    response = requests.get(apiBaseURL + 'movie/' + str(id) + '?api_key=' + apiKey).json()
    title = response["title"]
    overview = response["overview"]
    rating = response["vote_average"]
    release = response["release_date"]
    imageurl = imagebase + response["poster_path"]
    if Movie.objects.filter(name=title).exists():
        pass
    else:
        moviedata = Movie(name=title, description=overview, averageRating=rating, release_date=release, image=imageurl)
        moviedata.save()
    # review = reviews.objects.all().filter(movieid = movie_id)
    return render(request, 'main/details.html', {'response':response})

#search a movie

def searchresults(request):
    searchTerm = request.POST.get("searchTerm")
    response = requests.get(apiBaseURL + 'search/movie?api_key=' + apiKey + '&language=en-US&page=1&include_adult=false&query=' + searchTerm).json()
    popular_movies = response["results"]
    movie_id = []
    for i in popular_movies:
        movie_id.append(i["id"])
    response3 = {}
    for i in movie_id:
        response3[i] = requests.get(apiBaseURL + 'movie/' + str(i) + '?api_key=' + apiKey).json()
    return render(request, 'main/search.html/', {'response3' : response3, 'searchTerm':searchTerm})

def review(request):

    movie_id = request.POST.get("movieid")
    response = requests.get(apiBaseURL + 'movie/' + movie_id + '?api_key=' + apiKey).json()
    title = response["title"]
    overview = response["overview"]
    rating = response["vote_average"]
    release = response["release_date"]
    moviedata = movies(movieid=movie_id, title=title, overview=overview, rating=rating, release=release)
    moviedata.save()
    review = reviews.objects.all().filter(movieid = movie_id)
    if request.user.is_authenticated:
        if request.method== "POST":
            form = ReviewForm(request.POST or None)
            if form.is_valid():
                data= form.save(commit= False)
                data.review= request.POST["review"]
                data.rating= request.POST["rating"]
                data.user= request.user
                data.movieid= movie_id
                data.save()
                return redirect("main:detail" , movie_id)
        else:
            form = MovieForm()
        return render(request, 'main/details.html', {'response':response, 'review':review, 'form' : form})
    else:
        return redirect("accounts:login")










































































# def detail(request,id):
#     movie= Movie.objects.get(id=id) #select * from Moview where id=id
#     context = {
#         "movie" : movie
#     }
#
#     return render(request, 'main/details.html', context)
#
# #add movies to the databse
#
# def add_movies(request):
#     if request.user.is_authenticated:
#         if request.user.is_superuser:
#             if request.method == "POST":
#                 form = MovieForm(request.POST or None)
#
#                 #check if the form is valid
#                 if form.is_valid():
#                     data= form.save(commit=False)
#                     data.save()
#                     return redirect("main:home")
#
#             else:
#                 form =MovieForm()
#             return render( request, 'main/addMovies.html' , {"form" : form, "controller" : "Add movie"})
#
#         #if they are not admin
#         else:
#             return redirect("main:home")
#     #if they are not logged in
#     else:
#         return redirect("accounts:login")
#
#
# #edit movies details
# def edit_movies(request,id):
#     if request.user.is_authenticated:
#         if request.user.is_superuser:
#             movie= Movie.objects.get(id=id) #select * from Moview where id=id
#             if request.method == "POST":
#                 form = MovieForm(request.POST or None, instance=movie)
#
#                 if form.is_valid():
#                     data= form.save(commit=False)
#                     data.save()
#                     return redirect("main:detail" , id)
#                     # important point to note here after main: "<the name of the page that you gave in your urls.py>"
#
#             else:
#                 form = MovieForm(instance=movie)
#             return render(request , 'main/addMovies.html', {"form" : form, "controller" : "Edit Movie"})
#         #if they are not admin
#         else:
#             return redirect("main:home")
#     #if they are not logged in
#     else:
#         return redirect("accounts:login")
#
# def delete_movies(request,id):
#     if request.user.is_authenticated:
#         if request.user.is_superuser:
#             movie= Movie.objects.get(id=id)
#             movie.delete()
#             return redirect('main:home')
#         else:
#             return redirect("main:home")
#     #if they are not logged in
#     else:
#         return redirect("accounts:login")
