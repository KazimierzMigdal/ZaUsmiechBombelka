from .models import Product
from actions.utils import create_action
from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import (CreateView,
                                ListView,
                                DetailView,
                                UpdateView,
                                DeleteView)
from messanger_system.models import Message
import redis


r=redis.StrictRedis(host=settings.REDIS_HOST,
                    port=settings.REDIS_PORT,
                    db = settings.REDIS_DB)


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


class ProductDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Product
    success_url = '/market'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'market'
        return context

    def test_func(self):
        product = self.get_object()
        if self.request.user == product.author:
            return True
        else:
            return False


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


class ProductSoldView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    template_name = "market/sold_for.html"
    fields = ['sold_for']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context['section'] = 'market'
        return context

    def get_form(self, form_class=None):
        product = self.get_object()
        messages = Message.objects.filter(Q(subject=product)&Q(parent_msg__isnull=True))
        ids = [1,6]
        sold_id=[]
        for msg in messages:
            sold_id=msg.sender.id
            ids.append(sold_id)

        queryset=User.objects.filter(id__in=sold_id)
        if form_class is None:
            form_class = self.get_form_class()
        form = super(ProductSoldView, self).get_form(form_class)
        form.fields['sold_for'] = forms.ModelChoiceField(queryset=queryset, widget = forms.Select(attrs={'class':"form-control mt-2 mb-2"}))
        form.fields['sold_for'].lable=''
        return form

    def form_valid(self, form):
        form.instance.sold = True
        return super().form_valid(form)

    def test_func(self):
        product = self.get_object()
        if self.request.user == product.author:
            return True
        else:
            return False


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    fields = ['title', 'description', 'photo_1', 'photo_2', 'photo_3', 'tag_sex','tag_age', 'price']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'market'
        return context

    def test_func(self):
        product = self.get_object()
        if self.request.user == product.author:
            return True
        else:
            return False


def main(request):
    products = Product.objects.filter(sold=False).order_by('-date_posted')
    paginator = Paginator(products, 3)
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        products = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request,
                    'market/list_ajax.html',
                    {'products': products,
                    'section': 'market'})

    return render(request,
                    'market/index.html',
                    {'products': products,
                    'section': 'market'})


@login_required
def user_products(request, username):
    user = get_object_or_404(User,
                username=username,
                is_active=True)
    products = Product.objects.filter(author=user).order_by('-date_posted')

    return render(request,
                'market/index.html',
                {'products':products})
