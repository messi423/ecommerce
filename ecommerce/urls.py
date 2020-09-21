from django.contrib import admin
from django.urls import path, include
from users import views as users_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from products.views import *
from rest_framework.routers import DefaultRouter
from products.views import OrderView

router = DefaultRouter()
router.register(r'article', ArticleView, basename='article')
#router.register(r'order', OrderView, basename='order')

urlpatterns = [
    path('api/', include(router.urls)),
    path('', include('products.urls')),
   # path('order/', OrderView.as_view(), name='order'),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('products/', include('products.urls')),
    path('register/', users_views.register, name='register'),
    path('profile/', users_views.profile, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<str:token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete')

]


if settings.DEBUG:
    urlpatterns += [

                  ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

