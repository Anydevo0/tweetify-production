from django.urls import path
from . import views

urlpatterns = [
    path('/', views.home_page, name='home_page'),
    path('list/', views.tweet_list, name='tweet_list'),
    path('mytweets/', views.my_tweets, name='my_tweets'),
    path('create/', views.tweet_create, name='tweet_create'),
    path('<int:tweet_id>/edit/', views.tweet_edit, name='tweet_edit'),
    path('<int:tweet_id>/delete/', views.tweet_delete, name='tweet_delete'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('users/', views.display_profiles, name='display_profiles'),
    path('edit/profile/', views.update_profile, name='update_profile'),
    path('profile/<str:username>/follow/', views.follow, name='follow'),
    path('profile/<str:username>/unfollow/', views.unfollow, name='unfollow'),
    path('profile/<str:username>/followers/', views.followers_list, name='followers_list'),
    path('profile/<str:username>/following/', views.following_list, name='following_list'),

    # path('search-users/', views.search_users, name='search_users'),
] 