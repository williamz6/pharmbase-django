from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import DrugSerializer, OrderItemSerializer, ProfileSerializer
from backend.models import Drug, OrderItem, Order

@api_view(['GET'])
def getRoutes(request):
    routes = [
        {'GET':'/api/drugs'},
        {'GET':'/api/drugs/id'},
        {'POST':'/api/drugs/order/id'},
        {'GET':'/api/orders'},

        {'POST':'/api/users/token'},
        {'POST':'/api/users/token/refresh'},
    ]

    return Response(routes)

@api_view(['GET'])
def getDrugs(request):
    drugs = Drug.objects.all()
    serializer = DrugSerializer(drugs, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getDrug(request, pk):
    drug = Drug.objects.get(id=pk)
    serializer = DrugSerializer(drug, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def getOrders(request):
    orders = OrderItem.objects.all()
    serializer= OrderItemSerializer(orders, many=True)
    return Response(serializer.data)