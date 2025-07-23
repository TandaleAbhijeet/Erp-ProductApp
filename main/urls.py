from django.urls import path,include
from main.views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'product_list', ProductViewSet, basename='product-list-retrieve')


urlpatterns = [
    path('',include(router.urls)),
    path('create_update_delete_product/',CreateUpdateDeleteProduct.as_view()),
    path('product_bulk_delete/',DeleteBulkProduct.as_view()),
    path('import_product/',ProductImportView.as_view()),
    
]
