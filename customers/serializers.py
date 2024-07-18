from rest_framework import serializers
from .models import Customer
from django.contrib.auth.models import User

# Step 1: Create a User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class CustomerSerializer(serializers.ModelSerializer):
    # user = serializers.StringRelatedField(many=False)
    user = UserSerializer(read_only=True)
    class Meta:
        model = Customer
        fields = '__all__'

class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True, write_only=True)
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'confirm_password')
        extra_kwargs = {'password': {'write_only': True}}
    
    def save(self, **kwargs):
        # return super().save(**kwargs)
        username = self.validated_data['username']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        email = self.validated_data['email']
        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']

        # password validation checking
        if password != confirm_password:
            raise serializers.ValidationError({'error': 'both passwords must bve match'})
        
        # check if the username or email is already taken
        if User.objects.filter(email=email).exists() or User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'error': 'username or email is already exist'})

        user = User(username=username, first_name=first_name, last_name=last_name, email=email)
        user.set_password(password)
        user.is_active = False
        user.save()
        # Customer(user=user).save()
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)