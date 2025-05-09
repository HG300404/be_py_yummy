from datetime import datetime

from django.db.models import Q, Sum
from rest_framework import status, generics
from rest_framework.response import Response

from accounts.models import Order, Restaurant, User
from accounts.serializers import OrderSerializer


class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        try:
            # Kiểm tra các trường cần thiết
            required_fields = ['user_id', 'restaurant_id', 'price', 'ship', 'discount', 'total_amount', 'payment']
            if not all(field in request.data for field in required_fields):
                return Response({
                    "status": "error",
                    "message": "Not enough info"
                }, status=status.HTTP_400_BAD_REQUEST)


            # Tạo đơn hàng mới
            order = Order.objects.create(
                user_id=request.data.get('user_id'),
                restaurant_id=request.data.get('restaurant_id'),
                price=request.data.get('price'),
                ship=request.data.get('ship'),
                discount=request.data.get('discount'),
                total_amount=request.data.get('total_amount'),
                payment="Tiền mặt" if request.data.get('payment') == 0 else "Trực tuyến"
            )

            return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": "error",
                "message": f"Error: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get(self, request, *args, **kwargs):
        orders = Order.objects.all()
        return Response(OrderSerializer(orders, many=True).data, status=status.HTTP_200_OK)

class OrderDetailView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get(self, request, *args, **kwargs):
        try:
            order = self.get_object()
            return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({
                "status": "error",
                "message": "ID không tồn tại"
            }, status=status.HTTP_400_BAD_REQUEST)


# class OrderUserItemsView(generics.GenericAPIView):
#     def get(self, request, user_id, *args, **kwargs):
#         try:
#             # Lấy tất cả đơn hàng của người dùng
#             orders = Order.objects.filter(user_id=user_id)
#             response_data = []
#
#             for order in orders:
#                 restaurant = Restaurant.objects.get(id=order.restaurant_id)
#                 order_items = OrdersItems.objects.filter(order_id=order.id)
#                 count = sum(item.quantity for item in order_items)
#
#                 dish = Dishes.objects.get(id=order_items.first().item_id)
#                 response_data.append({
#                     'img': dish.img,
#                     'id': restaurant.id,
#                     'restaurant_name': restaurant.name,
#                     'address': restaurant.address,
#                     'count': count,
#                 })
#
#             return Response(response_data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({
#                 "status": "error",
#                 "message": f"Error: {str(e)}"
#             }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OrderUpdateView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def update(self, request, *args, **kwargs):
        try:
            order = self.get_object()
            for field, value in request.data.items():
                setattr(order, field, value)
            order.save()

            return Response({
                'status': 'success',
                'data': OrderSerializer(order).data
            }, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'ID không tồn tại'
            }, status=status.HTTP_400_BAD_REQUEST)


class OrderDeleteView(generics.DestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def delete(self, request, *args, **kwargs):
        try:
            order = self.get_object()
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


class OrderSearchView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        input = kwargs.get('input', '')
        if not input:
            return Response({
                "status": "error",
                "message": "Vui lòng nhập từ khoá tìm kiếm"
            }, status=status.HTTP_400_BAD_REQUEST)

        orders = Order.objects.filter(
            Q(id__icontains=input) |
            Q(user_id__icontains=input) |
            Q(restaurant_id__icontains=input)
        )

        if not orders:
            return Response({
                "status": "success",
                "message": "Không tìm thấy kết quả"
            }, status=status.HTTP_200_OK)

        return Response(OrderSerializer(orders, many=True).data, status=status.HTTP_200_OK)

class TotalRevenueByMonthView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        current_year = datetime.datetime.now().year
        revenue = Order.objects.filter(created_at__year=current_year) \
            .values('created_at__month') \
            .annotate(total=Sum('total_amount')) \
            .order_by('created_at__month')

        return Response(revenue, status=status.HTTP_200_OK)


class TotalOrderByWeekdayView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        current_week_start = datetime.datetime.now().date() - datetime.timedelta(days=datetime.datetime.now().weekday())
        current_week_end = current_week_start + datetime.timedelta(days=6)

        total_orders = Order.objects.filter(
            created_at__range=[current_week_start, current_week_end]
        ).values('created_at__weekday') \
         .annotate(total=Sum('total_amount')) \
         .order_by('created_at__weekday')

        return Response(total_orders, status=status.HTTP_200_OK)
