from .serializers import OrderSerializer, OrderCreateSerializer
from .models import Order
from flowers.models import Flower
from rest_framework import viewsets
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import TokenAuthentication
from django.http import HttpResponseRedirect
from sslcommerz_lib import SSLCOMMERZ
import random
import string
from customers.models import Customer
import environ
from django.urls import reverse
# for mail sending
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

env = environ.Env()
environ.Env.read_env()

# generate unique id
def unique_transaction_id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# Create your views here.
class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        customer_id = self.request.query_params.get('customer_id')
        if customer_id is not None:
            queryset = queryset.filter(customer_id=customer_id)
        return queryset
    
class OrderCreateAPIView(APIView):
    serializer_class = OrderCreateSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
    
        if serializer.is_valid():
            order = serializer.save()
            flower = get_object_or_404(Flower, pk=order.flower_id)
            full_name = f'{order.customer.user.first_name} {order.customer.user.last_name}'
            transaction_id = unique_transaction_id_generator()
            order.transaction_id = transaction_id
            order.save()
            store_id = env('STORE_ID')
            store_pass = env('STORE_PASS')
            settings = { 'store_id': store_id, 'store_pass': store_pass, 'issandbox': True }
            sslcz = SSLCOMMERZ(settings)
            post_body = {
                'total_amount': order.total_price,
                'currency': "BDT",
                'tran_id': transaction_id,
                'success_url': f"{env('BACKEND_URL')}/order/success/{order.id}",
                'fail_url': f"{env('BACKEND_URL')}/order/fail/{order.id}",
                'cancel_url': f"{env('BACKEND_URL')}/order/fail/{order.id}",
                'emi_option': 0,
                'cus_name': full_name,
                'cus_email': order.customer.user.email,
                'cus_phone': "01700000000",
                'cus_add1': "Lakshmipur",
                'cus_city': "Dhaka",
                'cus_country': "Bangladesh",
                'shipping_method': "NO",
                'multi_card_name': "",
                'num_of_item': 1,
                'product_name': flower.title,
                'product_category': "Flower",
                'product_profile': "general"
            }

            response = sslcz.createSession(post_body) # API response
            print('SSL commerce',response)
            # Need to redirect user to response['GatewayPageURL']
            return Response({'redirect_url': response['GatewayPageURL']}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderConfirmationAPIView(APIView):
    def post(self, request, order_id):
        try:
            order =  get_object_or_404(Order, pk=order_id)
            flower = get_object_or_404(Flower, pk=order.flower_id)
        except(TypeError, ValueError, OverflowError, Order.DoesNotExist or Flower.DoesNotExist):
            return Response({'error': 'Order not found or invalid order id'}, status=status.HTTP_404_NOT_FOUND)
        order.payment_status = True
        order.save(update_fields=['payment_status'])
        flower.available -= order.quantity
        flower.save(update_fields=['available'])
        full_name = f'{order.customer.user.first_name} {order.customer.user.last_name}'
        email_subject = f'Your Order Confirmation - Orchid Oasis (#[{order.id}])'
        email_body = render_to_string('orders/order_confirmation.html', {'customer_name': full_name, 'order': order})
        email = EmailMultiAlternatives(email_subject, '', to=[order.customer.user.email])
        email.attach_alternative(email_body, 'text/html')
        email.send()
        return HttpResponseRedirect(f"{env('ClIENT_URL')}/order/{order_id}")

class OrderCancelAPIView(APIView):
    def post(self, request, order_id):
        try:
            order =  get_object_or_404(Order, pk=order_id)
        except(TypeError, ValueError, OverflowError, Order.DoesNotExist):
            return Response({'error': 'Order not found or invalid order id'}, status=status.HTTP_404_NOT_FOUND)
        order.status = 'Cancelled'
        order.save()
        return HttpResponseRedirect(f"{env('ClIENT_URL')}/order/{order_id}")
    
class ChangeOrderStatusAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    def put(self, request, order_id):
        try:
            order =  get_object_or_404(Order, pk=order_id)
        except(TypeError, ValueError, OverflowError, Order.DoesNotExist):
            return Response({'error': 'Order not found or invalid order id'}, status=status.HTTP_404_NOT_FOUND)
        
        order.status = 'Completed'
        order.save()
        full_name = f'{order.customer.user.first_name} {order.customer.user.last_name}'
        email_subject = f'Your Order is Completed - Orchid Oasis (#[{order.id}])'
        email_body = render_to_string('orders/order_completed.html', {'customer_name': full_name, 'order': order})
        email = EmailMultiAlternatives(email_subject, '', to=[order.customer.user.email])
        email.attach_alternative(email_body, 'text/html')
        email.send()
        return Response({'message': 'Order status has been changed'}, status=status.HTTP_200_OK)