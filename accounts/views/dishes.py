from django.db.models import Count, Q
from rest_framework import status, generics
from rest_framework.response import Response

from accounts.models import Dish, Restaurant
from accounts.serializers import DishSerializer


class DishCreateView(generics.CreateAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer

    def create(self, request, *args, **kwargs):
        restaurant_id = request.data.get('restaurant_id')
        name = request.data.get('name')
        price = request.data.get('price')
        type = request.data.get('type')
        img = request.data.get('img')  # Chuỗi base64 hình ảnh từ frontend
        rate = request.data.get('rate')

        # Kiểm tra xem có đủ thông tin hay không
        if not all([name, price, type, img, rate, restaurant_id]):
            return Response({
                "status": "error",
                "message": "Not enough info"
            }, status=status.HTTP_400_BAD_REQUEST)

        # Tạo món ăn mới
        dish = Dish.objects.create(
            restaurant_id=restaurant_id,
            name=name,
            price=price,
            type=type,
            img=img,
            rate=rate,

        )

        return Response({
            "status": "success",
            "message": "Dish created successfully",
        }, status=status.HTTP_200_OK)

class DishTopView(generics.GenericAPIView):
    serializer_class = DishSerializer

    def get(self, request, *args, **kwargs):
        try:
            # Thực hiện join giữa Dishes, OrderItems, Orders và Restaurants
            top_dishes = Dish.objects.annotate(order_count=Count('orderitem')).select_related('restaurant').values('img', 'name', 'restaurant__name', 'type', 'rate', 'price', 'restaurant_id').order_by('-order_count')

            if not top_dishes:
                return Response({
                    "status": "success",
                    "message": "No data found"
                }, status=status.HTTP_200_OK)

            return Response(top_dishes, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "status": "error",
                "message": f"Error: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DishListView(generics.GenericAPIView):
    serializer_class = DishSerializer

    def get(self, request, user_id, *args, **kwargs):
        try:
            # Lấy nhà hàng theo user_id
            restaurant = Restaurant.objects.filter(user_id=user_id).first()

            if not restaurant:
                return Response({
                    "status": "error",
                    "message": "Restaurant not found"
                }, status=status.HTTP_400_BAD_REQUEST)

            # Lấy các món ăn của nhà hàng đó và sắp xếp theo rating giảm dần
            dishes = Dish.objects.filter(restaurant_id=restaurant.id).order_by('-rate')

            if not dishes:
                return Response({
                    "status": "success",
                    "message": "No data found"
                }, status=status.HTTP_200_OK)

            # Serialize danh sách món ăn
            dishes_data = DishSerializer(dishes, many=True).data

            return Response(dishes_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "status": "error",
                "message": f"Error: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DishUpdateView(generics.UpdateAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer

    def update(self, request, *args, **kwargs):
        dish = self.get_object()

      #  dish.restaurant_id = request.data.get('restaurant_id')
        dish.name = request.data.get('name', dish.name)
        dish.img = request.data.get('img', dish.img)
        dish.price = request.data.get('price', dish.price)
        dish.rate = request.data.get('rate', dish.rate)
        dish.type = request.data.get('type', dish.type)

        dish.save()

        return Response({
            "status": "success",
            "message": "Dish updated successfully",
            "data": DishSerializer(dish).data
        }, status=status.HTTP_200_OK)

class DishDeleteView(generics.DestroyAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer

    def delete(self, request, *args, **kwargs):
        dish = self.get_object()
        dish.delete()

        return Response({
            "status": "success",
            "message": "Dish deleted successfully"
        }, status=status.HTTP_200_OK)

class DishSearchView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        input = kwargs.get('input', '')  # Lấy input từ URL path
        res_id = kwargs.get('res_id')  # Lấy restaurant_id từ URL path

        if not input:
            return Response({
                "status": "error",
                "message": "Vui lòng nhập từ khoá tìm kiếm"
            }, status=status.HTTP_400_BAD_REQUEST)

        if not res_id:
            return Response({
                "status": "error",
                "message": "Vui lòng cung cấp restaurant_id"
            }, status=status.HTTP_400_BAD_REQUEST)

        # Khởi tạo điều kiện tìm kiếm
        search_conditions = Q()

        # Các trường mà bạn muốn tìm kiếm
        search_fields = ['name', 'price', 'rate', 'type']  # Thêm các trường khác nếu cần

        # Tạo các điều kiện tìm kiếm cho từng trường
        for field in search_fields:
            search_conditions |= Q(**{f'{field}__icontains': input})

        # Tìm kiếm các món ăn theo điều kiện và restaurant_id
        results = Dish.objects.filter(search_conditions, restaurant_id=res_id)

        if not results.exists():
            return Response({
                "status": "success",
                "message": "Không tìm thấy kết quả"
            }, status=status.HTTP_200_OK)

        # Nếu có kết quả, trả về danh sách các món ăn
        dishes_data = [{
            "id": dish.id,
            "name": dish.name,
            "restaurant_id": res_id,
            "price": dish.price,
            "rate": dish.rate,
            "type": dish.type,
            "img": dish.img
        } for dish in results]

        return Response(dishes_data, status=status.HTTP_200_OK)

class DishSearchDishView(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        input = request.query_params.get('input', '')  # Lấy từ khóa tìm kiếm từ query params

        if not input:
            return Response({
                "status": "error",
                "message": "Vui lòng nhập từ khoá tìm kiếm"
            }, status=status.HTTP_400_BAD_REQUEST)

        # Tìm kiếm các món ăn theo tên
        results = Dish.objects.filter(name__icontains=input)

        if not results.exists():
            return Response({
                "status": "success",
                "message": "Không tìm thấy kết quả"
            }, status=status.HTTP_200_OK)

        # Nhóm các món ăn theo restaurant_id
        grouped_results = {}
        for dish in results:
            restaurant_id = dish.restaurant.id
            if restaurant_id not in grouped_results:
                grouped_results[restaurant_id] = []
            grouped_results[restaurant_id].append(dish)

        # Tạo danh sách kết quả trả về
        list_data = []
        for restaurant_id, dishes in grouped_results.items():
            restaurant = Restaurant.objects.get(id=restaurant_id)
            dishes_data = [
                {
                    'dish_id': dish.id,
                    'img': dish.img,
                    'name': dish.name,
                    'price': dish.price
                } for dish in dishes
            ]
            list_data.append({
                'res_id': restaurant.id,
                'restaurant_name': restaurant.name,
                'dishes': dishes_data
            })

        return Response(list_data, status=status.HTTP_200_OK)

class DishDetailView(generics.RetrieveAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer

    def get(self, request, *args, **kwargs):
        dish = self.get_object()
        return Response(DishSerializer(dish).data, status=status.HTTP_200_OK)