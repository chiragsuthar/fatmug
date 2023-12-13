from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Vendor, PurchaseOrder  
from .metrics import update_performance_metrics 
from .serializers import VendorSerializer, PurchaseOrderSerializer 
from django.db.models.signals import post_save
from django.dispatch import receiver
from .metrics import update_performance_metrics

# Vendor ViewSet
class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    @action(detail=True, methods=['get'])
    def performance(self, request, pk=None):
        vendor = self.get_object()
        performance_metrics = {
            'on_time_delivery_rate': vendor.on_time_delivery_rate,
            'quality_rating_avg': vendor.quality_rating_avg,
            'average_response_time': vendor.average_response_time,
            'fulfillment_rate': vendor.fulfillment_rate,
        }
        return Response(performance_metrics)

# PurchaseOrder ViewSet
class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    @action(detail=True, methods=['post'])
    def acknowledge(self, request, pk=None):
        po = self.get_object()
        po.acknowledgment_date = timezone.now()
        po.save()
        update_performance_metrics(po.vendor)
        return Response({'status': 'PO acknowledged'}, status=status.HTTP_200_OK)
    
    @receiver(post_save, sender=PurchaseOrder)
    def update_vendor_metrics(sender, instance, **kwargs):
        update_performance_metrics(instance.vendor)
