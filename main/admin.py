from django.contrib import admin
from .models import Category,Product
from review.models import Comment, Rating


class RatingInline(admin.TabularInline):
    model = Rating


class CommentInline(admin.TabularInline):
    model = Comment


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','category','status']
    list_filter = ['category','status']
    search_fields = ['title', 'description']
    inlines = [CommentInline, RatingInline]
    

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)

