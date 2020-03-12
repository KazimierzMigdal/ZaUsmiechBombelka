from django.shortcuts import (render,
                            redirect,
                            get_object_or_404)
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        UserPassesTestMixin)
from django.views.generic.edit import FormMixin
from .models import (Post,
                    Descriptione,
                    Comment)
from .forms import PostForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.generic import (ListView,
                                DetailView,
                                CreateView,
                                UpdateView,
                                DeleteView)

from django.core.paginator import (Paginator,
                                EmptyPage,
                                PageNotAnInteger)
from django.http import JsonResponse, HttpResponse
from django import forms
from django.contrib import messages
from actions.utils import create_action
from .forms import CommentForm
from django.urls import reverse


@login_required
def home(request):
    posts = Post.objects.all().order_by('-date_posted')
    paginator = Paginator(posts, 3)
    page = request.GET.get('page')

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            create_action(request.user, 'dodał post', post)
            messages.success(request, f'Post został dodany')
            return redirect('blog-home')
    else:
        form = PostForm()

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        images = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request,
                    'blog/list_ajax.html',
                    {'posts': posts,
                    'section': 'blog'})
    return render(request,
                    'blog/home.html',
                    {'posts': posts,
                    'section': 'blog',
                    'form': form})

class PostDetailView(FormMixin, DetailView):
    model = Post
    form_class = CommentForm

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['section'] = 'blog'
        context['cos'] = self.object.id
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = Post.objects.get(pk=self.kwargs.get('pk'))
        create_action(self.request.user, 'skomentował', Post.objects.get(pk=self.object.id))
        messages.success(self.request, f'Skomentowałeś post')
        form.save()
        return super(PostDetailView, self).form_valid(form)

@login_required
def user_posts(request, username):
    user = get_object_or_404(User,
                username=username,
                is_active=True)
    posts = Post.objects.filter(author=user).order_by('-date_posted')

    paginator = Paginator(posts, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        posts = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request,
                    'blog/list_ajax.html',
                    {'posts': posts,
                    'section': 'blog'})

    return render(request,
                    'blog/home.html',
                    {'posts': posts,
                    'section': 'blog'})




class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'blog'
        return context

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        form = super(PostCreateView, self).get_form(form_class)
        form.fields['content'].widget = forms.Textarea(attrs={"rows":"6", "class":"form-control"})
        form.fields['title'].widget = forms.TextInput(attrs={"class":"form-control"})
        return form


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False


class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False


def about(request):
    context = { 'title': 'About',
                'Descriptiones': Descriptione.objects.all()
                }
    return render(request, 'blog/about.html', context)


class CommentCreateView(LoginRequiredMixin,CreateView):
    model = Comment
    fields = ['text']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = Post.objects.get(pk=self.kwargs.get('pk'))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'blog'
        context['post'] = Post.objects.get(pk=self.kwargs.get('pk'))
        create_action(self.request.user, 'skomentował', Post.objects.get(pk=self.kwargs.get('pk')))
        return context

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        form = super(CommentCreateView, self).get_form(form_class)
        form.fields['text'].widget = forms.Textarea(attrs={"rows":"6", "class":"form-control"})
        return form

@login_required
@require_POST
def post_like(request):
    post_id = request.POST.get('id')
    action = request.POST.get('action')
    if post_id and action:
        try:
            post = Post.objects.get(id=post_id)
            if action == 'like':
                post.users_like.add(request.user)
            else:
                post.users_like.remove(request.user)
            return JsonResponse({'status':'ok'})
        except:
            pass
    return JsonResponse({'status':'ko'})


@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Post.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
                create_action(request.user, 'polubił', image)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status':'ok'})
        except:
            pass
    return JsonResponse({'status':'ko'})
