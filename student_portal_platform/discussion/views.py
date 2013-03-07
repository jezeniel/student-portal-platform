from django.views.generic import ListView, DetailView, View
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect

from .models import Thread,Post
from .forms import ThreadForm, ReplyForm, QuickReplyForm

class LoginRequiredMixin(object):
    '''Mixin for class views that requires login'''
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)
    
class ThreadCreate(LoginRequiredMixin, CreateView):
    model = Thread
    form_class = ThreadForm
    template_name = "development/discussion-create.html"

    def get_context_data(self, **kwargs):
        context = super(ThreadCreate, self).get_context_data(**kwargs)
        context['thread_form'] = context['form']    
        return context
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(ThreadCreate,self).form_valid(form)

class ReplyCreate(LoginRequiredMixin, CreateView):
    model = Post
    form_class = ReplyForm
    template_name = "development/discussion-view.html"
    success_url = reverse_lazy("discuss:view")

    def get_context_data(self, **kwargs):
        context = super(ReplyCreate,self).get_context_data(**kwargs)
        context['reply_form'] = context['form']
        return context
    
    def form_valid(self,form):
        form.instance.author = self.request.user
        return super(ReplyCreate,self).form_valid(form)

class ThreadList(LoginRequiredMixin, ListView):
    model = Thread
    context_object_name = "threads"
    template_name = "development/discussion.html"

class ThreadDetail(LoginRequiredMixin, View):
    template_name = "development/discussion-view.html"
    
    def get(self,request, thread_id, *args, **kwargs):
        thread = get_object_or_404(Thread, id = thread_id)
        thread_name = "VIEWED_THREAD_%s" % (thread_id)
        if not self.request.session.get(thread_name , False):
            thread.views += 1
            self.request.session[thread_name] = True
        thread.save()
        reply_form = QuickReplyForm()
        return render(request, self.template_name, {'thread':thread, 'reply_form': reply_form})
    
    def post(self, request, thread_id, *args, **kwargs):
        thread = get_object_or_404(Thread, id = thread_id)
        reply_form = QuickReplyForm(request.POST)
        if reply_form.is_valid():
            author = request.user
            content = reply_form.cleaned_data['content']
            title = thread.title
            reply = Post.objects.create(content = content, author = author, title = title, thread = thread)
            return redirect("discuss:view", thread_id = thread.id )
        return HttpResponse("WHAT?")
