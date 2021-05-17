# -*- coding: utf-8 -*
"""views"""
import os
import requests
import csv
# from django.contrib.auth import authenticate, login
# from django.http import HttpResponse
# from django.http import HttpResponseNotFound
import imdb
from imdby.imdb import imdb as search_film_detail
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from .models import Film, Film_with_user, User


def add_film(title_id, request):
    try:
        film = Film.objects.get(id_title=title_id)
    except Film.DoesNotExist:
        film = Film()
        film.id_title = title_id
        details = search_film_detail(f'tt{title_id}')
        if details.movie_release_year is None and details.released_dates is None:
            return 0
        film.name = details.title
        # print(dir(details))
        if details.movie_release_year is None:
            film.year = details.released_dates[0].split()[-1]
        else:
            film.year = details.movie_release_year
        if details.budget is None:
            film.budget = 0
        else:
            film.budget = details.budget
        film.rating = details.rating
        # print(details.sound_mix)
        # print("time:", details.film_length," ### ", details.runtime)
        print(list(details.runtime), details.runtime)
        string_runtime = details.runtime
        list_string_duration = []
        print(string_runtime)
        for elem in string_runtime.split(" "):
            string_duration = ''
            for num in elem:
                try:
                    int(num)
                    string_duration += num
                except ValueError:
                    pass
            if string_duration != "":
                list_string_duration.append(int(string_duration))
        if "episodes" in string_runtime:
            print("!!!")

            print(string_runtime, string_duration.split("episodes"))
            print(int(list_string_duration[0]) * int(list_string_duration[1]))
            film.duration = int(list_string_duration[0]) * int(list_string_duration[1])
        else:
            film.duration = max(list_string_duration)
        print(list_string_duration)
        # print(dur_str)
        # print(" ### ", details.rating)
        # print(details.imdb_movie_metadata)
        # print(details.imdb_technical_spec_metadata)
        film.save()
    try:
        Film_with_user.objects.get(film=film, user=request.user.id)
        # if len(Film_with_user.objects.get(film=film, user=request.user.id)):

    except Film_with_user.DoesNotExist:
        film_with_user = Film_with_user()
        film_with_user.user = User.objects.get(id=request.user.id)
        film_with_user.film = film
        film_with_user.save()


@login_required(login_url='/login/')
def main(request):
    check_bad = False
    list_find_films = []
    list_id_films = []
    if request.method == "POST":
        print(request.POST.get("add_film"))
        if request.POST.get("add_film") is not None:
            title_id = request.POST.get("add_film")
            add_film(title_id, request)
            user = User.objects.get(id=request.user.id)
            print(request.POST.get("add_film"))
            films = Film_with_user.objects.filter(user=user)
            all_durations = 0
            for film in films:
                all_durations += film.film.duration
            all_durations_h = round(all_durations / 60, 2)
            return render(request, 'main.html',
                          {"all_durations_h": all_durations_h, "films": films,
                           "all_durations": all_durations})
        if request.POST.get("del_film") is not None:
            title_id = request.POST.get("del_film")
            user = User.objects.get(id=request.user.id)
            film = Film.objects.get(id_title=title_id)
            film_user = Film_with_user.objects.get(user=user, film=film)
            film_user.delete()
        if request.POST.get("title") is not None:
            imdb_cl = imdb.IMDb()
            name = request.POST.get("title")
            search = imdb_cl.search_movie(name)
            # print(dir(search))
            for i in search:
                page = requests.get(f'https://www.imdb.com/title/tt{i.movieID}/')
                if "Runtime" in page.text:
                    small_dict_films = {}
                    small_dict_films.update({"id": i.movieID})
                    small_dict_films.update({"title": i})
                    list_find_films.append(small_dict_films)
    user = User.objects.get(id=request.user.id)
    films = Film_with_user.objects.filter(user=user)
    all_durations = 0
    for film in films:
        all_durations += film.film.duration
    all_durations_h = round(all_durations / 60, 2)
    return render(request, 'main.html', {"films": films, "all_durations": all_durations,
                                         "check_bad": check_bad, "all_durations_h": all_durations_h,
                                         "list_find_films": list_find_films,
                                         "list_id_films": list_id_films})


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
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    path_start = '{}'.format(cur_dir)
    with open(f'{path_start}\\movies.csv', "r", encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
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
