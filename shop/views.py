# from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from .models import (
    # Category,
    Games,
    ActivityBox,
    SpecialBooks,
    KnowledgeCapsule,
    Standard,
    Pricing
)
from .serializers import (
    GamesSerializer,
    ActivityBoxSerializer,
    SpecialBooksSerializer,
    KnowledgeCapsuleSerializer,
    StandardSerializer
)
from rest_framework.response import Response
# Create your views here.


def google_index(request):
    return HttpResponse("google-site-verification: googleff4301433a1854f8.html")

class GamesList(ListAPIView):
    serializer_class = GamesSerializer
    queryset = Games.objects.all()

class GamesDetail(RetrieveAPIView):
    serializer_class = GamesSerializer
    queryset = Games.objects.all()


class ActivityBoxList(ListAPIView):
    serializer_class = ActivityBoxSerializer
    # queryset = ActivityBox.objects.all()

    def get_queryset(self):
        if self.request.GET.get('id', False):
            return ActivityBox.objects.filter(standard__id=int(self.request.GET['id']))
        else:
            return ActivityBox.objects.all()

class ActivityBoxDetail(RetrieveAPIView):
    serializer_class = ActivityBoxSerializer
    queryset = ActivityBox.objects.all()

class SpecialBooksList(ListAPIView):
    serializer_class = SpecialBooksSerializer
    queryset = SpecialBooks.objects.all()

class SpecialBooksDetail(RetrieveAPIView):
    serializer_class = SpecialBooksSerializer
    queryset = SpecialBooks.objects.all()

class KnowledgeCapsuleAPI(APIView):
    # serializer_class = KnowledgeCapsuleSerializer
    # queryset = KnowledgeCapsule.objects.all()
    def post(self, request):
        name = request.data["name"]
        email = request.data["email"]
        city = request.data["city"]
        school = request.data["school"]
        standard = request.data["standard"]

        KnowledgeCapsule.objects.create(
            name=name,
            email=email,
            city_name=city,
            school_name=school,
            standard=standard
        )

        return Response({
            "message":"successful!!"
        })

class StandardList(ListAPIView):
    serializer_class = StandardSerializer
    queryset = Standard.objects.all()

class PricingView(APIView):
    def get(self, request):
        name_ = request.GET['name']
        price = Pricing.objects.get(name=name_).price

        return Response({
            'price':price
        })