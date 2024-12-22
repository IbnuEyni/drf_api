from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from .models import User, Product
from .serializers import UserSerializer, ProductSerializer

@api_view(['GET', 'POST'])
def user_list(request):
    if request.method == 'GET':
        cached_users = cache.get('v1_users')
        if cached_users:
            response = Response(cached_users)
            response['X-Cache'] = 'HIT'
        else:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            cache.set('v1_users', serializer.data, timeout=60 * 15) 
            response = Response(serializer.data)
            response['X-Cache'] = 'MISS'
        response['X-API-Version'] = 'v1'
        return response

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete('v1_users') 
            response = Response(serializer.data, status=status.HTTP_201_CREATED)
            response['X-API-Version'] = 'v1'
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        response = Response(serializer.data)
        response['X-API-Version'] = 'v1'
        return response

    elif request.method in ['PUT', 'PATCH']:
        serializer = UserSerializer(user, data=request.data, partial=(request.method == 'PATCH'))
        if serializer.is_valid():
            serializer.save()
            cache.delete('v1_users') 
            response = Response(serializer.data)
            response['X-API-Version'] = 'v1'
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        cache.delete('v1_users') 
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response['X-API-Version'] = 'v1'
        return response


# Product Views
@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        cached_products = cache.get('products')
        if cached_products:
            response = Response(cached_products)
            response['X-Cache'] = 'HIT'
        else:
            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True)
            cache.set('products', serializer.data, timeout=60 * 15) 
            response = Response(serializer.data)
            response['X-Cache'] = 'MISS'
        response['X-API-Version'] = '1.0'
        return response

    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete('products')  
            response = Response(serializer.data, status=status.HTTP_201_CREATED)
            response['X-API-Version'] = '1.0'
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        cached_product = cache.get(f'product_{pk}')
        if cached_product:
            response = Response(cached_product)
            response['X-Cache'] = 'HIT'
        else:
            serializer = ProductSerializer(product)
            cache.set(f'product_{pk}', serializer.data, timeout=60 * 15) 
            response = Response(serializer.data)
            response['X-Cache'] = 'MISS'
        response['X-API-Version'] = '1.0'
        return response

    elif request.method in ['PUT', 'PATCH']:
        serializer = ProductSerializer(product, data=request.data, partial=(request.method == 'PATCH'))
        if serializer.is_valid():
            serializer.save()
            cache.delete('products')  
            cache.set(f'product_{pk}', serializer.data, timeout=60 * 15)  
            response = Response(serializer.data)
            response['X-API-Version'] = '1.0'
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product.delete()
        cache.delete('products')  
        cache.delete(f'product_{pk}')  
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response['X-API-Version'] = '1.0'
        return response
