
from django.urls import path, reverse_lazy
from django.conf import settings
from . import views 
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views



app_name = 'users'
urlpatterns = [

    path('register', views.register, name='register'),
    path('login', views.login_form, name='login'),
    path('logout', views.logout_user, name='logout'),

    path('forgot-password', views.forgot_password, name='forgot_password'),
    path('change-password/<token>', views.change_password, name='change_password'),
    # path('reset/<token>/',
    #  auth_views.PasswordResetConfirmView.as_view(template_name='users/password-confirm.html'),
    #  name='password_reset_confirm'),

    path('', views.index, name='index'),
    path('products', views.products, name='products'),
    path('cart', views.cart, name='cart'),
    path('checkout', views.checkout , name='checkout'),
    path('update-item', views.updateItem , name='update_item'),
    path('process-order', views.processOrder, name='process-order')

#     path('password_reset', auth_views.PasswordResetView.as_view(success_url = reverse_lazy('users:password_reset_done')), name="password_reset"),

#     path('pasword_reset_done', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),

#     re_path(r'^password_reset_confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
# auth_views.PasswordResetConfirmView.as_view(),name="password_reset_confirm"),

#     path('password_reset_complete', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)