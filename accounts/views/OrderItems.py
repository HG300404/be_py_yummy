from django.db.models import Q
from rest_framework import status, generics
from rest_framework.response import Response

from accounts.models import OrderItem, Cart, Dish, Restaurant, Order, User
from accounts.serializers import OrderItemSerializer


class OrderItemCreateView(generics.CreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    def create(self, request, *args, **kwargs):
        # Lấy dữ liệu từ request
        user_id = request.data.get('user_id')
        restaurant_id = request.data.get('restaurant_id')
        order_id = request.data.get('order_id')

        # Kiểm tra các trường cần thiết
        if not all([order_id, user_id, restaurant_id]):
            return Response({
                "status": "error",
                "message": "Enter full information"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Lấy đối tượng User, Restaurant và Order
            user = User.objects.get(id=user_id)
            restaurant = Restaurant.objects.get(id=restaurant_id)
            order = Order.objects.get(id=order_id)

        except User.DoesNotExist:
            return Response({
                "status": "error",
                "message": "User not found"
            }, status=status.HTTP_404_NOT_FOUND)

        except Restaurant.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Restaurant not found"
            }, status=status.HTTP_404_NOT_FOUND)

        except Order.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Order not found"
            }, status=status.HTTP_404_NOT_FOUND)

        # Lấy danh sách các món ăn trong giỏ hàng của người dùng và nhà hàng
        cart_items = Cart.objects.filter(user_id=user_id, restaurant_id=restaurant_id)

        # Kiểm tra và tạo OrderItem từ giỏ hàng
        for item in cart_items:
            try:
                # Tìm món ăn tương ứng với item_id
                dish = Dish.objects.get(id=item.item_id)  # Lấy đối tượng Dish từ item_id

            except Dish.DoesNotExist:
                return Response({
                    'status': 'error',
                    'message': f'Không tìm thấy món ăn với ID {item.item_id}'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Tạo mục đơn hàng mới từ giỏ hàng
            OrderItem.objects.create(
                order_id=order.id,  # Truyền đối tượng Order
                item_id=dish.id,  # Truyền ID của Dish (chỉ truyền `dish.id`)
                quantity=item.quantity,
                options=request.data.get('option', None)  # Nếu có tùy chọn, sử dụng giá trị này
            )

            # Xóa mục trong giỏ hàng sau khi chuyển sang đơn hàng
            item.delete()

        return Response({
            "status": "success",
            "message": "Đặt hàng thành công"
        }, status=status.HTTP_200_OK)


class OrderItemGetAllView(generics.GenericAPIView):
    def get(self, request, order_id):
        try:
            # Kiểm tra xem order_id có hợp lệ không
            order_items = OrderItem.objects.filter(order_id=order_id)

            if not order_items:
                return Response({
                    "status": "error",
                    "message": f"No items found for Order ID: {order_id}"
                }, status=status.HTTP_404_NOT_FOUND)

            response_data = []

            for item in order_items:
                try:
                    # Kiểm tra xem món ăn có tồn tại không
                    dish = Dish.objects.get(id=item.item_id)
                except Dish.DoesNotExist:
                    return Response({
                        "status": "error",
                        "message": f"Dish not found for Item ID: {item.item_id.id}"
                    }, status=status.HTTP_404_NOT_FOUND)

                response_data.append({
                    'dish_id': dish.id,
                    'dish_name': dish.name,
                    'dish_price': dish.price,
                    'dish_img': dish.img,
                    'quantity': item.quantity,
                    'options': item.options
                })

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "status": "error",
                "message": f"Error: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrderItemGetAllByResView(generics.GenericAPIView):
    def get(self, request, user_id):
        try:
            restaurant = Restaurant.objects.filter(user_id=user_id).first()
            if not restaurant:
                return Response({
                    "status": "error",
                    "message": "Restaurant not found"
                }, status=status.HTTP_404_NOT_FOUND)

            orders = Order.objects.filter(restaurant_id=restaurant.id)
            response_data = []

            for order in orders:
                user = User.objects.get(id=order.user_id)
                order_items = OrderItem.objects.filter(order_id=order.id)
                order_details = []

                for item in order_items:
                    dish = Dish.objects.get(id=item.item_id)
                    order_details.append({
                        'name': dish.name,
                        'price': dish.price,
                        'quantity': item.quantity,
                        'options': item.options
                    })

                response_data.append({
                    'name': user.name,
                    'phone': user.phone,
                    'address': user.address,
                    'dishes': order_details,
                    'total_amount': order.total_amount,
                    'created_at': order.created_at
                })

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": "error",
                "message": f"Error: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetAllOrdersView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        try:
            # Lấy tất cả đơn hàng
            orders = Order.objects.all()

            response_data = []

            for order in orders:
                # Lấy thông tin nhà hàng và người dùng
                restaurant = Restaurant.objects.get(id=order.restaurant_id)
                user = User.objects.get(id=order.user_id)

                # Lấy các món trong đơn hàng
                order_items = OrderItem.objects.filter(order_id=order.id)
                details = []
                money = []

                for order_item in order_items:
                    dish = Dish.objects.get(id=order_item.item_id)
                    details.append({
                        'name': dish.name,
                        'price': dish.price,
                        'quantity': order_item.quantity,
                    })

                # Thông tin chi phí
                money.append({
                    'price': order.price,
                    'ship': order.ship,
                    'discount': order.discount,
                    'total_amount': order.total_amount,
                })

                # Thêm tất cả thông tin vào response
                response_data.append({
                    'restaurant_name': restaurant.name,
                    'name': user.name,
                    'phone': user.phone,
                    'address': user.address,
                    'money': money,
                    'option': order_items[0].options if order_items else None,
                    'dishes': details,
                    'created_at': order.created_at,
                })

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "status": "error",
                "message": f"Error: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OrderItemUpdateView(generics.UpdateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    def update(self, request, *args, **kwargs):
        try:
            item = self.get_object()
            dish_id = request.data.get('item_id')
            dish = Dish.objects.get(id=dish_id)

            if not dish:
                return Response({
                    'status': 'error',
                    'message': 'Không tìm thấy món ăn'
                }, status=status.HTTP_400_BAD_REQUEST)

            item.item_id = dish.id
            item.quantity = request.data.get('quantity', item.quantity)
            item.options = request.data.get('options', item.options)
            item.save()

            return Response({
                'status': 'success',
                'data': OrderItemSerializer(item).data
            }, status=status.HTTP_200_OK)
        except OrderItem.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'ID không tồn tại'
            }, status=status.HTTP_400_BAD_REQUEST)


class OrderItemGetView(generics.GenericAPIView):
    serializer_class = OrderItemSerializer

    def get(self, request, order_id, item_id, *args, **kwargs):
        try:
            # Lấy mục đơn hàng theo order_id và item_id
            order_item = OrderItem.objects.get(order_id=order_id, item_id=item_id)

            # Trả về dữ liệu đã lấy
            return Response(OrderItemSerializer(order_item).data, status=status.HTTP_200_OK)
        except OrderItem.DoesNotExist:
            return Response({
                "status": "error",
                "message": "ID không tồn tại"
            }, status=status.HTTP_400_BAD_REQUEST)

class OrderItemDeleteView(generics.DestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    def delete(self, request, order_id, item_id):
        try:
            item = OrderItem.objects.get(order_id=order_id, item_id=item_id)
            item.delete()

            return Response({
                "status": "success",
                "message": "Xoá mục đơn hàng thành công"
            }, status=status.HTTP_200_OK)
        except OrderItem.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Mục không tồn tại"
            }, status=status.HTTP_400_BAD_REQUEST)

class OrderItemDeleteAllView(generics.GenericAPIView):
    def delete(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            order_items = OrderItem.objects.filter(order_id=order_id)

            if not order or not order_items:
                return Response({
                    "status": "error",
                    "message": "ID không tồn tại"
                }, status=status.HTTP_400_BAD_REQUEST)

            order_items.delete()
            order.delete()

            return Response({
                "status": "success",
                "message": "Xoá thành công"
            }, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({
                "status": "error",
                "message": "ID không tồn tại"
            }, status=status.HTTP_400_BAD_REQUEST)

class OrderItemSearchView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        input = kwargs.get('input', '')
        if not input:
            return Response({
                "status": "error",
                "message": "Vui lòng nhập từ khoá tìm kiếm"
            }, status=status.HTTP_400_BAD_REQUEST)

        order_items = OrderItem.objects.filter(
            Q(item_id__icontains=input) |
            Q(order_id__icontains=input)
        )

        if not order_items:
            return Response({
                "status": "success",
                "message": "Không tìm thấy kết quả"
            }, status=status.HTTP_200_OK)

        return Response(OrderItemSerializer(order_items, many=True).data, status=status.HTTP_200_OK)
