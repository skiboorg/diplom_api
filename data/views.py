import json

import django_filters
from django_filters import IsoDateTimeFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from .models import *
from rest_framework import generics, viewsets, parsers


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'name_slug'

class DirectionViewSet(viewsets.ModelViewSet):
    queryset = Direction.objects.all()
    serializer_class = DirectionSerializer
    lookup_field = 'name_slug'
class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    lookup_field = 'name_slug'

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    lookup_field = 'name_slug'

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    parser_classes = [parsers.MultiPartParser, parsers.JSONParser]
    lookup_field = 'uuid'

    def create(self, request, *args, **kwargs):
        setattr(request.data, '_mutable', True)
        try:
            request.data.pop('files')
            files_descriptions = request.data.pop('descriptions')
        except:
            files_descriptions = []
        data = json.loads(json.dumps(request.data))
        json_data = {}
        for dat in data:
            json_data[dat] = json.loads(data[dat])
        serializer = self.get_serializer(data=json_data)
        if serializer.is_valid():
            order = serializer.save()
            order.created_by = request.user
            order.save()
            for index,file in enumerate(request.FILES.getlist('files')):
                OrderFile.objects.create(file=file,order=order,description=files_descriptions[index])
        else:
            print(serializer.errors)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        setattr(request.data, '_mutable', True)
        try:
            request.data.pop('files')
            files_descriptions = request.data.pop('descriptions')
        except:
            files_descriptions = []
        data = json.loads(json.dumps(request.data))
        json_data = {}
        for dat in data:
            json_data[dat] = json.loads(data[dat])
        print(json_data)
        serializer = self.get_serializer(instance, data=json_data)
        if serializer.is_valid():
            order = serializer.save()
            for index, file in enumerate(request.FILES.getlist('files')):
                OrderFile.objects.create(file=file, order=order, description=files_descriptions[index])
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

class ManagerOrderFilter(django_filters.FilterSet):
    start_date_gte = IsoDateTimeFilter(field_name="start_date", lookup_expr='gte')
    class Meta:
        model = Order
        fields = {
            'start_date': ('lte', 'gte'),
            'is_dead_line_soon': ('exact',),
            'is_done': ('exact',),
            'user__is_vip': ('exact',),
            'service__id': ('exact',),
            'pay_status__id': ('exact',),
            'order_status__id': ('exact',),
        }

class ManagerOrder(generics.ListAPIView):
    serializer_class = OrderSerializer
    # queryset = Order.objects.all()
    # lookup_field = 'id'
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ManagerOrderFilter
    filterset_fields = ['is_dead_line_soon',
                        'is_done',
                        'user__is_vip',
                        'service__id',
                        'start_date__gte',
                        'status__id',
                        'pay_status__id',
                        'order_status__id',
                        ]
    ordering_fields = ['start_date', 'end_date']

    def get_queryset(self):
        return Order.objects.filter(created_by__uuid=self.kwargs['created_by__uuid'])

class UserOrder(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user__uuid=self.kwargs['user__uuid'])


class FileOrder(generics.DestroyAPIView):
    serializer_class = OrderFileSerializer
    queryset = OrderFile.objects.all()


class OrderStatus(generics.ListAPIView):
    serializer_class = OrderStatusSerializer
    queryset = OrderStatus.objects.all()


class PayStatus(generics.ListAPIView):
    serializer_class = PayStatusSerializer
    queryset = PayStatus.objects.all()

class OrderComments(APIView):
    def post(self,request,comment_id=None,*args,**kwargs):
        order = Order.objects.get(uuid=self.kwargs['uuid'])
        OrderComment.objects.create(order=order,text=request.data['text'])
        return Response(status=status.HTTP_201_CREATED)
    def delete(self,request,comment_id,*args,**kwargs):
        OrderComment.objects.get(id=comment_id).delete()
        return Response(status=status.HTTP_200_OK)

class OrderFiles(APIView):
    def post(self,request,file_id=None,*args,**kwargs):
        order = Order.objects.get(uuid=self.kwargs['uuid'])
        OrderFile.objects.create(order=order,file=request.FILES.get('file'),description=request.data.get('description'))
        return Response(status=status.HTTP_201_CREATED)

    def delete(self,request,file_id,*args,**kwargs):
        OrderFile.objects.get(id=file_id).delete()
        return Response(status=status.HTTP_200_OK)



