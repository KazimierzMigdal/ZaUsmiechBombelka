from django.shortcuts import render
from .models import Action
from django.contrib.auth.models import User
from market.models import Product

def actions(request):
    actions=Action.objects.all()
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id',
                                                       flat=True)
    if following_ids:
        # If user is following others, retrieve only their actions
        actions = actions.filter(user_id__in=following_ids)
        actions = actions.select_related('user', 'user__profile').prefetch_related('target')

    products = Product.objects.all()[:4]
    users = User.objects.all()[:4]
    return render(request, 'actions/action/detail.html', {'section': 'actions',
                                                        'actions': actions,
                                                        'products': products,
                                                        'users':users})
