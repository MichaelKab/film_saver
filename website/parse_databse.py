'''
import csv
from models import Film
import os
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
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nirla.settings") #nirla is the name of the project
print (Film.objects.all())
with open('movies.csv', "r") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    print(csv_reader)
    for index, row in enumerate(csv_reader):
        print(row)
        film = Film()
        film.id_title = row.imdb_title_id
        film.name = row.title
        film.year = row.year
        film.genre = row.genre
        film.country = row.country
        film.budget = row.budget

        if index > 3:
            break
'''
'''
from imdby.imdb import imdb
#for i in range(100):
details = imdb('tt0000000')
print(details)
#for i in range(10000000):
for i in range(len(details.genre)):
    print(details.genre[i])
#for i in range(1000):
details = imdb('tt4154796') ## tt4154796
print(details)

import imdb
from imdby.imdb import imdb as im
#from imdby.imdb import imdb
# creating instance of IMDb
ia = imdb.IMDb()
name = "Back to the Futur"
search = ia.search_movie(name)
for i in search:
    print(i.movieID)
    print(i)
    #details = im(f'tt{i.movieID}')
    #print(details, dir(details))
    #print(details.title)
'''
