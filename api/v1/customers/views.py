from customers.models import Customer
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.v1.customers.serializers import CustomerSerializer
from rest_framework import status


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def customers(request):
    instances = Customer.objects.filter(is_deleted = False)
    serialized = CustomerSerializer(instances,many=True, context={"request":request})
    
    response_data = {
        "statusCode" : 6000,
        'data' : serialized.data
    }

    return Response(response_data, status=status.HTTP_200_OK)
    
    
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def customer(request,pk):
    instance = None
    if Customer.objects.filter(is_deleted = False, pk=pk).exists():
        instance = Customer.objects.get(is_deleted = False, pk=pk)
    
    if instance:
        serialized = CustomerSerializer(instance,context={"request":request})
    
        response_data = {
            "statusCode" : 6000,
            'data' : serialized.data
        }
    else:
        response_data = {
            "statusCode" : 6001,
            'message' : "Customer not found"
        }
    return Response(response_data, status=status.HTTP_200_OK)