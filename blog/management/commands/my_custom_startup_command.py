# my_app/management/commands/my_custom_startup_command.py
# cf https://pythonin1minute.com/where-to-put-django-startup-code/

from django.core.management.base import BaseCommand, CommandError
from blog.models import Post, Comment

class Command(BaseCommand):
    help = 'My custom startup command'

    def handle(self, *args, **kwargs):
        try:
            for ir in range(10):
                i = ir + 1
                post = Post(title=f'Post {i}', text=f'text for post {i}')
                post.save()
                for jr in range(ir):
                    j = jr + 1
                    comment = Comment(text=f'comment {j} for post {i}', post=post)
                    comment.save()
        except:
            raise CommandError('Initalization failed.')
