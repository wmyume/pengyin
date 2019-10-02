#-*-coding:utf-8-*-
from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns

from computerapps import views

urlpatterns = [
    path('ProductAPI/', views.ProductListView.as_view(),
         name='ProductAPI'),
    path('ProductCategAPI/', views.ProductListByCategoryView.as_view(),
         name='ProductCategAPI'),
    path('ProductCategManuAPI/', views.ProductListByCategoryManufacturerView.as_view(),
         name='ProductCategManuAPI'),
    path('UserInfoAPI/', views.UserInfoView.as_view(),
         name='UserInfoAPI'),
    path('UserProfileAPI/', views.UserProfileView.as_view(),
         name='UserProfileAPI'),
    path('UserCreateAPI/', views.UserCreateView.as_view(),
         name='UserCreateAPI'),
    path('DelivAddrAPI/', views.DeliveryAddressView.as_view(),
         name='DelivAddrAPI'),
    path('CartOrderAPI/', views.CartListView.as_view(),
         name='CartOrderAPI'),
    path('OrderAPI/', views.OrderListView.as_view(),
         name='OrderAPI'),
    path('OrderCreateAPI/', views.OrderCreateView.as_view(),
         name='OrderCreateAPI'),
    re_path(r'^OrderConfirmAPI/(?P<order_id>[1,]+)/$', views.OrderConfirmView.as_view(),
         name='OrderConfirmAPI'),
    re_path(r'^ProductModelAPI/(?P<model>)/', views.ProductListByModelView.as_view(),
         name='ProductModelAPI'),
    re_path(r'^DelivAddrCurrentAPI/(?P<addr_id>[1,]+)/$', views.DeliveryAddressCurrentView.as_view(),
         name='DelivAddrCurrentAPI'),
    re_path(r'^ProductRtrieveAPI/(?P<pk>[1,]+)/$', views.ProductRetrieveView.as_view(),
         name='ProductRtrieveAPI'),
]

urlpatterns = format_suffix_patterns(urlpatterns)