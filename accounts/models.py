from django.db import models
from django.utils import timezone

class User(models.Model):
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255, default="")
    role = models.CharField(max_length=50)
    image = models.ImageField(upload_to='user_images/', null=True, blank=True, default="")
    level = models.IntegerField(default=0)
    coin = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    opening_hours = models.CharField(max_length=100)
    user = models.ForeignKey('User', on_delete=models.CASCADE,default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Dish(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    img = models.TextField(null=True, blank=True)
    price = models.IntegerField()
    rate = models.IntegerField()
    type = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE)
    price = models.IntegerField()
    ship = models.IntegerField()
    discount = models.IntegerField(default= 0)
    total_amount = models.IntegerField()
    payment = models.CharField(max_length=50, default='Tiền mặt', db_index=True)
    vnpay_payment_status = models.CharField(
        max_length=20, blank=True, null=True, db_index=True,
        choices=[
            ('pending_vnpay', 'VNPAY - Chờ thanh toán'),
            ('paid_vnpay', 'VNPAY - Đã thanh toán'),
            ('failed_vnpay', 'VNPAY - Thanh toán lỗi')
        ],
        help_text='Trạng thái thanh toán cụ thể qua VNPAY.'
    )
    vnpay_response_code = models.CharField(max_length=2, blank=True, null=True, help_text='Mã phản hồi từ VNPAY (vnp_ResponseCode).')
    vnpay_transaction_no = models.CharField(max_length=100, blank=True, null=True, help_text='Mã giao dịch do VNPAY cung cấp khi thành công (vnp_TransactionNo).')
    vnpay_txn_ref = models.CharField(max_length=100, blank=True, null=True, unique=True, db_index=True, help_text='Mã giao dịch của Merchant gửi cho VNPAY (vnp_TxnRef).')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 1. Mã tham chiếu đơn hàng gửi cho VNPAY (vnp_TxnRef)
    #    Mã này do hệ thống của bạn tạo ra, phải duy nhất trong ngày.
    #    Ví dụ: ORDER_ID_TIMESTAMP
    vnpay_txn_ref = models.CharField(
        max_length=100,
        blank=True,  # Có thể trống nếu không thanh toán qua VNPAY
        null=True,
        unique=True, # Đảm bảo duy nhất nếu được sử dụng
        db_index=True,
        help_text="Mã giao dịch của Merchant gửi cho VNPAY (vnp_TxnRef)."
    )

    # 2. Trạng thái thanh toán VNPAY
    PENDING_VNPAY = 'pending_vnpay'
    PAID_VNPAY = 'paid_vnpay'
    FAILED_VNPAY = 'failed_vnpay'
    VNPAY_STATUS_CHOICES = [
        (PENDING_VNPAY, 'VNPAY - Chờ thanh toán'),
        (PAID_VNPAY, 'VNPAY - Đã thanh toán'),
        (FAILED_VNPAY, 'VNPAY - Thanh toán lỗi'),
    ]
    vnpay_payment_status = models.CharField(
        max_length=20,
        choices=VNPAY_STATUS_CHOICES,
        blank=True, # Có thể trống nếu không thanh toán qua VNPAY
        null=True,
        db_index=True,
        help_text="Trạng thái thanh toán cụ thể qua VNPAY."
    )

    # 3. Mã giao dịch của VNPAY (vnp_TransactionNo)
    #    Mã này do VNPAY trả về khi giao dịch thành công (qua IPN).
    vnpay_transaction_no = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Mã giao dịch do VNPAY cung cấp khi thành công (vnp_TransactionNo)."
    )

    # 4. Mã phản hồi từ VNPAY (vnp_ResponseCode)
    #    Lưu mã này từ IPN (và cả Return URL nếu muốn) để debug.
    vnpay_response_code = models.CharField(
        max_length=2, # Thường là 2 chữ số, ví dụ '00'
        blank=True,
        null=True,
        help_text="Mã phản hồi từ VNPAY (vnp_ResponseCode)."
    )



    def __str__(self):
        return f"Order #{self.id} - {self.user.name} - Method {self.payment}"

    def generate_vnpay_txn_ref(self):
        """
        Hàm gợi ý để tạo mã vnpay_txn_ref duy nhất.
        Nên được gọi khi người dùng chọn thanh toán VNPAY và trước khi tạo URL.
        """
        if not self.id:
            # Điều này không nên xảy ra nếu bạn lưu đơn hàng trước khi tạo ref
            raise ValueError("Order must be saved and have an ID before generating vnpay_txn_ref.")
        # Kết hợp ID đơn hàng và timestamp để tăng tính duy nhất
        timestamp = int(timezone.now().timestamp())
        return f"ORDER_{self.id}_{timestamp}"

class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    item = models.ForeignKey('Dish', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    options = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Item {self.item.name} in Order #{self.order.id}"

class Review(models.Model):
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE,related_name='reviews',  default='')
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, default='')
    rating = models.IntegerField()
    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review for {self.item.name} by {self.user.name}"

class Cart(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    item = models.ForeignKey('Dish', on_delete=models.CASCADE, default= "")
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE, default='')
    quantity = models.PositiveIntegerField(default= 1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user.name} with {self.quantity} {self.item.name}"
