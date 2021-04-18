from graphene_django import DjangoObjectType, DjangoConnectionField
from graphene_django.debug import DjangoDebug
import graphene
import logging
from graphene import List, ObjectType, Schema
from .models import Post, Comment

logger = logging.getLogger(__name__)

class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        only_fields = ('text',)

class PostType(DjangoObjectType):
    comments = List(CommentType)

    class Meta:
        model = Post
        only_fields = ('title', 'text')

    def resolve_comments(self, info, **kwargs):
        logger.info(f'PostType.resolve_comments')
        return self.comments.all()

class PostLoaderType(DjangoObjectType):
    comments = List(CommentType)

    class Meta:
        model = Post
        only_fields = ('title', 'text')

    def resolve_comments(self, info, **kwargs):
        logger.info(f'PostLoaderType.resolve_comments')
        return info.context.comments_by_post_id_loader.load(self.id)

class PostRawType(DjangoObjectType):
    comments = List(CommentType)

    class Meta:
        model = Post

    def resolve_comments(self, info, **kwargs):
        logger.info(f'PostRawType.resolve_comments')
        return self.comments.all()

class Query(ObjectType):
    debug = graphene.Field(DjangoDebug, name='_debug')
    postsNaive = graphene.List(PostType)
    postsLoader = graphene.List(PostLoaderType)
    postsPrefetch = graphene.List(PostRawType)
    #comments = graphene.List(CommentType)

    def resolve_postsNaive(self, info, **kwargs):
        logger.info(f'resolve_postsNaive')
        return Post.objects.all()

    def resolve_postsLoader(self, info, **kwargs):
        logger.info(f'resolve_postsLoader')
        return Post.objects.all()

    def resolve_postsPrefetch(self, info):
        logger.info(f'resolve_postsPrefetch')
        #logger.info(f'info {info}')
        #logger.info(f'info.schema {info.schema}')
        #logger.info(f'info.field_name {info.field_name}')
        #logger.info(f'info.parent_type {info.parent_type}')
        #logger.info(f'info.field_asts[0] {info.field_asts[0]}')
        #logger.info(f'type(info.field_asts[0]) {type(info.field_asts[0])}')
        #result = Post.objects.all()
        result = Post.objects.prefetch_related('comments').all() # -> QuerySet
        #logger.info(f'resolve_postR: {result}')
        return result

schema = Schema(query=Query)
