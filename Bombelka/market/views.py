from .models import Product
from actions.utils import create_action
from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.views.generic import (CreateView,
                                ListView,
                                DetailView,
                                UpdateView,
                                DeleteView)
import redis


r=redis.StrictRedis(host=settings.REDIS_HOST,
                    port=settings.REDIS_PORT,
                    db = settings.REDIS_DB)


class ProductListView(LoginRequiredMixin,ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'market/index.html'
    ordering = ['-date_posted']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'market'
        return context


@login_required
def user_products(request, username):
    user = get_object_or_404(User,
                username=username,
                is_active=True)
    products = Product.objects.filter(author=user).order_by('-date_posted')

    return render(request,
                'market/index.html',
                {'products':products})


class ProductCreateView(LoginRequiredMixin,CreateView):
    model = Product
    success_url = '/market'
    fields = ['title', 'description', 'photo_1', 'photo_2', 'photo_3', 'tag_sex','tag_age', 'price']

    def form_valid(self, form):
        form.instance.author = self.request.user
        post = form.save(commit=False)
        post.save()
        create_action(self.request.user, 'dodał produkt', post)
        messages.success(self.request, f'Produkt został dodany')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'market'
        return context

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        form = super(ProductCreateView, self).get_form(form_class)
        form.fields['description'].widget = forms.Textarea(attrs={"rows":"6", "class":"form-control", "placeholder": "Opis Produktu"})
        form.fields['title'].widget = forms.TextInput(attrs={"class":"form-control",  "placeholder": "Nazwa Produktu"})
        form.fields['price'].widget = forms.NumberInput(attrs={"class":"form-control", "placeholder": "0,00", 'step':".01"})
        form.fields['price'].lable=''
        form.fields['title'].lable=''
        return form


class ProductDetailView(LoginRequiredMixin,DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'market'
        product = Product.objects.get(pk=self.kwargs.get('pk'))
        total_views = r.incr('product:{}:views'.format(product.id))
        r.zincrby('product_ranking', 1,  product.id)
        context['total_views'] = total_views
        return context


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    fields = ['title', 'description', 'photo_1', 'photo_2', 'photo_3', 'tag_sex','tag_age', 'price']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        product = self.get_object()
        if self.request.user == product.author:
            return True
        else:
            return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'market'
        return context


class ProductDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Product
    success_url = '/'

    def test_func(self):
        product = self.get_object()
        if self.request.user == product.author:
            return True
        else:
            return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'market'
        return context

