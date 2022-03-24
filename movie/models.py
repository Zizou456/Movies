from django.db import models

# Create your models here.
class Genre(models.Model):
    tag         = models.CharField(max_length=30)

    def __str__(self):
        return self.tag


def get_default_movie_image():
    return "posters/default.png"

def get_movie_image_filepath(self):
    return 'posters/' + str(self.id) + '.png'

class Movie(models.Model):
    id                  = models.IntegerField(primary_key=True)
    title               = models.CharField(max_length=200)
    overview            = models.TextField(null=True, blank=True)
    trailer             = models.TextField(null=True, blank=True)
    geners              = models.ManyToManyField(Genre, blank=True)
    duration            = models.FloatField(null=True, blank=True)
    release_date        = models.CharField(max_length=10, blank=True)
    rating              = models.FloatField(null=True, blank=True)
    votes               = models.FloatField(null=True, blank=True)
    poster              = models.ImageField(null=True, upload_to=get_movie_image_filepath, blank=True,default=get_default_movie_image)


    def __str__(self):
        return self.title