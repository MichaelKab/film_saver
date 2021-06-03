# -*- coding: utf-8 -*
"""views"""
import os
import asyncio
from asgiref.sync import async_to_sync, sync_to_async
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
import time
from django_rq import job
#from rq import use_connection, Queue

@job("default")
def myfunc(x, y):
    return x * y


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
        if film.rating is None:
            film.rating = 11
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

            #print(string_runtime, string_duration.split("episodes"))
            #print(int(list_string_duration[0]) * int(list_string_duration[1]))
            film.duration = int(list_string_duration[0]) * int(list_string_duration[1])
        else:
            film.duration = max(list_string_duration)
        #print(list_string_duration)
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

    #use_connection()
    from .worker import conn
    """
    q = Queue(connection=conn)
    from .utils import count_words_at_url
    #result = q.enqueue(count_words_at_url, 'http://heroku.com')
    #print(result)
    r = q.enqueue(myfunc, 318, 62)
    print(r.return_value)
    time.sleep(2)
    print(r.return_value)
    """


@login_required(login_url='/login/')
def main(request):
    check_bad = False
    list_find_films = []
    list_id_films = []
    """import django_rq
    import redis
    my_connection = redis.Redis(host='127.0.0.1', port=58848)
    use_connection(my_connection)
    qe = django_rq.get_queue('default'qe)
    print(qe)
    el = qe.enqueue(myfunc, (32, 12))
    print(el)"""
    if request.method == "POST":
        print(request.POST.get("add_film"))
        if request.POST.get("add_film") is not None:
            title_id = request.POST.get("add_film")
            #loop = asyncio.get_event_loop()
            #asyncio.set_event_loop(loop)
            #args_add_film = [title_id, request]
            #loop.create_task(add_film(*args_add_film))
            #return HttpResponseRedirect("/")
            add_film(title_id, request)
            user = User.objects.get(id=request.user.id)
            print(request.POST.get("add_film"))
            """films = Film_with_user.objects.filter(user=user)
            all_durations = 0
            for film in films:
                all_durations += film.film.duration
            all_durations_h = round(all_durations / 60, 2)
            return render(request, 'main.html',
                          {"all_durations_h": all_durations_h, "films": films,
                           "all_durations": all_durations})"""

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
                from bs4 import BeautifulSoup
                page = requests.get(f'https://www.imdb.com/title/tt{i.movieID}/')
                soup = BeautifulSoup(page.text, 'lxml')
                class_name = "Media__PosterContainer-sc-1x98dcb-1 dGdktI"
                quotes = soup.find('div', class_=class_name)
                urls = []
                normal_img = ''
                if quotes is not None:
                    a = quotes.find("a")
                    href = a.get("href").split("?")
                    href = href[0]
                    img_page = requests.get(f'https://www.imdb.com{href}')
                    soup2 = BeautifulSoup(img_page.text, 'lxml')
                    url_img = soup2.find_all('img', class_="MediaViewerImagestyles__PortraitImage-sc-1qk433p-0 bnaOri")
                    for img in url_img:
                        normal_img = img.get("src")
                        #print(normal_img)

                if "Runtime" in page.text:
                    small_dict_films = {}
                    small_dict_films.update({"id": i.movieID})
                    small_dict_films.update({"title": i})
                    how_to_find_film = [normal_img, small_dict_films]
                    list_find_films.append(how_to_find_film)

    user = User.objects.get(id=request.user.id)
    films = Film_with_user.objects.filter(user=user)
    all_durations = 0
    for film in films:
        all_durations += film.film.duration
    all_durations_h = round(all_durations / 60, 2)
    return render(request, 'main.html', {"films": films, "all_durations": all_durations,
                                         "check_bad": check_bad, "all_durations_h": all_durations_h,
                                         "list_find_films": list_find_films,
                                         "list_id_films": list_id_films,})


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
