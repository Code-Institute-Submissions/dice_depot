from decimal import Decimal
from django.conf import settings

def bag_contents(request):

    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
    }

    return context