from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

class DiscussionAbstract(models.Model):
    author = models.ForeignKey(User)
    content = models.TextField()
    content_html = models.TextField(blank = True)
    last_edit = models.DateTimeField(auto_now = True)
    post_date = models.DateTimeField(auto_now_add = True)
    rating = models.IntegerField(default = 0)
       
    class Meta:
        abstract = True
        
class Thread(DiscussionAbstract):
    title = models.CharField(max_length = 100)
    views = models.IntegerField(default = 0)
    posts = models.IntegerField(default = 0)
    
    def get_latest_author(self):
        try:
            author = self.post_set.latest('post_date').author
        except Post.DoesNotExist:
            return self.author
        else:
            return author
    
    def get_absolute_url(self):
        return reverse('discuss:view', kwargs = { 'thread_id': self.pk })
        
class Post(DiscussionAbstract):
    title = models.CharField(max_length = 100, blank = True)
    thread = models.ForeignKey(Thread)
    
    

    
