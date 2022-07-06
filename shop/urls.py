from django.urls import path
from . import views

urlpatterns = [
    path('games', views.GamesList.as_view()),
    path('activity_box', views.ActivityBoxList.as_view()),
    path('special_books', views.SpecialBooksList.as_view()),
    path('games/<uuid:pk>', views.GamesDetail.as_view()),
    path('activity_box/<uuid:pk>', views.ActivityBoxDetail.as_view()),
    path('special_books/<uuid:pk>', views.SpecialBooksDetail.as_view()),
    path('standard', views.StandardList.as_view()),
    path('knowledge_capsule', views.KnowledgeCapsuleAPI.as_view()),
    path('pricing', views.PricingView.as_view()),

]