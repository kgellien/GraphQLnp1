from django.urls import path
from graphene_django.views import GraphQLView
from . import views
from .views_gql import CustomGraphQLView
#from . import views_gql.CustomGraphQLView

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<pk>/remove/', views.post_remove, name='post_remove'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
]

urlpatterns = [
    path('graphql/', CustomGraphQLView.as_view(graphiql=True)),
]
