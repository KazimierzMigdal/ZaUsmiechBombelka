from .forms import (UserRegisterForm,
                    UserUpdateForm,
                    ProfileUpdateForm)
from .models import Contact
from actions.utils import create_action
from blog.models import Post
from django import forms
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import (render,
                            redirect,
                            get_object_or_404)
from django.views.decorators.http import require_POST
from market.models import Product


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.interested_sex_tag = form.cleaned_data.get('interested_sex_tag')
            user.profile.interested_age_tag = form.cleaned_data.get('interested_age_tag')
            user.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You are able to log in!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request,'users/register.html', {'form': form})


@login_required
def profile(request, username):
    user = get_object_or_404(User,
                            username=username,
                            is_active=True)
    posts = Post.objects.filter(author=user).order_by('-date_posted')[:3]
    products = Product.objects.filter(author=user).order_by('-date_posted')[:3]
    context = {
        'posts': posts,
        'products': products,
        'user': user,
    }
    return render(request, 'users/profile.html', context)


@login_required
def profile_editor(request):
    username = request.user.username
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,
                                instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                    request.FILES,
                                    instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            new_username = u_form.cleaned_data['username']
            messages.success(request, f'Twój profil został zaktualizowany')
            return redirect('profile', new_username)
        else:
            print(u_form.errors)
            print(p_form.errors)
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'users/profile_editor.html', context)


@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user,
                                            user_to=user)
                create_action(request.user, 'zaczął obserwować', user)
            else:
                Contact.objects.filter(user_from=request.user,
                                    user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'ko'})
    return JsonResponse({'status': 'ko'})


class MyPasswordResetView(PasswordResetView):
    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        form = super(MyPasswordResetView, self).get_form(form_class)
        form.fields['email'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
        form.fields['email'].lable = ''
        return form

class MyPasswordResetConfirmView(PasswordResetConfirmView):
    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        form = super(MyPasswordResetConfirmView, self).get_form(form_class)
        form.fields['new_password1'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New password'})
        form.fields['new_password1'].label = False
        form.fields['new_password1'].help_text = None
        form.fields['new_password2'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password confirmation'})
        form.fields['new_password2'].label = False
        form.fields['new_password2'].help_text = None
        return form
