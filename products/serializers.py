from django.db.models import Avg
from rest_framework import serializers

from products.models import Category, Product, Review


class CategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')
        read_only_fields = ['id']


class ProductModelSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'price', 'image', 'attributes', 'colors',
                  'description', 'expire_time', 'count', 'likes_count', 'avg_rating')
        read_only_fields = ['id']

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_avg_rating(self, obj):
        avg = obj.reviews.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 1) if avg else 0


    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['category'] = {
            'id': instance.category.id,
            'name': instance.category.name,
        }
        return res


class ReviewModelSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.fullname', read_only=True)
    like_count = serializers.SerializerMethodField()
    dislike_count = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ('id', 'product', 'user', 'user_name', 'content',
                  'like_count', 'dislike_count', 'created_at')
        read_only_fields = ['id', 'user']

    def get_like_count(self, obj):
        return obj.like_count

    def get_dislike_count(self, obj):
        return obj.dislike_count



    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class WishlistModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'price', 'image')

