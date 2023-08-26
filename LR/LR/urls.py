from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView
from test.views import home, signup, login, index  # Remove duplicated imports
from test.views import signup, verify_email,verification_failed, verification_pending

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('login/', login, name='login'),  # Use LoginView
    path('index/', index, name='index'),
    path('signup/', signup, name='signup'),
    path('verify/<str:uidb64>/<str:token>/', verify_email, name='verify_email'),
    path('verification-pending/', verification_pending, name='verification_pending'),
    path('verification-failed/', verification_failed, name='verification_failed'),
]
