from django.db import models

# Create your models here.

class Genere(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(null=True, blank=True)


    def __str__(self):
        return self.title
    



class Author(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    email = models.EmailField(null=True, blank=True)
    contact = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.name
    


class Book(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    price = models.FloatField()
    discount_price = models.FloatField(null=True, blank=True)
    description = models.TextField()
    nu_of_pages = models.IntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='authors')
    genere = models.ForeignKey(Genere, on_delete=models.CASCADE, related_name='category')
    cover_image = models.ImageField(upload_to='books/cover')
    edition = models.CharField(default='latest edition')
    isbn = models.CharField(max_length=200)

    def __str__(self):
        return self.title + " : " + self.author.name