from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, ListAPIView
from .serializers import UserSerializer, AddressSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Address, ContactUs
# from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
# Create your views here.

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from .tokens import token_generator
from django.core.mail import send_mail
from django.conf import settings

class AddressList(ListAPIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return self.request.user.address_list.all()

class CreateAddress(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        name = request.data["username"]
        phone = request.data["mobileNumber"]
        pin_code = request.data["pinCode"]
        flat = request.data["flat"]
        area = request.data["area"]
        landmark = request.data["landMark"]
        town = request.data["town"]
        state = request.data["state"]

        try:
            address = Address.objects.create(
                user=request.user,
                full_name=name,
                phone=phone,
                pin_code=pin_code,
                house=flat,
                area=area,
                landmark=landmark,
                town=town,
                state=state
            )

            return Response(AddressSerializer(address).data)
        except Exception as e:
            return Response({
                "message":str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteAddress(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def delete(self, request):
        pk = request.data["pk"]
        try:
            address = request.user.address_list.get(pk=pk)
            address.delete()
            return Response({
                "message":"delete successful"
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "message":"address not found"
            }, status=status.HTTP_404_NOT_FOUND)

class CreateUser(APIView):
    def post(self, request):
        name = request.data["name"]
        email = request.data["email"]
        password = request.data["password"]

        try:
            user = User.objects.create_user(username=email,password=password,email=email,first_name=name)
            user.is_active = False
            user.save()

            current_site = settings.DOMAIN_NAME_HOST
            mail_subject = 'Activate your account'
            message = render_to_string('email_template.html', {
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':token_generator.make_token(user)
            })

            send_mail(mail_subject, '', settings.EMAIL_HOST_USER, [user.email,], html_message=message)
            return Response({
                "message":"Email send to your mail"
            })
        except Exception as e:
            print(e)
            return Response({
                "message":str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'activation_success.html')
        # return HttpResponse("Thanks for registering")
    else:
        # return HttpResponse("Activation failed")
        return render(request, 'activation_failed.html')

class IsActive(APIView):
    def get(self, request):
        username = request.GET['username']
        user = User.objects.get(username=username)

        if not user.is_active:
            current_site = settings.DOMAIN_NAME_HOST
            mail_subject = 'Activate your account'
            message = render_to_string('email_template.html', {
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':token_generator.make_token(user)
            })

            send_mail(mail_subject, '', settings.EMAIL_HOST_USER, [user.email,], html_message=message)

        return Response({
            "is_active":user.is_active
        })

class CreateContactUs(APIView):
    def post(self, request):
        name = request.data["name"]
        email = request.data["email"]
        subject = request.data["subject"]
        message = request.data["message"]

        ContactUs.objects.create(name=name,email=email,subject=subject,message=message)
        return Response({
            "message":"feed back sent.Thank you"
        })

class UserDetail(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self):
        return self.request.user

import pandas as pd
# import csv


def address_csv(request):
	address_list = Address.objects.all()
	addresses = address_list.values('id', 'user__email', 'full_name', 'phone', 'pin_code', 'house', 'area', 'landmark', 'town', 'state')
	df = pd.DataFrame(addresses)

	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="address.csv"'

	df.to_csv(path_or_buf=response)
# 	writer = csv.writer(response)

# 	csv_text = df.to_csv()

# 	for line in csv_text.split('\n'):
# 		row = line.split(',')

# 		if row != ['']:
# 			writer.writerow(row)

	return response