# from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from .models import Order, Copun, OrderItem
from .RazorPay import client
from .serializers import OrderSerializer, CopunSerializer #, OrderItemSerializer
from shop.models import SpecialBooks, Games, ActivityBox
from django.template.loader import render_to_string
from django.core.mail import EmailMessage# send_mail
from django.conf import settings
from django.db.models import Q
from shop.models import Pricing
from django.utils.timezone import now
import requests
# expire_date

# Create your views here.

class GetCopun(RetrieveAPIView):
    serializer_class = CopunSerializer

    def get_object(self):
        if self.request.GET.get('id', False) and self.request.GET.get('category', False):
            category = self.request.GET['category']
            id = self.request.GET['id']
            if category == 'games':
                item = Games.objects.get(id=id)
            elif category == 'special_books':
                item = SpecialBooks.objects.get(id=id)
            elif category == 'activity_box':
                item = ActivityBox.objects.get(id=id)

            if item.copun.expire_date >= now().date():
                return item.copun
            else:
                return None

        if self.request.GET.get("code", False):
            code = self.request.GET.get("code")
            try:
                return Copun.objects.get(code=code)
            except:
                return None

        q1 = Q(status=True)
        q2 = Q(is_combo=True)
        q3 = Q(expire_date__gte = now().date())
        return Copun.objects.filter(q1 & q2 & q3).last()


class TestCheckout(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        print(request.data)
        return Response({
            "message":"testing"
        })

def send_order_mail(order):
    address = order.address.addr_str
    order_id = order.order_id

    order_items = order.order_items.all()

    sub_total = 0

    for i in order_items:
        sub_total += i.price

    if order.copun:
        discount = order.copun.percentage
    else:
        discount = 0

    delivery_charges = Pricing.objects.get(name='shipping').price

    grand_total = order.total

    if order.cod:
        cod_charges = Pricing.objects.get(name='cod').price
    else:
        cod_charges = 0

    context = {
        "address":address,
        "order_id":order_id,
        "order_items":order_items,
        "sub_total":sub_total,
        "discount":discount,
        "delivery_charges":delivery_charges,
        "grand_total":grand_total,
        "cod_charges":cod_charges
    }

    html = render_to_string("odrerconfirm.html", context)
    user_mail = order.user.email

    response = requests.post(
        'https://maker.ifttt.com/trigger/order_received/with/key/lUWnrStMqwljy9Wr1CknlXSUHxdpjIGjKLvg7oGw8Tw',
        data={"value1":user_mail,"value2":"contact@varohgames.com","value3":html}
    )

    print(response)
    # email = EmailMessage(
    #         'Order Received',
    #         html,
    #         settings.EMAIL_HOST_USER_EMAIL,
    #         [user_mail,'contact@varohgames.com']
    #         #,reply_to=['contact@varohgames.com']
    #     )

    # email.content_subtype = "html"
    # # email.send(fail_silently=True)
    # email.send()
    # send_mail('Order Received', '', settings.EMAIL_HOST_USER, [user_mail,], html_message=html)


class CreateOrder(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        # delete un processed orders
        q1 = Q(is_processed=False)
        q2 = Q(cod=False)
        unprocessed = request.user.orders.filter(q1 & q2)

        for order_ in unprocessed:
            order_.delete()


        address = request.user.address_list.get(id=request.data['address'])
        cod = request.data.get("cod", False)

        if cod:
            extra_charge = Pricing.objects.get(name='cod').price
        else:
            extra_charge = 0

        order = Order(
            address=address,
            user=request.user
        )

        order.save()

        if request.data["copun"] != "":
            copun = Copun.objects.get(code=request.data['copun'])
        else:
            copun = None


        total = 0

        order_items = []
        for item in request.data['items']:

            if item['category'] == 'special_books':
                Item = SpecialBooks
            elif item['category'] == 'games':
                Item = Games
            elif item['category'] == 'activity_box':
                Item = ActivityBox

            order_item = OrderItem.objects.create(
                name=item['name'],
                category=item['category'],
                quantity=int(item['quantity']),
                price=Item.objects.get(id=item['id']).price,
                image=item['image'],
                order=order
            )

            order_items.append(order_item)
            total += int(item['quantity']) * order_item.price

        order.copun = copun

        if copun:
            total -= total * (copun.percentage/100.0)

        order.total = total + Pricing.objects.get(name='shipping').price + extra_charge


        try:
            if cod:
                order.cod = cod
                order.save()
                send_order_mail(order)
                return Response({
                    "message":"Payment successful!!"
                })
        except Exception as e:
            return Response({
                "message": str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            options = {
                "amount":order.total*100,
                "currency":"INR",
                "receipt":order.order_id,
                "payment_capture":0
            }

            res = client.order.create(options)
            order.razor_pay = res["id"]

            order.save()
        except Exception as e:
            for order_item in order_items:
                order_item.delete()

            return Response({
                "message": str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            'razor_id': order.razor_pay,
            'order_id': order.order_id
        }, status=status.HTTP_200_OK)

class VerifyOrder(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        params_dict = {
            'razorpay_order_id':request.data['order_id'],
            'razorpay_payment_id':request.data['payment_id'],
            'razorpay_signature':request.data['signature']
        }

        print(params_dict)

        try:
            client.utility.verify_payment_signature(params_dict)
            order = Order.objects.get(razor_pay=request.data["order_id"])
            order.is_processed = True
            order.save()

            send_order_mail(order)

            return Response({
                "message":"Payment successful!!"
            })
        except Exception as e:
            return Response({
                "message":str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OrdersList(ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    serializer_class = OrderSerializer

    def get_queryset(self):
        return self.request.user.orders.all().order_by('-pk')

import pandas as pd
# import csv
from django.http import HttpResponse
#from orders.models import Order

def orders_csv(request):
	orders_list = Order.objects.all().order_by('-pk')
	orders = orders_list.values('timestamp', 'user__first_name', 'copun', 'order_id', 'razor_pay', 'cod', 'address__full_name', 'user__email', 'address__phone', 'address__pin_code', 'address__house', 'address__area', 'address__landmark', 'address__town', 'address__state')
	df = pd.DataFrame(orders)

	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="orders.csv"'

# 	writer = csv.writer(response)

	df.to_csv(path_or_buf=response)

# 	for line in csv_text.split('\n'):
# 		row = line.split(',')

# 		if row != ['']:
# 			writer.writerow(row)

	return response
