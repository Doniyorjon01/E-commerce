from django.contrib import admin

from products.models import Category, Product, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name', 'created_at')
    list_filter = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'created_at', 'updated_at',
                    'image', 'show_attributes', 'show_colors', 'price', 'description',
                    'expire_time', 'count', 'likes_count')
    search_fields = ('name', 'price', 'category', 'created_at', 'updated_at')
    filter_horizontal = ('likes',)

    def show_attributes(self, obj):
        return obj.attributes

    show_attributes.short_description = "Attributes"

    def show_colors(self, obj):
        return obj.colors

    show_colors.short_description = "Colors"
    def likes_count(self, obj):
        return obj.likes.count()



@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'content')


