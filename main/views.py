from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
import requests
from main.serializers import *
from main.models import *
from rest_framework import status,generics
from main.pagination import CustomPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.filters import SearchFilter
from django.shortcuts import get_object_or_404

class ProductViewSet(ReadOnlyModelViewSet):
    '''
    ProductViewSet
    -----------------------
    ViewSet for retrieving a list of products or a single product instance.

    List Endpoint:
    --------------
    - Method: GET
    - URL: /products/
    - Description: Returns a paginated list of products ordered by highest rating.
    - Query Params:
        - page (optional): Page number
        - page_size (optional): Items per page
        - search (optional): Filter products by title (case-insensitive)

    Retrieve Endpoint:
    ------------------
    - Method: GET
    - URL: /products/{pk}/
    - Description: Retrieve a single product by its ID.
    '''

    serializer_class = ViewProductSerializer
    pagination_class =CustomPagination
    filter_backends = [SearchFilter]  
    search_fields = ['title']
    
    def get_queryset(self):
        # Return all products ordered by rating_rate descending
        return Product.objects.all().order_by('-rating_rate')

    @swagger_auto_schema(
        operation_summary="List products with pagination and search by title",
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description="Page number"),
            openapi.Parameter('page_size', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description="Items per page"),
            openapi.Parameter('search', openapi.IN_QUERY, type=openapi.TYPE_STRING, description="Search by title"),
        ],
        tags=['Product List API`s']
    )
    def list(self,request,*args,**kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Retrieve a single product by ID.",
        tags=['Product List API`s']
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
        

class CreateUpdateDeleteProduct(APIView):

    '''
    CreateUpdateDeleteProduct
    -------------------------
    - POST: Create a product (validates duplicate title case-insensitively)
    - PUT: Update an existing product by product_id
    - DELETE: Delete a product by product_id
    '''

    @swagger_auto_schema(operation_summary="Create a new Product",
        request_body=ProductSerializer,
        tags=['Product API`s']
    )
    def post(self,request):
        '''
        POST /create_update_delete_product/
        ----------------
        - Create a new product.
        - Rejects if title already exists (case-insensitive).
        '''

        data = request.data

        # Check for title uniqueness (case-insensitive)
        if Product.objects.filter(title__iexact = data.get('title')).exists():
            return Response({'responseMessage':'Product with this title already exists'},status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'responseMessage':'Product created successfully'},status=status.HTTP_201_CREATED)
        return Response({'error':serializer.errors,'responseMessage':'Someting is wrong! Please check your input'},status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary="Update the existing Product data",
        manual_parameters=[
        openapi.Parameter('product_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Enter the Unique id of product'),

        ],
        request_body=ProductSerializer,
        tags=['Product API`s']
    )
    def put(self,request):
        '''
        PUT /create_update_delete_product/?product_id={id}
        ------------------------------
        - Updates an existing product.
        - Validates product_id and duplicate title.
        '''

        product_id = request.query_params.get('product_id')
        if not product_id:
            return Response({'responseMessage':'Product id is required'},status=status.HTTP_400_BAD_REQUEST)
        data = request.data
        title = data.get('title')

        # Check for duplicate title excluding updating product
        if Product.objects.filter(title__iexact = title).exclude(product_id= product_id).exists():
            return Response({'responseMessage':'Product with this title already exists'},status=status.HTTP_400_BAD_REQUEST)
        
        product = get_object_or_404(Product,product_id=product_id)
        serializer = ProductSerializer(product,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'responseMessage':'Product data updated successfully'},status=status.HTTP_200_OK)
        return Response({'data':serializer.errors,'responseMessage':'Someting is wrong! Please check your input'},status=status.HTTP_400_BAD_REQUEST)


    @swagger_auto_schema(operation_summary="Delete single product by using product id",
        manual_parameters=[
        openapi.Parameter('product_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Enter the Unique id of product'),

        ],
        tags=['Product API`s']
    )
    def delete(self,request):
        '''
        DELETE /create_update_delete_product/?product_id={id}
        -----------------------------
        - Deletes a single product by ID.
        '''
        product_id = request.query_params.get('product_id')
        if not product_id:
            return Response({'responseMessage':'Product id required'},status=status.HTTP_400_BAD_REQUEST)
        product = get_object_or_404(Product,product_id=product_id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DeleteBulkProduct(APIView):
    '''
    DeleteBulkProduct
    -----------------
    - DELETE: Delete multiple products by product IDs.
    '''
    @swagger_auto_schema(operation_summary="Delete multiple product by using product id",
            type=openapi.TYPE_OBJECT,
        properties={
            'product_ids': openapi.Schema(type=openapi.TYPE_ARRAY,items=openapi.Items(type=openapi.TYPE_INTEGER),description="List of product IDs to delete")
        },
        tags=['Product API`s']
    )
    def delete(self,request):
        product_ids = request.data.get('product_ids',[])

        if not isinstance(product_ids,list) or not product_ids:
            return Response({'responseMessage':'Please provide valid list of product ids'},status=status.HTTP_400_BAD_REQUEST)
        
        Product.objects.filter(product_id__in=product_ids).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    




class ProductImportView(APIView):
    '''
    ProductImportView
    -------------
    - POST: Imports products from https://fakestoreapi.com/products.
    - Adds only non-duplicate products based on case-insensitive title check.
    '''
    @swagger_auto_schema(
        operation_summary="Import third party Prodcut details",
        tags=['Product Import API`s']
    )
    def post(self,request):
        url = "https://fakestoreapi.com/products"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            instances = []

            for item in data:

                # Check for duplicates using case-insensitive title
                if not Product.objects.filter(title__iexact=item['title']).exists():
                    instances.append(
                        Product(
                            title=item['title'],
                            price=item['price'],
                            description=item['description'],
                            category=item['category'],
                            image=item['image'],
                            rating_rate=item['rating']['rate'],
                            rating_count=item['rating']['count']
                            ) 
                        )
            if instances:
                Product.objects.bulk_create(instances)
                return Response({'responseMessage':f'{len(instances)} product has been imported successfully'},status=status.HTTP_200_OK)
            return Response({'responseMessage':'All products already exist. No new products were imported.'},status=status.HTTP_200_OK)
        return Response({'responseMessage': 'Failed to fetch data from external API'}, status=status.HTTP_400_BAD_REQUEST)
    

