# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http.response import HttpResponseRedirect, HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from customers.models import Customer
from api.v1.customers.serializers import CustomerSerializer
from django.db.models import Q
from main.functions import get_auto_id
from api.v1.general.functions import generate_serializer_errors

#create customer
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def create_customer(request):
    serialized = CustomerSerializer(data=request.data)
    if serialized.is_valid():
        auto_id = get_auto_id(Customer)
        serialized.save(auto_id=auto_id,creator=request.user,updater=request.user)

        response_data = {
        "StatusCodes" : 6000,
        "data" : serialized.data
        }
        return Response(response_data, status=status.HTTP_200_OK)
    else:
        response_data = {
        "StatusCodes" : 6001,
        "message" : generate_serializer_errors(serialized._errors)
        }
        return Response(response_data, status=status.HTTP_200_OK)

#edit customer
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def edit_customer(request,pk):
    serialized = CustomerSerializer(data=request.data)
    instance = None
    if Customer.objects.filter(is_deleted=False,pk=pk).exists():
        instance = Customer.objects.get(is_deleted=False,pk=pk)
    if instance:
        if serialized.is_valid():
            serialized.update(instance,serialized.data)

            response_data = {
            "StatusCodes" : 6000,
            "data" : serialized.data
            }
        else:
            response_data = {
            "StatusCodes" : 6001,
            "message" : generate_serializer_errors(serialized._errors)
            }

        return Response(response_data, status=status.HTTP_200_OK)

    else:
        response_data = {
        "StatusCodes" : 6001,
        "messege" : "Not found"
        }

    return Response(response_data, status=status.HTTP_200_OK)

#views all customers
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def customers(request):
    instances = Customer.objects.filter(is_deleted=False)

    query = request.GET.get('q')
    if query:
        instances = instances.filter(Q(name__icontains=query))

    serialized = CustomerSerializer(instances,many=True,context={"request":request})

    response_data = {
    "StatusCodes" : 6000,
    "data" : serialized.data
    }
    return Response(response_data, status=status.HTTP_200_OK)


#single view by pk
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def customer(request,pk):
    instance = None
    if Customer.objects.filter(is_deleted=False,pk=pk).exists():
        instance = Customer.objects.get(is_deleted=False,pk=pk)

    if instance:
        serialized = CustomerSerializer(instance,context={"request":request})

        response_data = {
        "StatusCodes" : 6000,
        "data" : serialized.data
        }
    else:
        response_data = {
        "StatusCodes" : 6001,
        "messege" : "Not found"
        }

    return Response(response_data, status=status.HTTP_200_OK)
