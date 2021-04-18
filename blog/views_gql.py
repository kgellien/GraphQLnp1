from django.utils.functional import cached_property
from graphene_django.views import GraphQLView
from .loaders import CommentsByPostIdLoader

class GQLContext:
    def __init__(self, request):
        self.request = request
    @cached_property
    def user(self):
        return self.request.user
    @cached_property
    def comments_by_post_id_loader(self):
        return CommentsByPostIdLoader()

class CustomGraphQLView(GraphQLView):
    def get_context(self, request):
        return GQLContext(request)
