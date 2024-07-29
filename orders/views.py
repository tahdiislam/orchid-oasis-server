from django.shortcuts import render, redirect
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
# for mail sending
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# Create your views here.
class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Order.objects.all()
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
            flower.available -= order.quantity
            flower.save(update_fields=['available'])
            full_name = f'{order.customer.user.first_name} {order.customer.user.last_name}'
            email_subject = f'Your Order Confirmation - Orchid Oasis (#[{order.id}])'
            email_body = render_to_string('orders/order_confirmation.html', {'customer_name': full_name, 'order': order})
            email = EmailMultiAlternatives(email_subject, '', to=[order.customer.user.email])
            email.attach_alternative(email_body, 'text/html')
            email.send()
            return Response({'success': 'Order confirmed'}, status=200)
        return redirect(f'http://localhost:3000/admin')
    
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