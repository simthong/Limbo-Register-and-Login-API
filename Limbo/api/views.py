from django.shortcuts import render

from rest_framework.decorators import api_view

from rest_framework.response import Response
from . models import Product 
from . serializers import ProductSerializer, RegistrationSerializer

from rest_framework import status

from rest_framework.authtoken.models import Token




@api_view(['GET', 'POST'])
def product_list(request, format=None):


    if request.method == 'GET':


        products = Product.objects.all()


        serializer = ProductSerializer(products, many=True)


        return Response(serializer.data)


    if request.method == 'POST':

        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data)
              

@api_view(['GET', 'PUT', 'DELETE'])
def product(request, pk, format=None):
    
    try:
        
        product = Product.objects.get(id=pk)

    except Product.DoesNotExist():

        return Response(status=status.HTTP_404_NOT_FOUND)   


    if request.method == 'GET':

        serializer = ProductSerializer(product)

        return Response(serializer.data, status=status.HTTP_200_OK)

        
    elif request.method == 'PUT':

        serializer = ProductSerializer(product,  data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        



    elif request.method == 'DELETE':

        product.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)        





@api_view(['POST'])
def register(request):

    if request.method == 'POST':

        serializer = RegistrationSerializer(data=request.data)

        data = {}

        if serializer.is_valid():

            user = serializer.save()

            data['response'] = 'Successfully registered a new user!'

            ######## the login of our user

            auth_token = Token.objects.get(user=user).key

            data['token'] = auth_token

        else:

            data = serializer.errors

        return Response(data)         









