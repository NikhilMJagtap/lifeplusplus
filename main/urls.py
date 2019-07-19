from django.urls import path
from . import views


app_name = 'main'


urlpatterns = [
    path("", views.homepage, name="homepage"),
    path('signup',views.signup,name='signup'),
    path('login',views.login_,name='login'),
    path('logout',views.logout_,name='logout'),
    path('requests',views.requests,name='requests'),
    path('donate',views.donate,name='donate'),
]