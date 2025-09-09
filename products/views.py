from pickle import FALSE

from django.db.models import Avg, Count
from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from products.models import Category, Product, Review
from products.serializers import CategoryModelSerializer, ProductModelSerializer, ReviewModelSerializer, \
    WishlistModelSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class IsAdminUserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    parser_classes = (FormParser, MultiPartParser)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # Agar likes_count DB ustuni yo'q bo'lsa, uni ordering_fields ga qo'ymang
    ordering_fields = ["created_at", "updated_at"]

    def get_queryset(self):
        qs = super().get_queryset()

        # simple filters
        category = self.request.query_params.get('category')
        search = self.request.query_params.get('search')
        if category:
            qs = qs.filter(category__name__icontains=category)
        if search:
            qs = qs.filter(name__icontains=search)

        # custom ordering keywords
        ordering = self.request.query_params.get('ordering')
        if ordering == "newest":
            qs = qs.order_by("-created_at")
        elif ordering == "most_recent":
            qs = qs.order_by("-updated_at")
        elif ordering == "popular":
            # count likes dynamically then order
            qs = qs.annotate(likes_count=Count("likes")).order_by("-likes_count")
        # "all" or None => default ordering

        return qs

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="category",
                in_=openapi.IN_QUERY,
                description="Filter by category name",
                required=False,
                schema=openapi.Schema(type=openapi.TYPE_STRING),
            ),
            openapi.Parameter(
                name="search",
                in_=openapi.IN_QUERY,
                description="Search by product name",
                required=False,
                schema=openapi.Schema(type=openapi.TYPE_STRING),
            ),
            openapi.Parameter(
                name="ordering",
                in_=openapi.IN_QUERY,
                description="Choose ordering: all | newest | popular | most_recent",
                required=False,
                schema=openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=["all", "newest", "popular", "most_recent"]
                ),
            ),
        ],
        responses={200: ProductModelSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        # Add rating information
        reviews = Review.objects.filter(product=instance)
        avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        total_reviews = reviews.count()

        # Rating distribution
        rating_dist = []
        for i in range(1, 6):
            count = reviews.filter(rating=i).count()
            percentage = (count / total_reviews * 100) if total_reviews > 0 else 0
            rating_dist.append({
                'stars': i,
                'count': count,
                'percentage': percentage
            })

        data.update({
            'avg_rating': round(avg_rating, 1),
            'total_reviews': total_reviews,
            'rating_distribution': rating_dist
        })

        return Response(data)


class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewModelSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        product_id = self.request.query_params.get('product_id')
        if product_id:
            return Review.objects.filter(product_id=product_id).order_by('-created_at')
        return Review.objects.none()


# @api_view(['POST'])
# @permission_classes(IsAuthenticated)
# def toggle_like_product(request, product_id):
#     try:
#         product = Product.objects.get(id=product_id)
#         user = request.user
#
#         if user in product.likes.all():
#             product.likes.remove(user)
#             liked = False
#         else:
#             product.likes.add(user)
#             liked = True
#
#         return Response({
#             'liked': liked,
#             'likes_count': product.likes.count()
#         })
#     except Product.DoesNotExist:
#         return Response({'error': 'Product not found'}, status=404)



class ToggleLikeProductView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductModelSerializer
    def post(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            user = request.user

            if user in product.likes.all():
                product.likes.remove(user)
                liked = False
            else:
                product.likes.add(user)
                liked = True

            return Response({
                "liked": liked,
                "likes_count": product.likes.count()
            })
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)

@api_view(['POST'])
def toggle_like_review(request, review_id):
    try:
        review = Review.objects.get(id=review_id)
        user = request.user

        if user in review.likes.all():
            review.likes.remove(user)
            liked = False
        else:
            review.likes.add(user)
            # Remove from dislikes if previously disliked
            if user in review.dislikes.all():
                review.dislikes.remove(user)
            liked = True

        return Response({
            'liked': liked,
            'likes_count': review.like_count,
            'dislikes_count': review.dislike_count
        })
    except Review.DoesNotExist:
        return Response({'error': 'Review not found'}, status=404)


class WishlistListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        products = Product.objects.filter(likes=user)
        serializer = WishlistModelSerializer(products, many=True)
        return Response(serializer.data)


