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
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm


@login_required(login_url='/login/')
def main(request):
    bad_title = ""
    check_bad = False
    if request.method == "POST":
        print("#################################")
        try:
            film = Film.objects.get(name=request.POST.get("title"))
            if len(Film_with_user.objects.filter(film=film)) == 0:
                film_with_user = Film_with_user()
                user = User.objects.get(id=request.user.id)
                film_with_user.user = user
                film_with_user.film = film
                film_with_user.save()
                print("TRUE", film_with_user)
        except Film.DoesNotExist:
            bad_title = request.POST.get("title")
            check_bad = True
    user = User.objects.get(id=request.user.id)
    films = Film_with_user.objects.filter(user=user)
    all_durations = 0
    for el in films:
        all_durations += el.film.duration
        print(el.film.name)
    all_durations_h = round(all_durations / 60, 2)
    return render(request, 'main.html', {"films": films, "all_durations": all_durations,
                                         "check_bad": check_bad, "bad_title": bad_title,
                                         "all_durations_h": all_durations_h})


'''
def is_not_none_warning(request, model_field, text_name_in_ht, warning):
    field = request.POST.get(text_name_in_ht)
    print(field, list(field))
    if field is not str():
        print("!!")
        model_field = field
    else:
        warning += 1
    print(warning, "###")
    return model_field, warning


@login_required(login_url='/login/')
def main(request):
        #print(request.META["HTTP_REFERER"])
    bad_ap = []
    user = CustomUser.objects.get(id=request.user.id)
    applications = Application.objects.filter(user_creator=request.user.id)
    warning = 0


    if request.method == "POST":
        print("#################################")
        film = Film.objects.get(name=request.POST.get("name_film"))
        Film_with_user = 

'''


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


def cr_db(request):
    # commands djnago
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
                # print("$$$$$$$$$$$$")
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
