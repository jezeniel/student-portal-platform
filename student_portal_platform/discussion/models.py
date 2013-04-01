from django.utils import timezone
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify

from users.models import UserInfo


class DiscussionAbstract(models.Model):
    author = models.ForeignKey(User)
    content = models.TextField()
    content_html = models.TextField(blank=True)
    last_post = models.DateTimeField(null=True)
    post_date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    class Meta:
        abstract = True


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(blank=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __unicode__(self):
        return self.name

    def get_latest_thread(self):
        try:
            thread = self.thread_set.latest('last_post')
        except Thread.DoesNotExist:
            return None
        else:
            return thread

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class Thread(DiscussionAbstract):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=100)
    views = models.IntegerField(default=0)

    def save(self):
        if self.last_post is None:
            self.last_post = timezone.now()
            author = UserInfo.objects.get(user=self.author)
            author.posts += 1
            author.save()
        super(Thread, self).save()

    def get_latest_author(self):
        try:
            author = self.post_set.latest('post_date').author
        except Post.DoesNotExist:
            return self.author
        else:
            return author

    def more_than_oneday(self):
        if timezone.now() > self.last_post + timezone.timedelta(days=1):
            return True
        return False

    def get_absolute_url(self):
        return reverse('discuss:view', kwargs={'thread_id': self.pk, 'category': self.category.slug})

    def __unicode__(self):
        return self.title


class Post(DiscussionAbstract):
    title = models.CharField(max_length=100, blank=True)
    thread = models.ForeignKey(Thread)

    def save(self, *args, **kwargs):
        self.thread.last_post = timezone.now()
        self.thread.save()
        author = UserInfo.objects.get(user=self.author)
        author.posts += 1
        author.save()
        super(Post, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title
