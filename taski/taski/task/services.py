from taski.task.models import Comment


def add_new_comment_to_task(auther, content, task):
    comment = Comment.objects.create(author=auther, content=content, task=task)
    comment.save()
    return comment
