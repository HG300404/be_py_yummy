from django.db.models import Sum
from rest_framework import status, generics
from rest_framework.response import Response

from accounts.models import Cart, Dish, Restaurant, User, Order
from accounts.serializers import CartSerializer


class CartCreateView(generics.CreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def create(self, request, *args, **kwargs):
        try:
            # Kiểm tra các trường cần thiết
            required_fields = ['user_id', 'item_id', 'restaurant_id', 'quantity']
            if not all(field in request.data for field in required_fields):
                return Response({
                    "status": "error",
                    "message": "Enter full infor"
                }, status=status.HTTP_400_BAD_REQUEST)

            # Tạo một mục giỏ hàng mới
            cart_item = Cart.objects.create(
                user_id=request.data.get('user_id'),
                item_id=request.data.get('item_id'),
                restaurant_id=request.data.get('restaurant_id'),
                quantity=request.data.get('quantity')
            )

            return Response({
                "status": "success",
                "message": "Add new item in cart success"
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": "error",
                "message": f"Error: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CartGetAllView(generics.GenericAPIView):
    def get(self, request, user_id, restaurant_id):
        try:
            cart_items = Cart.objects.filter(user_id=user_id, restaurant_id=restaurant_id).order_by('-created_at')
            response_data = []

            for item in cart_items:
                dish = Dish.objects.get(id=item.item_id)
                response_data.append({
                    'dish_id': dish.id,
                    'dish_name': dish.name,
                    'dish_price': dish.price,
                    'dish_img': dish.img,
                    'quantity': item.quantity,
                })

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": "error",
                "message": f"Error: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CartGetAllByUserView(generics.GenericAPIView):
    def get(self, request, user_id):
        try:
            cart_items = Cart.objects.filter(user_id=user_id) \
                .values('restaurant_id') \
                .annotate(total=Sum('quantity')) \
                .order_by('restaurant_id')

            response_data = []

            for item in cart_items:
                restaurant = Restaurant.objects.get(id=item['restaurant_id'])
                dishes = Dish.objects.filter(restaurant_id=item['restaurant_id'])

                response_data.append({
                    'img': dishes[0].img if dishes else '',
                    'id': restaurant.id,
                    'restaurant_name': restaurant.name,
                    'address': restaurant.address,
                    'count': item['total'],
                })

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "status": "error",
                "message": f"Error: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CartUpdateView(generics.UpdateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def update(self, request, *args, **kwargs):
        try:
            # Lấy đối tượng cart_item dựa trên user_id, restaurant_id, item_id
            cart_item = Cart.objects.get(
                user_id=request.data.get('user_id'),
                restaurant_id=request.data.get('restaurant_id'),
                item_id=request.data.get('item_id')
            )

            # Kiểm tra nếu có quantity trong request, thì cập nhật quantity
            quantity = request.data.get('quantity')
            if quantity:
                cart_item.quantity = quantity

            # Lưu lại sự thay đổi
            cart_item.save()

            # Trả về dữ liệu đã cập nhật
            return Response({
                'status': 'success',
                'data': CartSerializer(cart_item).data
            }, status=status.HTTP_200_OK)

        except Cart.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Cart item not found'
            }, status=status.HTTP_404_NOT_FOUND)

class CartDeleteView(generics.DestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def delete(self, request, user_id, restaurant_id, item_id):
        try:
            cart_item = Cart.objects.get(user_id=user_id, restaurant_id=restaurant_id, item_id=item_id)
            cart_item.delete()

            return Response({
                "status": "success",
                "message": "Delete success"
            }, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({
                "status": "error",
                "message": "ID not exist"
            }, status=status.HTTP_400_BAD_REQUEST)
