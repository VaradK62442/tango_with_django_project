from django.contrib import admin

from rango.models import Category, Page

class PageAdmin(admin.ModelAdmin):
    # what to display in what order on admin page
    list_display = ('title', 'category', 'url')

admin.site.register(Category)
admin.site.register(Page, PageAdmin)
