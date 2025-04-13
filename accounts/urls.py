from django.urls import path

from accounts.views.users import *

urlpatterns = [
    #USER
    path('register', RegisterView.as_view(), name='user-register'),
    path('login', LoginView.as_view(), name='user-login'),
    path('user/getAll', UserListView.as_view(), name='user-list'),
    path('user/getUser/<int:pk>', UserDetailView.as_view(), name='user-detail'),
    path('user/search/<str:input>', UserSearchView.as_view(), name='user-search'),
    path('user/update/<int:pk>', UserUpdateView.as_view(), name='user-update'),
    path('user/delete/<int:pk>', UserDeleteView.as_view(), name='user-delete'),

    #DISH
]
