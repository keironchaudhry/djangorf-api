from django.urls import path
from user_comments import views

urlpatterns = [
    path(
        'user_comments/',
        views.CommentList.as_view()
    ),
    path(
        'user_comments/<int:pk>/',
        views.CommentDetail.as_view()
    ),
]
