from collections import defaultdict
from promise import Promise
from promise.dataloader import DataLoader
from .models import Comment

class CommentsByPostIdLoader(DataLoader):
    def batch_load_fn(self, post_ids):
        comments_by_post_ids = defaultdict(list)
        for comment in Comment.objects.filter(post_id__in=post_ids).iterator():
            comments_by_post_ids[comment.post_id].append(comment)
        return Promise.resolve([comments_by_post_ids.get(post_id, [])
                                for post_id in post_ids])
