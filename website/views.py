# -*- coding: utf-8 -*
import os
import csv
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
import imdb
from imdby.imdb import imdb as imdby


@login_required(login_url='/login/')
def main(request):
    bad_title = ""
    check_bad = False
    list_find_films = []
    list_id_films = []
    dict_find_films = {}
    if request.method == "POST":

        # film = Film.objects.filter(name=request.POST.get("title"))
        """if film:
                    print(len(film), str(film))
                    if len(film) > 1:
                        bad_title = request.POST.get("title")
                        check_bad = True
                    else:
                        print(Film_with_user.objects.get(film=film, user=request.user.id))
                        if len(Film_with_user.objects.filter(film=film, user=request.user.id)) == 0:
                            film_with_user = Film_with_user()
                            user = User.objects.get(id=request.user.id)
                            film_with_user.user = user
                            film_with_user.film = film
                            film_with_user.save()
                            print("TRUE", film_with_user)"""
        ia = imdb.IMDb()
        name = request.POST.get("title")
        search = ia.search_movie(name)
        print(dir(search))
        for i in search:
            print(i.movieID)
            print(i)
            try:
                Film.objects.get(id_title=i.movieID)
                # if len(Film_with_user.objects.get(film=film, user=request.user.id)):
                #    print("!!!!!")
            except Film.DoesNotExist:
                small_dict_films = {}
                small_dict_films.update({"id": i.movieID})
                small_dict_films.update({"title": i})
                list_find_films.append(small_dict_films)
                # list_id_films.append(i.movieID)

            # print(dir(i))
            # print(details.genre)
            # al = ia.get_movie(i.movieID)
            # print(al, "###")
            # print(i.genre)
        # bad_title = request.POST.get("title")
        # check_bad = True

    user = User.objects.get(id=request.user.id)
    films = Film_with_user.objects.filter(user=user)
    all_durations = 0
    for el in films:
        all_durations += el.film.duration
        # print(el.film.name)
    all_durations_h = round(all_durations / 60, 2)
    return render(request, 'main.html', {"films": films, "all_durations": all_durations,
                                         "check_bad": check_bad, "bad_title": bad_title,
                                         "all_durations_h": all_durations_h, "list_find_films": list_find_films,
                                         "list_id_films": list_id_films})


@login_required(login_url='/login/')
def add_vie(request, pk):
    print(pk)
    film = Film()
    film.id_title = pk
    from imdby.imdb import imdb as im
    details = im(f'tt{pk}')
    # print(dir(details))
    film.name = details.title
    # print(details.budget, details.movie_release_year, details.film_length)
    film.year = details.movie_release_year
    film.budget = details.budget
    film.rating = details.rating
    # print(details.sound_mix)
    # print("time:", details.film_length," ### ", details.runtime)
    print(list(details.runtime))
    # dur_str = ''
    ch = False
    string_runtime = details.runtime
    print(string_runtime, string_runtime.split(" "))
    list_string_duration = []
    for elem in string_runtime.split(" "):
        string_duration = ''
        for num in elem:
            try:
                int(num)
                string_duration += num
            except:
                pass
        if string_duration != "":
            list_string_duration.append(int(string_duration))
    film.duration = max(list_string_duration)
    print(list_string_duration)
    # print(dur_str)
    # print(" ### ", details.rating)
    # print(details.imdb_movie_metadata)
    # print(details.imdb_technical_spec_metadata)
    try:
        Film.objects.get(id=film.id)
        # if len(Film_with_user.objects.get(film=film, user=request.user.id)):
        #    print("!!!!!")
    except Film.DoesNotExist:
        print("NO")
        film.save()
    try:
        print(Film_with_user.objects.get(film=film, user=request.user.id))
        # if len(Film_with_user.objects.get(film=film, user=request.user.id)):
        #    print("!!!!!")
    except Film_with_user.DoesNotExist:
        film_with_user = Film_with_user()
        user = User.objects.get(id=request.user.id)
        film_with_user.user = user
        film_with_user.film = film
        film_with_user.save()
    # print(details.name, details.year, dir(details))
    return render(request, 'add_film.html')


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


def cr_db(request):
    """
    class Film(models.Model):
        id_title = models.CharField(max_length=100000)
        name = models.CharField(max_length=10000)
        year = models.CharField(max_length=10000)
        genre = models.CharField(max_length=10000)
        country = models.CharField(max_length=10000)
        budget = models.CharField(max_length=10000)
        duration = models.IntegerField(default=10)
        rating = models.DecimalField(max_digits=5, decimal_places=3)
    """
    # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nirla.settings") #nirla is the name of the project
    # print(Film.objects.all())
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    path_start = '{}'.format(cur_dir)
    with open(f'{path_start}\movies.csv', "r", encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        # print(csv_reader)
        for index, row in enumerate(csv_reader):
            try:
                if len(Film.objects.filter(id_title=row["imdb_title_id"])) != 0:
                    continue
                # print(row)
                film = Film()
                film.id_title = row["imdb_title_id"]
                # print(row["imdb_title_id"], "!")
                film.name = row["title"]
                # print(row["title"], "@")
                film.year = row["year"]
                # print(row["year"], "$")
                film.genre = str(row["genre"])
                # print(str(row["genre"]), type(row["genre"]), "%")
                film.country = row["country"]
                # print(row["country"], "*")
                film.budget = row["budget"]
                # print(row["budget"], "###")
                film.duration = row["duration"]
                # print(row["duration"], "____")
                film.save()
            except UnicodeDecodeError:
                pass
    return HttpResponseRedirect("/")
