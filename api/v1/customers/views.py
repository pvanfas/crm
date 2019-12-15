from rest_framework.permissions import AllowAny, IsAuthenticated
from api.v1.customers.serializers import CustomerSerializer
from customers.models import Customer
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.response import Response
from rest_framework import status
from api.v1.general.functions import generate_serializer_errors
from main.functions import get_auto_id


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def customers(request):
    instances = Customer.objects.filter(is_deleted = False)
    query = Customer.objects.filter(is_deleted=False)
    if query:
        instances = instances.filter(name__icontains=query)
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
    
    
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def create_customer(request):
    serialized = CustomerSerializer(data=request.data)
    if serialized.is_valid():
        auto_id = get_auto_id(Customer)
        serialized.save(auto_id=auto_id,creator=request.user,updater=request.user)
        
        response_data = {
            "StatusCode" : 6000,
            'data' : serialized.data
        }
        
        return Response(response_data,status=status.HTTP_200_OK)
    else:
        response_data = {
            "StatusCode" : 6000,
            "message" : generate_serializer_errors(serialized._errors)
        }
        return Response(response_data,status=status.HTTP_200_OK)
    
    
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def edit_customer(request):
    serialized = CustomerSerializer(data=request.data)
    instance = None
    if Customer.objects.filter(is_deleted=False,pk=pk).exists():
        instance = Customer.objects.get(is_deleted=False,pk=pk)
    if instance:
        if serialized.is_valid():
            serialized.update(instance,serialized.data)
            response_data = {
                "StatusCode" : 6000,
                'data' : serialized.data
            }
            return Response(response_data,status=status.HTTP_200_OK)
        else:
            response_data = {
                "StatusCode" : 6000,
                "message" : generate_serializer_errors(serialized._errors)
            }
            return Response(response_data,status=status.HTTP_200_OK)
    else:
        response_data = {
            "StatusCode" : 6000,
            "message" : "Customer not found"
        }
        return Response(response_data,status=status.HTTP_200_OK)
    
            