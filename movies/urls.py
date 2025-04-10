from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [  
    path('payment/', views.payment_view, name='payment'),  # New payment URL
    path('', views.movie_list, name='movie_list'),
    path('search/', views.search_movies, name='search_movies'),  # New search URL
    path('<int:movie_id>/theaters', views.theater_list, name='theater_list'),
    path('theater/<int:theater_id>/seats/book/', views.book_seats, name='book_seats'),
    path('payment/confirm/', views.payment_confirm, name='payment_confirm'),  # New payment confirmation URL
    path('profile/', views.user_profile, name='user_profile'),  # User profile URL
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
