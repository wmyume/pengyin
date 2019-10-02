#-*-coding:utf-8-*-
from django.contrib.auth.models import User
from rest_framework import serializers

from computerapps.models import Product, Manufacturer, Category, UserProfile, DeliveryAddress, Order


class UserProfileSerializer(serializers.ModelSerializer):
    """
    User Profiles Serializer
    用户其他信息
    """
    class Meta:
        model = UserProfile
        fields = ('id', 'user', 'mobile_phone',
                  'nickname', 'description', 'icon',
                  'created', 'updated', )
        read_only_fields = ('user',)


class UserSerializer(serializers.ModelSerializer):
    """
    User Serializer
    用户基本信息
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email',
                  'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only':True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        user_profile = UserProfile(user=user)
        user_profile.save()
        return user


class UserInfoSerializer(serializers.ModelSerializer):
    """
    User Information Serializer
    用户基本信息和用户其他信息
    """
    profile_of = UserProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'email',
                  'first_name', 'last_name',
                  'date_joined', 'profile_of')


class CategorySerializer(serializers.ModelSerializer):
    """
    Category Serializer
    """
    class Meta:
        model = Category
        fields = ('id', 'name')


class ManufacturerSerializer(serializers.ModelSerializer):
    """
    Mnaufacturer Serializer
    """
    class Meta:
        model = Manufacturer
        fields = ('id', 'name')


class ProductListSerializer(serializers.ModelSerializer):
    """
    product Serializer
    """
    class Meta:
        model = Product
        fields = ('id', 'model', 'image', 'price',
                  'sold', 'category', 'manufacturer', 'description')


class ProductRetrieveSerializer(serializers.ModelSerializer):
    """
    product Retrieve detail information
    """
    manufacturer = ManufacturerSerializer()
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = ('id', 'model', 'image', 'price',
                  'sold', 'category', 'manufacturer', 'description',
                  'created', 'updated',)


class DeliveryAddressSerializer(serializers.ModelSerializer):
    """
    Delivery Address Serializer
    """
    class Meta:
        model = DeliveryAddress
        fields = ('id', 'user', 'contact_person',
                  'contact_mobile_phone','delivery_address', 'created','updated',)
        read_only_fields = ('user',)


class OrderListSerializer(serializers.ModelSerializer):
    """
    OrderList Information
    """
    product = ProductListSerializer()
    address = DeliveryAddressSerializer()

    class Meta:
        model = Order
        fields = ('id',  'status', 'user', 'product',
                  'price', 'quantity', 'address', 'remark',
                  'created', 'updated')
        read_only_fields = ('user', )


class OrderCreateSerializer(serializers.ModelSerializer):
    """
    Create Order Serializer
    """

    class Meta:
        model = Order
        fields = ('id',  'status', 'user', 'product',
                  'price', 'quantity', 'address', 'remark',
                  'created', 'updated')
        read_only_fields = ('user', 'price', 'address')


class OrderConfirmSerializer(serializers.ModelSerializer):
    """
    Create Order Serializer
    """

    class Meta:
        model = Order
        fields = ('id', 'status')