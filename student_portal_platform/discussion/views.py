from django.views.generic import ListView, DetailView, View
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Category, Thread, Post, SubjectThread, SubjectPost
from .forms import ThreadForm, ReplyForm, QuickReplyForm, SubjectThreadForm
from subject.models import Subject


class LoginRequiredMixin(object):
    '''Mixin for class views that requires login'''

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class ThreadCreate(LoginRequiredMixin, CreateView):
    model = Thread
    form_class = ThreadForm
    template_name = "final/create-thread.html"

    def get_context_data(self, **kwargs):
        context = super(ThreadCreate, self).get_context_data(**kwargs)
        context['create_form'] = context['form']
        context['category'] = Category.objects.get(slug=self.kwargs['category'])
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.category = Category.objects.get(slug=self.kwargs['category'])
        return super(ThreadCreate,self).form_valid(form)


class ReplyCreate(LoginRequiredMixin, CreateView):
    model = Post
    form_class = ReplyForm
    template_name = "development/discussion-view.html"
    success_url = reverse_lazy("discuss:view")

    def get_context_data(self, **kwargs):
        context = super(ReplyCreate, self).get_context_data(**kwargs)
        context['reply_form'] = context['form']
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(ReplyCreate, self).form_valid(form)


class CategoryList(LoginRequiredMixin, ListView):
    model = Category
    context_object_name = "categories"
    template_name = "final/discuss-category.html"


class ThreadList(LoginRequiredMixin, ListView):
    model = Thread
    context_object_name = "threads"
    paginate_by = 10
    template_name = "final/discuss-topics.html"

    def get_context_data(self, **kwargs):
        context = super(ThreadList, self).get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, slug = self.kwargs['category'])
        return context

    def get_queryset(self, *args, **kwargs):
        slug = self.kwargs['category']
        category = get_object_or_404(Category, slug=slug)
        return category.thread_set.order_by("-last_post")


class ThreadDetail(LoginRequiredMixin, View):
    template_name = "final/discuss-view.html"

    def get(self, request, thread_id, *args, **kwargs):
        thread = get_object_or_404(Thread, id=thread_id)
        #increment the topic views
        thread_name = "VIEWED_THREAD_%s" % (thread_id)
        if not self.request.session.get(thread_name, False):
            thread.views += 1
            self.request.session[thread_name] = True
            thread.save()

        paginator = Paginator(thread.post_set.all(), 8)
        page = request.GET.get('page', 1)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        page = paginator.num_pages + (posts.end_index() % 8 == 0)

        reply_form = QuickReplyForm(initial={'next': page})
        return render(request, self.template_name, {'thread': thread, 'reply_form': reply_form,
                                                    'category': thread.category, 'posts':posts})

    def post(self, request, thread_id, *args, **kwargs):
        thread = get_object_or_404(Thread, id=thread_id)
        reply_form = QuickReplyForm(request.POST)
        if reply_form.is_valid():
            author = request.user
            content = reply_form.cleaned_data['content']
            title = thread.title
            next = reply_form.cleaned_data['next']
            post = Post.objects.create(content=content, author=author, title=title, thread=thread)
        url = reverse("discuss:view", kwargs={'category':thread.category.slug, 'thread_id':thread.id})
        url += "?page=%s#post-%s" % (next,post.id)
        return redirect(url)

class SubjectThreadList(LoginRequiredMixin, ListView):
    model = SubjectThread
    context_object_name = "subjectthreads"
    paginate_by = 10
    template_name = "final/course-discussion/discuss-topics.html"

    def get_context_data(self, **kwargs):
        context = super(SubjectThreadList, self).get_context_data(**kwargs)
        context['subject'] = get_object_or_404(Subject, id=self.kwargs['course_id'])
        return context

    def get_queryset(self, *args, **kwargs):
        id = self.kwargs['course_id']
        subject = get_object_or_404(Subject, id=id)
        return subject.subjectthread_set.order_by("-last_post")

class SubjectThreadCreate(LoginRequiredMixin, CreateView):
    model = SubjectThread
    form_class = SubjectThreadForm
    template_name = "final/create-thread.html"

    def get_context_data(self, **kwargs):
        context = super(SubjectThreadCreate, self).get_context_data(**kwargs)
        context['create_form'] = context['form']
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.subject = Subject.objects.get(id=self.kwargs['course_id'])
        return super(SubjectThreadCreate,self).form_valid(form)


class SubjectThreadDetail(LoginRequiredMixin, View):
    template_name = "final/course-discussion/discuss-view.html"

    def get(self, request, thread_id, *args, **kwargs):
        thread = get_object_or_404(SubjectThread, id=thread_id)
        #increment the topic views
        thread_name = "COURSE_VIEWED_THREAD_%s" % (thread_id)
        if not self.request.session.get(thread_name, False):
            thread.views += 1
            self.request.session[thread_name] = True
            thread.save()

        paginator = Paginator(thread.subjectpost_set.all(), 8)
        page = request.GET.get('page', 1)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        page = paginator.num_pages + (posts.end_index() % 8 == 0)

        reply_form = QuickReplyForm(initial={'next': page})
        return render(request, self.template_name, {'thread': thread, 'reply_form': reply_form,
                                                    'subject': thread.subject, 'posts':posts})

    def post(self, request, thread_id, *args, **kwargs):
        thread = get_object_or_404(SubjectThread, id=thread_id)
        reply_form = QuickReplyForm(request.POST)
        if reply_form.is_valid():
            author = request.user
            content = reply_form.cleaned_data['content']
            title = thread.title
            next = reply_form.cleaned_data['next']
            post = SubjectPost.objects.create(content=content, author=author, title=title, thread=thread)
        url = reverse("course:discuss_view", kwargs={'course_id':thread.subject.id, 'thread_id':thread.id})
        url += "?page=%s#post-%s" % (next,post.id)
        return redirect(url)
