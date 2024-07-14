from django.shortcuts import render
from .serializers import OrderSerializer
from .models import Order
from flowers.models import Flower
from rest_framework import viewsets
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
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
    serializer_class = OrderSerializer
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