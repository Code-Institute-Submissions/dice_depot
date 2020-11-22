from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from .models import Order, OrderLineItem
from products.models import Product
from profiles.models import UserProfile

import json
import time


class StripeWebhook:

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        cust_email = order.email
        subject = render_to_string(
            'checkout/emails/checkout_email_subject.txt',
            {'order': order})
        body = render_to_string(
            'checkout/emails/checkout_email_body.txt',
            {'order': order})

    def confirm_order(self, order):
        """
        Sends out confirmation email on completion of order
        """
        confirm_email = order.email
        subject = render_to_string(
            'checkout/checkout_emails/subject.txt',
            {'order': order})
        body = render_to_string(
            'checkout/checkout_emails/body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})
        
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL
            [cust_email]
        )

    
    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def event_error(self, event):

        return HttpResponse(
            content=f'Unhandled Webhook received: {event["type"]}',
            status=200)

    def event_payment_success(self, event):
        intent = event.data.object
        pid = intent.id
        bag = intent.metadata.bag
        save_info = intent.metadata.save_info

        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping_details
        grand_total = round(intent.charges.data[0].amount / 100, 2)

        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        profile = None
        username = intent.metadata.username
        if username is != 'AnonymousUser':
            profile = UserProfile.objects.get(user__username=username)
            if save_info:
                profile.phone_number = shipping_details.phone
                profile.country = shipping_details.address.country
                profile.postcode = shipping_details.address.postal_code
                profile.town_or_city = shipping_details.address.city
                profile.street_address1 = shipping_details.address.street_address1
                profile.street_address2 = shipping_details.address.street_address2
                profile.county = shipping_details.address.state
                profile.save()

        order_exists = False
        attempt = 1
        while attempt <= 5 : 
            try:
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone_number,
                    country__iexact=shipping_details.address.country,
                    postcode__iexact=shipping_details.address.postal_code,
                    town_or_city__iexact=shipping_details.address.city,
                    street_address1__iexact=shipping_details.address.street_address1,
                    street_address2__iexact=shipping_details.address.street_address2,
                    county__iexact=shipping_details.address.state,
                    grand_total=grand_total,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
            if order_exists:
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | Order verified in database',
                    status=200)
            else:
                order = None
                try:
                    order = Order.objects.create(
                        full_name=shipping_details.name,
                        user_profile=profile,
                        email=billing_details.email,
                        phone_number=shipping_details.phone_number,
                        country=shipping_details.address.country,
                        postcode=shipping_details.address.postal_code,
                        town_or_city=shipping_details.address.city,
                        street_address1=shipping_details.address.street_address1,
                        street_address2=shipping_details.address.street_address2,
                        county=shipping_details.address.state,
                        original_bag=bag,
                        stripe_pid=pid,
                    )
                    for product_id, item_data in json.loads(bag).items():
                        product = Product.objects.get(id=product_id)
                        if isinstance(item_data, int):
                            order_line_item = OrderLineItem(
                                    order=order,
                                    product=product,
                                    quantity=item_data,
                            )
                            order_line_item.save()
                except Exception as e: 
                    if order:
                        order.delete()
                    return HttpResponse(content=f'Webhook received: {event["type"]} | Error: {e}', status = 500)
            return HttpResponse( 
                content=f'Webhook received: {event["type"]} | Order created succesfully',
                status=200)

    def event_payment_failure(self, event):

        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)