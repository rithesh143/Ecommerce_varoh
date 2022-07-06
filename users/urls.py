from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('user_detail', views.UserDetail.as_view()),
    path('address', views.AddressList.as_view()),
    path('create/address', views.CreateAddress.as_view()),
    path('delete/address', views.DeleteAddress.as_view()),
    path('create/user', views.CreateUser.as_view()),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('contact_us', views.CreateContactUs.as_view()),
    path('password-reset', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset/done', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
    path('csv_report', views.address_csv, name='address_csv'),
    path('is_active', views.IsActive.as_view(), name='is_active'),
]