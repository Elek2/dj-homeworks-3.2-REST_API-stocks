from django.urls import path
from rest_framework.routers import DefaultRouter

from logistic.views import ProductViewSet, StockViewSet, FinalChangesGitworkFlow

router = DefaultRouter()
router.register('products', ProductViewSet)
router.register('stocks', StockViewSet)

urlpatterns = [path('', FinalChangesGitworkFlow.as_view())]+router.urls

# SDF
