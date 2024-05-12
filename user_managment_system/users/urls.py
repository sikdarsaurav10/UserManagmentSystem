from django.urls import path
from .views import UsersDataList

app_name='users'

urlpatterns = [
    path('users', UsersDataList.as_view(), name="users"),
    path('users/<int:id>', UsersDataList.as_view(), name="single_user"),
]