from django.urls import path

from accounts.views.OrderItems import *
from accounts.views.carts import *
from accounts.views.dishes import *
from accounts.views.orders import *
from accounts.views.restaurants import *
from accounts.views.reviews import *
from accounts.views.users import *
from accounts.views.rasa_Api import *
from .views.vnpay import vnpay_ipn, vnpay_return

urlpatterns = [
    #USER
    path('register', RegisterView.as_view(), name='user-register'),
    path('login', LoginView.as_view(), name='user-login'),
    path('user/getAll', UserListView.as_view(), name='user-list'),
    path('user/getUser/<int:pk>', UserDetailView.as_view(), name='user-detail'),
    path('user/search/<str:input>', UserSearchView.as_view(), name='user-search'),
    path('user/update/<int:pk>', UserUpdateView.as_view(), name='user-update'),
    path('user/delete/<int:pk>', UserDeleteView.as_view(), name='user-delete'),

    #RESTAURANT
    path('restaurant/create', RestaurantCreateView.as_view(), name='restaurant-create'),
    path('restaurant/getAll', RestaurantListView.as_view(), name='restaurant-getAll'),
    path('restaurant/getItem/<int:pk>', RestaurantDetailView.as_view(), name='restaurant-getItem'),
    path('restaurant/getItemOwner/<int:user_id>', RestaurantOwnerView.as_view(), name='restaurant-getItemOwner'),
    path('restaurant/update/<int:pk>', RestaurantUpdateView.as_view(), name='restaurant-update'),
    path('restaurant/delete/<int:pk>', RestaurantDeleteView.as_view(), name='restaurant-delete'),
    path('restaurant/search/<str:input>', RestaurantSearchView.as_view(), name='restaurant-search'),
    path('restaurants/order-by-rate/', RestaurantOrderByRateListView.as_view(), name='restaurants-order-by-rate'),
    path('restaurant/searchColumn/<str:label>/<str:input>', RestaurantSearchColumnView.as_view(),
         name='restaurant-searchColumn'),
    #Chua test
    path('restaurant/getAllHome', RestaurantTopListView.as_view(), name='restaurant-top-list'),


    #DISHES
    path('dish/create', DishCreateView.as_view(), name='dish-create'),
    # Chưa test
    path('dish/getAllHome', DishTopView.as_view(), name='dish-getAllHome'),
    path('dish/getAll/<int:user_id>', DishListView.as_view(), name='dish-getAll'),
   # path('dish/getRecent', DishRecentView.as_view(), name='dish-getRecent'),
    path('dish/getItem/<int:pk>', DishDetailView.as_view(), name='dish-getItem'),
    path('dish/update/<int:pk>', DishUpdateView.as_view(), name='dish-update'),
    path('dish/delete/<int:pk>', DishDeleteView.as_view(), name='dish-delete'),
    path('dish/search/<str:input>/<int:res_id>', DishSearchView.as_view(), name='dish-search'),
    path('dish/searchDish/<str:input>', DishSearchDishView.as_view(), name='dish-searchDish'),

    # ORDERS
    path('order/create', OrderCreateView.as_view(), name='order-create'),
    path('order/getAll', OrderListView.as_view(), name='order-getAll'),
    path('order/getItem/<int:pk>', OrderDetailView.as_view(), name='order-getItem'),
    # path('order/getItems/<int:user_id>', OrderUserItemsView.as_view(), name='order-getItems'),
    path('order/update/<int:pk>', OrderUpdateView.as_view(), name='order-update'),
    path('order/delete/<int:pk>', OrderDeleteView.as_view(), name='order-delete'),
    path('order/search/<str:input>', OrderSearchView.as_view(), name='order-search'),

    #ORDER ITEMS
    path('orderItems/create', OrderItemCreateView.as_view(), name='order_item-create'),
    path('orderItems/getAll/<int:order_id>', OrderItemGetAllView.as_view(), name='order_item-getAll'),
    path('orderItems/getAllByRes/<int:user_id>', OrderItemGetAllByResView.as_view(), name='order_item-getAllByRes'),
    path('orderItems/getAllAll', GetAllOrdersView.as_view(), name='orders-getAll'),
    path('orderItems/update/<int:pk>', OrderItemUpdateView.as_view(), name='order_item-update'),
    path('orderItems/getItem/<int:order_id>/<int:item_id>/', OrderItemGetView.as_view(), name='order_item-getItem'),
    path('orderItems/delete/<int:order_id>/<int:item_id>', OrderItemDeleteView.as_view(), name='order_item-delete'),
    path('orderItems/deleteAll/<int:order_id>', OrderItemDeleteAllView.as_view(), name='order_item-deleteAll'),
    path('orderItems/search/<str:input>', OrderItemSearchView.as_view(), name='order_item-search'),


    #CARTS
    path('cart/create', CartCreateView.as_view(), name='cart-create'),
    path('cart/getAll', CartListView.as_view(), name='cart-getAll'),
    path('cart/getAll/<int:user_id>/<int:restaurant_id>', CartGetAllView.as_view(), name='cart-getAll'),
    path('cart/getAllByUser/<int:user_id>/', CartGetAllByUserView.as_view(), name='cart-get-all-by-user'),
    path('cart/update', CartUpdateView.as_view(), name='cart-update'),
        path('cart/delete/<int:user_id>/<int:restaurant_id>/<int:item_id>', CartDeleteView.as_view(), name='cart-delete'),


    #REVIEWS
    path('comment/create', ReviewCreateView.as_view(), name='create_review'),
    path('comment/getItemByRate/<str:rate>', ReviewGetByRateView.as_view(), name='get_item_by_rate'),
    path('comment/getItemByDish/<str:item_id>', ReviewGetByDishView.as_view(), name='get_item_by_dish'),
    path('comment/getItemByRestaurant/<str:user_id>', ReviewGetByRestaurantView.as_view(),
         name='get_item_by_restaurant'),
    path('comment/getItemByOrder/<str:order_id>', ReviewGetByOrderView.as_view(), name='get_item_by_order'),
    path('comment/delete/<str:item_id>/<str:user_id>', ReviewDeleteView.as_view(), name='delete_review'),
    path('comment/deleteAll', ReviewDeleteAllView.as_view(), name='delete_all_reviews'),
    path('comment/search/<str:input>', ReviewSearchView.as_view(), name='search_reviews'),
    path('comment/delete/<int:pk>', CommentDeleteView.as_view(), name='comment-delete'),

    path('webhook/',RasaChatbot.as_view(), name='rasa_webhook'),

    # VNPAY
    path('vnpay/ipn/', vnpay_ipn, name='vnpay_ipn'),
    path('orders/vnpay/', OrderCreateVNPAYView.as_view(), name='order-create-vnpay'),
    path('vnpay/return/', vnpay_return, name='vnpay_return'),

]
