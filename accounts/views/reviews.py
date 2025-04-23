from django.db.models import Q
from rest_framework import status, generics
from rest_framework.response import Response

from accounts.models import Review, OrderItem, Dish, Restaurant
from accounts.serializers import ReviewSerializer

class ReviewCreateView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def create(self, request, *args, **kwargs):
        try:
            # Lấy dữ liệu từ request
            restaurant_id = request.data.get('restaurant_id')
            user_id = request.data.get('user_id')
            comment = request.data.get('comment')
            rating = request.data.get('rating')
            order_id = request.data.get('order_id')

            # Kiểm tra các trường cần thiết
            if not all([restaurant_id, user_id, comment, rating, order_id]):
                return Response({"status": "error", "message": "Enter full info"}, status=status.HTTP_400_BAD_REQUEST)

            # Lấy các mục đơn hàng của order_id
            order_items = OrderItem.objects.filter(order_id=order_id)

            # Cập nhật rating cho từng món ăn trong đơn hàng
            for item in order_items:
                try:
                    dish = Dish.objects.get(id=item.item_id)
                    dish.rate += int(rating)  # Cộng rating vào món ăn
                    dish.save()
                except Dish.DoesNotExist:
                    return Response({"status": "error", "message": f"Dish with id {item.item_id} not found"},
                                    status=status.HTTP_400_BAD_REQUEST)

            # Tạo đánh giá mới
            Review.objects.create(
                restaurant_id=restaurant_id,
                user_id=user_id,
                rating=rating,
                comment=comment,
                order_id=order_id
            )

            return Response({"status": "success", "message": "Save success"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReviewGetByRateView(generics.GenericAPIView):
    def get(self, request, rate, *args, **kwargs):
        reviews = Review.objects.filter(rating=rate)
        if reviews.exists():
            review_list = [
                {
                    'dish_name': item.dish.name,
                    'restaurant': item.restaurant.name,
                    'user_name': item.user.name,
                    'comment': item.comment
                } for item in reviews
            ]
            return Response(review_list)
        return Response({"status": "success", "message": "No data found"}, status=status.HTTP_200_OK)


class ReviewGetByDishView(generics.GenericAPIView):
    def get(self, request, item_id, *args, **kwargs):
        reviews = Review.objects.filter(item_id=item_id)
        if reviews.exists():
            review_list = [
                {
                    'rating': item.rating,
                    'user_name': item.user.name,
                    'comment': item.comment
                } for item in reviews
            ]
            return Response(review_list)
        return Response({"status": "success", "message": "No data found"}, status=status.HTTP_200_OK)


class ReviewGetByRestaurantView(generics.GenericAPIView):
    def get(self, request, user_id, *args, **kwargs):
        restaurant = Restaurant.objects.filter(user_id=user_id).first()
        if restaurant:
            reviews = Review.objects.filter(restaurant_id=restaurant.id)
            review_list = [
                {
                    'rating': item.rating,
                    'user_name': item.user.name,
                    'comment': item.comment,
                    'created_at': item.created_at
                } for item in reviews
            ]
            return Response(review_list)
        return Response({"status": "error", "message": "Restaurant not found"}, status=status.HTTP_400_BAD_REQUEST)


class ReviewGetByOrderView(generics.GenericAPIView):
    def get(self, request, order_id, *args, **kwargs):
        review = Review.objects.filter(order_id=order_id).first()
        if review:
            return Response({"rating": review.rating, "comment": review.comment})
        return Response({"status": "success", "message": "No data found"}, status=status.HTTP_200_OK)


class ReviewDeleteView(generics.DestroyAPIView):
    queryset = Review.objects.all()

    def delete(self, request, item_id, user_id, *args, **kwargs):
        try:
            review = Review.objects.get(user_id=user_id, item_id=item_id)
            review.delete()
            return Response({"status": "success", "message": "Deleted successfully"})
        except Review.DoesNotExist:
            return Response({"status": "error", "message": "Review not found"}, status=status.HTTP_400_BAD_REQUEST)


class ReviewDeleteAllView(generics.GenericAPIView):
    def delete(self, request, *args, **kwargs):
        try:
            Review.objects.all().delete()
            return Response({"status": "success", "message": "All reviews deleted"})
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReviewSearchView(generics.GenericAPIView):
    def get(self, request, input, *args, **kwargs):
        if not input:
            return Response({"status": "error", "message": "Please provide a search term"},
                            status=status.HTTP_400_BAD_REQUEST)

        reviews = Review.objects.filter(
            Q(comment__icontains=input) | Q(rating__icontains=input)
        )

        if reviews.exists():
            return Response(ReviewSerializer(reviews, many=True).data)
        return Response({"status": "success", "message": "No results found"}, status=status.HTTP_200_OK)
