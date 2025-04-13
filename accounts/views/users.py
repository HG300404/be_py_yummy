from django.contrib.auth.hashers import make_password, check_password
from rest_framework import status, generics
from rest_framework.response import Response
from django.db.models import Q

from accounts.models import User
from accounts.serializers import UserSerializer


# Đăng ký người dùng
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        if User.objects.filter(email=email).exists():
            return Response({"status": "error", "message": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        password = request.data.get('password')
        if password:
            request.data['password'] = make_password(password)  # Mã hóa mật khẩu

        # Tạo người dùng mới
        try:
            response = super().create(request, *args, **kwargs)
            return Response({
                "status": "success",
                "message": "Đăng ký thành công",
                "user": response.data
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


# Đăng nhập người dùng
class LoginView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({
                "status": "error",
                "message": "Please enter both email and password."
            }, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()

        if not user:
            return Response({
                "status": "error",
                "message": "Email does not exist"
            }, status=status.HTTP_400_BAD_REQUEST)

        if not check_password(password, user.password):
            return Response({
                "status": "error",
                "message": "Wrong password"
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "status": "success",
            "user": UserSerializer(user).data
        }, status=status.HTTP_200_OK)


# Lấy danh sách tất cả người dùng
class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Lấy thông tin chi tiết người dùng
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Tìm kiếm người dùng
class UserSearchView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        search_input = kwargs.get('input', '')  # Lấy giá trị input từ URL path
        if not search_input:
            return Response({
                "status": "error",
                "message": "No input to search"
            }, status=status.HTTP_400_BAD_REQUEST)

        # Tìm kiếm người dùng theo tên, email, phone hoặc address
        users = User.objects.filter(
            Q(name__icontains=search_input) |
            Q(email__icontains=search_input) |
            Q(phone__icontains=search_input) |
            Q(address__icontains=search_input)
        )

        if not users:
            return Response({
                "status": "success",
                "message": "No information found"
            }, status=status.HTTP_200_OK)

        return Response(UserSerializer(users, many=True).data, status=status.HTTP_200_OK)


# Cập nhật thông tin người dùng
class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        password = request.data.get('password')
        if password:
            user.password = make_password(password)  # Mã hóa mật khẩu
        return super().update(request, *args, **kwargs)


# Xóa người dùng
class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def delete(self, request, *args, **kwargs):
        try:
            user = self.get_object()
            user.delete()
            return Response({
                "status": "success",
                "message": "User deleted successfully"
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)