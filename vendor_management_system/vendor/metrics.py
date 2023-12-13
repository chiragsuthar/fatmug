from django.db.models import Avg, Count, F, Q
from django.utils import timezone
from .models import Vendor, PurchaseOrder

# On-Time Delivery Rate
def calculate_on_time_delivery_rate(vendor):
    completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
    on_time_pos = completed_pos.filter(delivery_date__lte=F('completion_date'))
    on_time_delivery_rate = on_time_pos.count() / completed_pos.count() if completed_pos.count() > 0 else 0
    return on_time_delivery_rate

# Quality Rating Average
def calculate_quality_rating_avg(vendor):
    quality_rating_avg = PurchaseOrder.objects.filter(vendor=vendor, status='completed').aggregate(quality_rating_avg=Avg('quality_rating'))['quality_rating_avg']
    return quality_rating_avg

# Average Response Time
def calculate_average_response_time(vendor):
    acknowledged_pos = PurchaseOrder.objects.filter(vendor=vendor).exclude(acknowledgment_date=None)
    if acknowledged_pos.count() > 0:
        response_times = acknowledged_pos.annotate(response_time=F('acknowledgment_date') - F('issue_date'))
        average_response_time = response_times.aggregate(average_response_time=Avg('response_time'))['average_response_time']
        return average_response_time
    else:
        return None  # or some other default value


# Fulfilment Rate
def calculate_fulfilment_rate(vendor):
    total_pos = PurchaseOrder.objects.filter(vendor=vendor)
    fulfilled_pos = total_pos.exclude(status='completed', issue__isnull=False)
    fulfilment_rate = fulfilled_pos.count() / total_pos.count() if total_pos.count() > 0 else 0
    return fulfilment_rate

# Update Performance Metrics
def update_performance_metrics(vendor):
    vendor.on_time_delivery_rate = calculate_on_time_delivery_rate(vendor)
    vendor.quality_rating_avg = calculate_quality_rating_avg(vendor)
    vendor.average_response_time = calculate_average_response_time(vendor)
    vendor.fulfillment_rate = calculate_fulfilment_rate(vendor)
    vendor.save()
