from django.shortcuts import render
from rest_framework import viewsets
from .serializers import CustomerSerializer, RegistrationSerializer, LoginSerializer
from .models import Customer
from django.contrib.auth.models import User
from rest_framework.views import APIView
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework.response import Response
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
# for mail sending
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# Create your views here.
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user_id')
        if user_id is not None:
            queryset = queryset.filter(user_id=user_id)
        return queryset

class UserRegistrationAPIView(APIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            print('token: ', token, 'uid :', uid)
            full_name = f'{user.first_name} {user.last_name}'
            confirm_url = f'https://orchid-oasis.onrender.com/customer/confirm/{uid}/{token}/'
            email_subject = 'Confirm Your Account'
            email_body = render_to_string('customers/confirm_account_mail.html', {'confirm_url': confirm_url, 'full_name': full_name})
            email = EmailMultiAlternatives(email_subject, '', to=[user.email])
            email.attach_alternative(email_body, 'text/html')
            email.send()
            return Response({'success': 'We have sent you a link to confirm your account. Please check your email'}, status=200)

def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
        print("🐍 File: customers/views.py | Line: 48 | activate ~ user",user)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        Customer(user=user).save()
        return redirect('http://localhost:3000/login')
    else:
        return Response('register')

class UserLoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            # authenticated user
            user = authenticate(username=username, password=password)
            if user is not None:
                token, _ = Token.objects.get_or_create(user=user)
                login(request, user)
                return Response({'token': token.key, 'user_id': user.pk}, status=200)

        return Response({'error': 'Invalid credentials'}, status=400)

class UserLogoutAPIView(APIView):
    def get(self, request):
        request.user.auth_token.delete()
        logout(request)
        return Response({'message': 'Successfully logged out'}, status=200)