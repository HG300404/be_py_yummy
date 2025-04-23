from django.contrib.postgres.lookups import Unaccent
from rest_framework import status, generics
from rest_framework.response import Response
from django.db.models import Q, Count

from accounts.models import Restaurant, User
from accounts.serializers import RestaurantSerializer


class RestaurantCreateView(generics.CreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def create(self, request, *args, **kwargs):
        name = request.data.get('name')
        address = request.data.get('address')
        phone = request.data.get('phone')
        opening_hours = request.data.get('opening_hours')
        user_id = request.data.get('user_id')

        if not all([name, address, phone, opening_hours, user_id]):
            return Response({
                "status": "error",
                "message": "Not enough info"
            }, status=status.HTTP_400_BAD_REQUEST)

        if Restaurant.objects.filter(name=name).exists():
            return Response({
                "status": "error",
                "message": "Name exists"
            }, status=status.HTTP_400_BAD_REQUEST)

        restaurant = Restaurant.objects.create(
            name=name,
            phone=phone,
            address=address,
            opening_hours=opening_hours,
            user_id=user_id
        )

        return Response({
            "status": "success",
            "message": "Add new restaurant success"
        }, status=status.HTTP_200_OK)

class RestaurantListView(generics.ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

class RestaurantDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

class RestaurantOwnerView(generics.GenericAPIView):
    serializer_class = RestaurantSerializer

    def get(self, request, user_id, *args, **kwargs):
        restaurant = Restaurant.objects.filter(user_id=user_id).first()

        if not restaurant:
            return Response({
                "status": "error",
                "message": "ID not exist"
            }, status=status.HTTP_400_BAD_REQUEST)

        # Trả về danh sách các nhà hàng đã tìm thấy
        return Response(RestaurantSerializer(restaurant).data, status=status.HTTP_200_OK)

class RestaurantUpdateView(generics.UpdateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def update(self, request, *args, **kwargs):
        restaurant = self.get_object()
        restaurant.name = request.data.get('name', restaurant.name)
        restaurant.address = request.data.get('address', restaurant.address)
        restaurant.phone = request.data.get('phone', restaurant.phone)
        restaurant.opening_hours = request.data.get('opening_hours', restaurant.opening_hours)
        restaurant.save()

        return Response({
            "status": "success",
            "message": "Restaurant updated successfully",
            "restaurant": RestaurantSerializer(restaurant).data
        }, status=status.HTTP_200_OK)


class RestaurantDeleteView(generics.DestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def delete(self, request, *args, **kwargs):
        try:
            restaurant = self.get_object()
            restaurant.delete()
            return Response({
                "status": "success",
                "message": "Restaurant deleted successfully"
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class RestaurantSearchView(generics.GenericAPIView):
    serializer_class = RestaurantSerializer

    def get(self, request, *args, **kwargs):
        search_input = kwargs.get('input', '')  # Lấy giá trị input từ URL path
        if not search_input:
            return Response({
                "status": "error",
                "message": "No input to search"
            }, status=status.HTTP_400_BAD_REQUEST)

        # Tìm kiếm không phân biệt dấu bằng unaccent
        search_input = search_input.lower()
        results = Restaurant.objects.annotate(
            name_unaccent=Unaccent('name'),
            address_unaccent=Unaccent('address')
        ).filter(
            Q(name_unaccent__icontains=search_input) |
            Q(address_unaccent__icontains=search_input)
        )

        if not results:
            return Response({
                "status": "success",
                "message": "No information found"
            }, status=status.HTTP_200_OK)

        return Response(RestaurantSerializer(results, many=True).data, status=status.HTTP_200_OK)


class RestaurantSearchColumnView(generics.GenericAPIView):
    serializer_class = RestaurantSerializer

    def get(self, request, label, input, *args, **kwargs):
        # Kiểm tra label hợp lệ
        if label not in ['name', 'phone', 'address', 'user_id']:
            return Response({
                "status": "error",
                "message": "Invalid column"
            }, status=status.HTTP_400_BAD_REQUEST)

        search_input = input.lower()

        # Xử lý Unaccent cho từng cột cụ thể
        if label == 'name':
            results = Restaurant.objects.annotate(
                unaccented_name=Unaccent('name')  # Loại bỏ dấu trong cột name
            ).filter(
                Q(unaccented_name__icontains=search_input)  # Tìm kiếm không phân biệt dấu
            )
        elif label == 'address':
            results = Restaurant.objects.annotate(
                unaccented_address=Unaccent('address')  # Loại bỏ dấu trong cột address
            ).filter(
                Q(unaccented_address__icontains=search_input)  # Tìm kiếm không phân biệt dấu
            )
        elif label == 'user_id':
            results = Restaurant.objects.filter(
                Q(user_id=search_input)  # Tìm kiếm cho trường user_id
            )
        elif label == 'phone':
            results = Restaurant.objects.filter(
                Q(phone__icontains=search_input)  # Tìm kiếm cho trường phone
            )

        if not results:
            return Response({
                "status": "success",
                "message": "No data found"
            }, status=status.HTTP_200_OK)

        return Response(RestaurantSerializer(results, many=True).data)


class RestaurantTopListView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        # Truy vấn lấy tổng số lượng đơn hàng của mỗi nhà hàng
        top_restaurants = Restaurant.objects.annotate(
            order_count=Count('order__id')  # Đếm số lượng đơn hàng liên kết với nhà hàng
        ).order_by('-order_count')  # Sắp xếp theo số lượng đơn hàng giảm dần

        # Chọn các trường cần thiết
        top_restaurants_data = top_restaurants.values(
            'id', 'name', 'address', 'opening_hours', 'order_count'
        )

        return Response(top_restaurants_data)