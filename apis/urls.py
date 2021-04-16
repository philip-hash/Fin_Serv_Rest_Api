from django.contrib import admin



from apis import views
from apis import stock_views

from django.urls import path,include

from rest_framework.documentation import include_docs_urls






urlpatterns = [
    path('login/',views.login.as_view()),
    path('register/',views.Register.as_view()),
    path('logout/',views.logout.as_view()),
    path('activate/<uidb64>/<token>',views.VerificationView.as_view(),name="activate"),
    path('password_reset/',views.password_reset.as_view()),
    path('set-new-password/<uidb64>/<token>',views.CompletePasswordReset.as_view(),name="reset-user-password"),

    path('stock_list/',stock_views.stock_list.as_view()),
    path('stock_list/<stock>/',stock_views.stock_details.as_view()),

    path('matrix_list/',stock_views.matrix_list.as_view()),
    path('matrix_list/<matrix>',stock_views.matrix_details.as_view()),
    path(r'docs/', include_docs_urls(title='fin_serv API')),
]


