from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(default=0)
    liked_books = models.ManyToManyField('Book', related_name='liked_by_users')
    
    def __str__(self):
        return self.name

class Book(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.name