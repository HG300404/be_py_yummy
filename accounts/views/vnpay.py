import hashlib
import hmac
import urllib.parse
import time
import requests  # Thêm dòng này
from datetime import datetime, timedelta  # <-- Thêm dòng này
from django.conf import settings
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render
from accounts.models import Order

def generate_vnpay_payment_url(order, amount, client_ip):
    vnp_TmnCode = settings.VNPAY_TMN_CODE
    vnp_HashSecret = settings.VNPAY_HASH_SECRET_KEY
    vnp_Url = settings.VNPAY_PAYMENT_URL
    vnp_ReturnUrl = settings.VNPAY_RETURN_URL

    vnp_TxnRef = order.generate_vnpay_txn_ref()
    order.vnpay_txn_ref = vnp_TxnRef
    order.save()

    vnp_Params = {
        'vnp_Version': '2.1.0',
        'vnp_Command': 'pay',
        'vnp_TmnCode': vnp_TmnCode,
        'vnp_Amount': str(amount * 100),
        'vnp_CurrCode': 'VND',
        'vnp_TxnRef': vnp_TxnRef,
        'vnp_OrderInfo': f"Thanh toan don hang {order.id}",
        'vnp_OrderType': 'food',  # Đổi thành 'food'
        'vnp_Locale': 'vn',
        'vnp_ReturnUrl': vnp_ReturnUrl,
        'vnp_IpAddr': client_ip,
        'vnp_CreateDate': timezone.now().strftime('%Y%m%d%H%M%S'),
    }

    sorted_params = sorted(vnp_Params.items())
    query_string = '&'.join([f"{k}={urllib.parse.quote_plus(str(v))}" for k, v in sorted_params])
    secure_hash = hmac.new(
        bytes(vnp_HashSecret, 'utf-8'),
        query_string.encode('utf-8'),  # Sử dụng query_string đã encode
        hashlib.sha512
    ).hexdigest()

    payment_url = f"{vnp_Url}?{query_string}&vnp_SecureHash={secure_hash}"
    print(f"Generated VNPay payment URL: {payment_url}")  # In ra URL thanh toán để kiểm tra
    return payment_url

@csrf_exempt
def vnpay_return(request):
    params = request.GET.dict()
    vnp_SecureHash = params.pop('vnp_SecureHash', None)
    vnp_HashSecret = settings.VNPAY_HASH_SECRET_KEY

    sorted_params = sorted(params.items())
    hash_data = '&'.join([f"{k}={urllib.parse.quote_plus(str(v))}" for k, v in sorted_params])
    secure_hash = hmac.new(
        bytes(vnp_HashSecret, 'utf-8'),
        hash_data.encode('utf-8'),
        hashlib.sha512
    ).hexdigest()

    if secure_hash != vnp_SecureHash:
        return JsonResponse({'status': 'error', 'message': 'Invalid signature'}, status=400)

    vnp_TxnRef = params.get('vnp_TxnRef')
    vnp_ResponseCode = params.get('vnp_ResponseCode')
    vnp_TransactionNo = params.get('vnp_TransactionNo')

    try:
        order = Order.objects.get(vnpay_txn_ref=vnp_TxnRef)
        if vnp_ResponseCode == '00':
            order.vnpay_payment_status = Order.PAID_VNPAY
            # Gửi webhook đến n8n khi thanh toán thành công
            webhook_url = 'http://localhost:5678/webhook-test/vnpay-success'  # Thay bằng URL webhook thực tế nếu cần
            if hasattr(order, 'created_at'):
                estimated_delivery = order.created_at + timedelta(hours=1)
            else:
                estimated_delivery = timezone.now() + timedelta(hours=1)
            payload = {
                'order_id': order.id,
                'user_id': order.user_id,
                'restaurant_id': order.restaurant_id,
                'total_amount': float(order.total_amount) / 100,
                'status': 'PAID_VNPAY',
                'vnpay_transaction_no': vnp_TransactionNo,
                'estimated_delivery': estimated_delivery.isoformat()
            }
            try:
                requests.post(webhook_url, json=payload, timeout=5)
            except Exception as e:
                print(f"Webhook error: {e}")
        else:
            order.vnpay_payment_status = Order.FAILED_VNPAY
        order.vnpay_transaction_no = vnp_TransactionNo
        order.vnpay_response_code = vnp_ResponseCode
        order.save()
        return JsonResponse({'status': 'success', 'message': 'Payment processed', 'order_id': order.id})
    except Order.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Order not found'}, status=404)

@csrf_exempt
def vnpay_ipn(request):
    params = request.GET.dict()
    vnp_SecureHash = params.pop('vnp_SecureHash', None)
    vnp_HashSecret = settings.VNPAY_HASH_SECRET_KEY

    if not all(key in params for key in ['vnp_TxnRef', 'vnp_Amount', 'vnp_ResponseCode', 'vnp_TmnCode']):
        return JsonResponse({'RspCode': '99', 'Message': 'Missing required parameters'}, status=400)

    sorted_params = sorted(params.items())
    query_string = '&'.join([f"{k}={urllib.parse.quote_plus(str(v))}" for k, v in sorted_params])
    secure_hash = hmac.new(
        bytes(vnp_HashSecret, 'utf-8'),
        query_string.encode('utf-8'),
        hashlib.sha512
    ).hexdigest()

    if secure_hash != vnp_SecureHash:
        return JsonResponse({'RspCode': '97', 'Message': 'Invalid signature'}, status=400)

    vnp_TxnRef = params.get('vnp_TxnRef')
    vnp_ResponseCode = params.get('vnp_ResponseCode')
    vnp_TransactionNo = params.get('vnp_TransactionNo')

    try:
        order = Order.objects.get(vnpay_txn_ref=vnp_TxnRef)
        if vnp_ResponseCode == '00':
            order.vnpay_payment_status = Order.PAID_VNPAY
            # Gửi webhook đến n8n khi thanh toán thành công
            webhook_url = 'http://localhost:5678/webhook-test/vnpay-success'
            if hasattr(order, 'created_at'):
                estimated_delivery = order.created_at + timedelta(hours=1)
            else:
                estimated_delivery = timezone.now() + timedelta(hours=1)
            payload = {
                'order_id': order.id,
                'user_id': order.user_id,  # Thêm user_id
                'restaurant_id': order.restaurant_id,  # Thêm restaurant_id
                'total_amount': float(order.total_amount) / 100,  # Thêm total_amount, chia 100 để hiển thị đúng
                'status': 'PAID_VNPAY',
                'vnpay_transaction_no': vnp_TransactionNo,
                'created_at': order.created_at.isoformat(),
                'estimated_delivery': estimated_delivery.isoformat()
            }
            try:
                response = requests.post(webhook_url, json=payload, timeout=5)
                print(f"Webhook sent to n8n: {payload}, Response: {response.status_code}, Content: {response.text}")
            except Exception as e:
                print(f"Webhook error: {e}")
        else:
            order.vnpay_payment_status = Order.FAILED_VNPAY
        order.vnpay_transaction_no = vnp_TransactionNo
        order.vnpay_response_code = vnp_ResponseCode
        order.vnpay_pay_date = timezone.now()
        order.save()
        return JsonResponse({'RspCode': '00', 'Message': 'Confirm Success'})
    except Order.DoesNotExist:
        return JsonResponse({'RspCode': '01', 'Message': 'Order not found'}, status=404)