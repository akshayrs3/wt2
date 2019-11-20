from django.urls import path

from . import views
app_name = 'main_app'

urlpatterns = [
    path('', views.Index.as_view(), name = 'Index'),
    path('search', views.SearchPage.as_view(), name='SearchPage'),
    path('login', views.LoginPage.as_view(), name='LoginPage'),
    path('get_cities', views.GetCities.as_view(), name = 'GetCities'),
    path('selection', views.SelectionPage.as_view(), name = 'SelectionPage'),
    path('register', views.UserFormView.as_view(), name='RegisterPage'),
    path('payment', views.PaymentPage.as_view(), name='PaymentPage'),
    path('thankyou', views.ThankYouPage.as_view(), name='ThankYouPage'),
    path('review', views.ReviewPage.as_view(), name='ReviewPage'),

    path('review_api', views.ReviewAPI.as_view(), name='ReviewAPI'),
]