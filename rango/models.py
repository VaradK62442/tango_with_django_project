from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Page(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE) 
    # CASCADE - delete associated pages
    
    title = models.CharField(max_length=128)
    url = models.URLField() 
    # URLField stores resource URLs
    
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title
