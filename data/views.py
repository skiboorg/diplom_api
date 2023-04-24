import json
from rest_framework.response import Response
from .serializers import *
from .models import *
from rest_framework import generics, viewsets, parsers


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


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


class ManagerOrder(generics.ListAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    lookup_field = 'created_by__uuid'

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



