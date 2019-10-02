from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from computerapps.models import Product, UserProfile, DeliveryAddress, Order
from computerapps.serializers import ProductListSerializer, ProductRetrieveSerializer, UserInfoSerializer, \
    UserProfileSerializer, UserSerializer, DeliveryAddressSerializer, OrderListSerializer, \
    OrderCreateSerializer, OrderConfirmSerializer



class ProductRetrieveView(generics.RetrieveAPIView):
    """
    product detail information
    """
    ordering_fields = ('model', 'description', 'category', 'manufacturer', 'created',
                       'sold')
    ordering = ('-id',)
    pagination_class = LimitOffsetPagination
    queryset = Product.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = ProductRetrieveSerializer


class ProductListView(generics.ListAPIView):
    """
    product list
    """
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (OrderingFilter, SearchFilter)
    search_fields = ('model',)
    ordering_fields = ('model', 'description', 'category', 'manufacturer', 'created',
                       'sold')
    ordering = ('id',)
    pagination_class = LimitOffsetPagination


class ProductListByCategoryView(generics.ListAPIView):
    """
    product category list
    """
    serializer_class = ProductListSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (OrderingFilter, SearchFilter)
    search_fields = ('model',)
    ordering_fields = ('category', 'manufacturer', 'created',
                       'price', 'sold')
    ordering = ('id',)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = Product.objects.filter(category=category)
        else:
            queryset = Product.objects.all()

        return queryset


class ProductListByCategoryManufacturerView(generics.ListAPIView):
    """
    product category manufacturer list
    """
    serializer_class = ProductListSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (OrderingFilter, SearchFilter)
    search_fields = ('model',)
    ordering_fields = ('category', 'manufacturer', 'created',
                       'price', 'sold')
    ordering = ('id',)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        category = self.request.query_params.get('category', None)
        manufacturer = self.request.query_params.get('manufacturer', None)
        if category and manufacturer is not None:
            queryset = Product.objects.filter(category=category, manufacturer=manufacturer)
        else:
            queryset = Product.objects.all()

        return queryset


class ProductListByModelView(generics.RetrieveAPIView):
    """
    Get product Model list
    根据电脑型号获取信息
    """
    serializer_class = ProductListSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (OrderingFilter, SearchFilter)
    search_fields = ('model',)
    ordering_fields = ('model', 'price', 'category',  'created')
    ordering = ('id',)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        model = self.kwargs['model']
        try:
            queryset = Product.objects.filter(model=model)
        except Exception as e:
            raise NotFound('not found this model.')
        return queryset


class UserInfoView(APIView):
    """
    Get User information
    用户名，密码等基本信息
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        user = self.request.user
        serializer = UserInfoSerializer(user)
        return Response(serializer.data)


class UserProfileView(APIView):
    """
    Create User Profile
    用户手机，地址等其他信息
    """
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        user = self.request.user
        obj = UserProfile.objects.get(user=user)
        return obj


class UserCreateView(generics.CreateAPIView):
    """
    Create User
    创建更改用户
    """
    serializer_class = UserSerializer


class DeliveryAddressView(generics.ListCreateAPIView):
    """
    Create Delivery Address information
    该用户所拥有的所有地址
    """
    serializer_class = DeliveryAddressSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        queryset = DeliveryAddress.objects.filter(user=user)
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        s = serializer.save(user=user)
        profile = user.profile_of
        profile.delivery_address = s
        profile.save()


class DeliveryAddressCurrentView(generics.RetrieveUpdateDestroyAPIView):
    """
    Modify Current Users Delivery Address information
    更改当前交易用户的实际收货地址
    """
    serializer_class = DeliveryAddressSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        user = self.request.user
        try:
            obj = DeliveryAddress.objects.get(id=self.kwargs['addr_id'], user=user)
        except Exception as e:
            raise NotFound('not found anything.')
        return obj


class CartListView(generics.ListAPIView):
    """
    Cart list
    购物车清单
    """
    serializer_class = OrderListSerializer
    permission_classes = (permissions.AllowAny,)

    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        user = self.request.user
        queryset = Order.objects.filter(user=user, status='0')

        return queryset


class OrderListView(generics.ListAPIView):
    """
    Order list
    订单
    """
    serializer_class = OrderListSerializer
    permission_classes = (permissions.AllowAny,)

    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        user = self.request.user
        queryset = Order.objects.filter(user=user, status__in=['1','2','3','4'])

        return queryset


class OrderCreateView(generics.CreateAPIView):
    """
    Create Order
    创建订单
    """
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        user = self.request.user
        product = serializer.validated_data.get('product')

        serializer.save(user=user, price=product.price, status='0',
                        address=user.profile_of.delivery_address)

        # logging.info('user %d cart changed, product %s related.')related


class OrderConfirmView(generics.CreateAPIView):
    """
    Confirm Order
    提交订单
    """
    serializer_class = OrderConfirmSerializer
    permission_classes = (permissions.IsAuthenticated,)

    pagination_class = LimitOffsetPagination

    def get_object(self):
        user = self.request.user
        obj = Order.objects.get(user=user, id=self.kwargs['order_id'])
        return obj

    def perform_update(self, serializer):
        user = self.request.user
        serializer.save(user=user, status='1')
