from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from .models import Product
from .serializers import ProductSerializer

@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        cached_products = cache.get('v2_products')
        if cached_products:
            response = Response(cached_products)
            response['X-Cache'] = 'HIT'
        else:
            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True)
            cache.set('v2_products', serializer.data, timeout=60 * 15)  
            response = Response(serializer.data)
            response['X-Cache'] = 'MISS'
        response['X-API-Version'] = 'v2'
        return response

    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete('v2_products') 
            response = Response(serializer.data, status=status.HTTP_201_CREATED)
            response['X-API-Version'] = 'v2'
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        response = Response(serializer.data)
        response['X-API-Version'] = 'v2'
        return response

    elif request.method in ['PUT', 'PATCH']:
        serializer = ProductSerializer(product, data=request.data, partial=(request.method == 'PATCH'))
        if serializer.is_valid():
            serializer.save()
            cache.delete('v2_products') 
            response = Response(serializer.data)
            response['X-API-Version'] = 'v2'
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product.delete()
        cache.delete('v2_products') 
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response['X-API-Version'] = 'v2'
        return response
